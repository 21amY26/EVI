"""Rich Layout - EVI Dashboard."""
from rich.layout import Layout
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.console import Console
from engine import EngineStats

console = Console()

def create_header():
    header_text = Text("🤖 EVI — Evidence Investigator", style="bold bright_magenta")
    return Panel(header_text, box=box.HEAVY)

def create_evi_panel(message='"Tell me what you\'d like to do."'):
    text = Text(message, style="italic cyan")
    return Panel(text, title="[bold cyan]🤖 EVI Assistant[/]", box=box.ROUNDED)

def create_actions_panel():
    text = Text.from_markup(
        '[bold cyan]▶ 1. Forensic Scan[/]\n'
        '[bold cyan]▶ 2. Live Monitor[/]\n'
        '[bold cyan]▶ 3. Hybrid Mode[/]\n'
        '[bold cyan]▶ 4. Help[/]\n'
        '[bold red]▶ 0. Exit[/]\n'
        '[bold white]Type 0-4 at EVI > prompt:[/]'
    )
    return Panel(text, title="[bold yellow]⚡ QUICK ACTIONS[/]", box=box.ROUNDED)

def create_dashboard_layout(evi_message='"Tell me what you\'d like to do."'):
    layout = Layout()
    layout.split_column(
        Layout(name="header",  size=3),
        Layout(name="evi",     size=5),
        Layout(name="actions", size=12),
    )
    layout["header"].update(create_header())
    layout["evi"].update(create_evi_panel(evi_message))
    layout["actions"].update(create_actions_panel())
    return layout