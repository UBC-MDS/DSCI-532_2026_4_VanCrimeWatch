from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page, expect

# set path to app file
app = create_app_fixture("../src/app.py")


def test_initial_dashboard_state(page: Page, app: ShinyAppProc) -> None:
    """The dashboard loads with the default year (2025) and 'monthly' time display selected."""
    page.goto(app.url)
    
    # check default Year 
    year_checkbox = controller.InputCheckboxGroup(page, "input_year")
    year_checkbox.expect_selected(["2025"])
    
    # check default time display 
    time_radio = controller.InputRadioButtons(page, "time_display")
    time_radio.expect_selected("monthly")


def test_filter_changes_update_ui(page: Page, app: ShinyAppProc) -> None:
    """Changing filters successfully updates the UI state."""
    page.goto(app.url)
    
    time_radio = controller.InputRadioButtons(page, "time_display")
    year_checkbox = controller.InputCheckboxGroup(page, "input_year")
    
    # change the filters
    time_radio.set("hourly")
    year_checkbox.set(["2024", "2025"])
    
    # verify the new changes 
    time_radio.expect_selected("hourly")
    year_checkbox.expect_selected(["2024", "2025"])


def test_reset_button_restores_defaults(page: Page, app: ShinyAppProc) -> None:
    """Clicking the reset button restores altered filters back to their original default states."""
    page.goto(app.url)
    
    year_checkbox = controller.InputCheckboxGroup(page, "input_year")
    reset_btn = controller.InputActionButton(page, "reset_btn")
    
    # change the filters
    year_checkbox.set(["2023"])

    # confirm the changes 
    year_checkbox.expect_selected(["2023"])
    
    # click the 'Reset Filters' button
    reset_btn.click()
    
    # verify the year is back to the default 2025
    year_checkbox.expect_selected(["2025"])


def test_empty_year_warning(page: Page, app: ShinyAppProc) -> None:
    """Deselecting all years triggers a warning notification and forces the selection back to 2025."""
    page.goto(app.url)
    
    year_checkbox = controller.InputCheckboxGroup(page, "input_year")
    
    # deselect the default year and leave it completely empty
    year_checkbox.set([])
    
    # verify the warning notification appeared
    notification = page.locator(".shiny-notification")
    expect(notification).to_have_count(1, timeout=5000) # give it up to 5 seconds to appear
    expect(notification).to_contain_text("Please select at least one year")

    # verify it defaulted back to 2025 
    year_checkbox.expect_selected(["2025"])