import html
import os
from datetime import datetime

import pandas as pd
from pymongo import MongoClient
from shiny import reactive, render, ui
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")
import re, markdown


try:
    _mongo_client = MongoClient(os.environ["PYMONGO_URI"])
    _collection = _mongo_client["vancrime"]["query_log"]
except Exception as e:
    print(f"[logger] Failed to connect to MongoDB: {e}")
    _mongo_client = None
    _collection = None

SCHEMA = ["timestamp", "user_query", "sql", "tool", "model", "llm_output", "input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens", "cost", "n_rows"]
DISPLAY_SCHEMA = ["timestamp", "user_query", "sql", "tool", "llm_output"]

def save_info(row: dict) -> None:
    try:
        _collection.insert_one(row)
    except Exception as e:
        print(f"[logger] MongoDB write failed: {e}")

def strip_suggestions(text: str) -> str:
    # Cut off at the horizontal rule that precedes suggestions
    text = re.sub(r'<span class="suggestion">|<.?span>', '', text)
    return text.strip()

def to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["tables"])

def format_sql(sql):
    return ui.HTML(
        f"""
        <pre style="
            margin:0;
            white-space:pre-wrap;
            word-break:break-word;
            overflow-wrap:anywhere;
            font-size:12px;
        "><code>{html.escape(sql)}</code></pre>
        """
    )

COOKIE_JS = ui.tags.script("""
(function() {
  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }
  function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + '=' + encodeURIComponent(value) +
      '; expires=' + expires + '; path=/; SameSite=Lax';
  }

  let token = getCookie('vancrime_user_token');
  if (!token) {
    token = 'vc-' + crypto.randomUUID();
    setCookie('vancrime_user_token', token, 365);
  }

  $(document).on('shiny:sessioninitialized', function() {
    Shiny.setInputValue('user_token', token, {priority: 'event'});
  });
})();
""")

history_tab = ui.nav_panel(
    "My Chat History",
    ui.card(
        ui.card_header(
            ui.div(
                "My Query History",
                ui.span(
                    ui.input_action_button(
                        "refresh_history",
                        ui.span(
                            ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>'),
                            " Load Latest",
                        ),
                        class_="btn-secondary btn-sm me-1",
                    ),
                    ui.download_button(
                        "download_history",
                        ui.span(
                            ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>'),
                            " Download CSV",
                        ),
                        class_="btn-success btn-sm",
                    ),
                    style="margin-left:auto; display:inline-flex; align-items:center;",
                ),
                style="display:flex; align-items:center; width:100%;",
            )
        ),
        ui.output_ui("history_content"),
    ),
)

def llm_logger(input, output, session, qc_vals):
    pending = reactive.value(None)
    
    def on_query(req):
        if req.name not in ("querychat_update_dashboard", "querychat_query"):
            return
        sql = req.arguments.get("query", "")
        if not sql:
            return
        turns = qc_vals.client.get_turns()
        user_turns = [t for t in turns if t.role == "user"]
        pending.set({
            "user_query": user_turns[-1].text if user_turns else "(unknown)",
            "sql": sql,
            "tool": req.name,
        })

    qc_vals.client.on_tool_request(on_query)

    @reactive.effect
    def flush_log():
        entry = pending()
        if not entry:
            return

        # Get last model response
        turns = qc_vals.client.get_turns()
        llm_turns = [t for t in turns if t.role != "user"]
        last = llm_turns[-1] if llm_turns else None

        # Fall back to second-to-last turn if last has no text
        if last and not last.text.strip():
            text_turns = [t for t in llm_turns if t.text and t.text.strip()]
            last = text_turns[-1] if text_turns else last

        llm_output = last.text if last else "(no model response)"
        entry["llm_output"] = strip_suggestions(llm_output)

        # Token + cost metadata
        if last and last.completion:
            usage = last.completion.usage
            entry["input_tokens"] = usage.input_tokens
            entry["output_tokens"] = usage.output_tokens
            entry["cache_read_tokens"] = usage.cache_read_input_tokens
            entry["cache_write_tokens"] = usage.cache_creation_input_tokens
            entry["cost"] = last.cost

        # Dataset metadata
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df

        entry.update({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "model": "anthropic/claude-haiku-4-5",
            "n_rows": len(df),
            "session_id": session.id,
        })

        try:
            entry["user_token"] = input.user_token()
        except Exception:
            entry["user_token"] = None

        save_info(entry)
        pending.set(None)

    @reactive.calc
    def history_data():
        input.refresh_history()
        try:
            tok = input.user_token()
        except Exception:
            return pd.DataFrame(columns=DISPLAY_SCHEMA)
        if not tok:
            return pd.DataFrame(columns=DISPLAY_SCHEMA)
        try:
            rows = list(_collection.find({"user_token": tok}, {"_id": 0}))
        except Exception as e:
            print(f"[logger] Error fetching history: {e}")
            return pd.DataFrame(columns=DISPLAY_SCHEMA)
        df = pd.DataFrame(rows)
        if not df.empty and "timestamp" in df.columns:
            df = df.sort_values("timestamp", ascending=False)
            df = df.drop(columns=["session_id", "user_token"], errors="ignore")
        return df

    @output
    @render.ui
    def history_content():
        df = history_data()
        if df.empty:
            return ui.div(
                ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:8px;opacity:0.4"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>'),
                ui.p("Click  Load Latest to retrieve your query history if present.", style="margin:0;"),
                style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:60px; color:#888;",
            )
        return ui.output_data_frame("history_table")

    @output
    @render.data_frame
    def history_table():
        df = history_data().copy()[[c for c in DISPLAY_SCHEMA if c in history_data().columns]]
        if "llm_output" in df.columns:
            df["llm_output"] = df["llm_output"].apply(
                lambda text: to_html(text) if isinstance(text, str) else text
            )
            df["llm_output"] = df["llm_output"].apply(ui.HTML)
        if "sql" in df.columns:
            df["sql"] = df["sql"].apply(
                lambda text: format_sql(text) if isinstance(text, str) else text
            )
        return render.DataGrid(df, width="100%")

    @output
    @render.download(filename="my_chat_history.csv")
    def download_history():
        yield history_data().to_csv(index=False)