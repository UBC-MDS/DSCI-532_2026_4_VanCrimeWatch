import os
from datetime import datetime

import pandas as pd
from pymongo import MongoClient
from shiny import reactive, render, ui
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")

_mongo_client = MongoClient(os.environ["PYMONGO_URI"])
_collection = _mongo_client["vancrime"]["query_log"]
SCHEMA = ["timestamp", "user_query", "sql", "tool", "model", "n_rows"]

def save_info(row: dict) -> None:
    try:
        _collection.insert_one(row)
    except Exception as e:
        print(f"[logger] MongoDB write failed: {e}")

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
                        class_="btn-outline-secondary btn-sm me-1",
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
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        entry["timestamp"] = datetime.now().isoformat(timespec="seconds")
        entry["model"] = "anthropic/claude-haiku-4-5"
        entry["n_rows"] = len(df)
        entry["session_id"] = session.id
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
            return pd.DataFrame(columns=SCHEMA)
        if not tok:
            return pd.DataFrame(columns=SCHEMA)
        rows = list(_collection.find({"user_token": tok}, {"_id": 0}))
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
        return render.DataGrid(history_data(), width="100%")

    @output
    @render.download(filename="my_chat_history.csv")
    def download_history():
        yield history_data().to_csv(index=False)