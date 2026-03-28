#!/usr/bin/env python3
"""EVI Main - Dashboard TUI."""
import sys
import signal
from rich.console import Console
from display import run_dashboard
from rich import print as rprint
from rich.text import Text
from rich.panel import Panel

def print_colorful_banner():
    banner = """███             ███             ██
       ███░            ███░            ███░
     ███░            ███░            ███░  
   ███░            ███░            ███░    
 ███░            ███░            ███░      
██░            ███░            ███░        
░            ███░            ███░          
            ░░░             ░░░            
     ████████████ ██████  █████ ████████   
   ███▒▒███▒▒▒▒▒█▒▒███░  ▒▒███ ▒▒█████░    
 ███░  ▒███  █ ▒ █▒███    ▒███  ▒███░      
██░    ▒██████ ███▒███    ▒███ █▒███       
░      ▒███▒▒███░ ▒▒███   ██████▒███       
       ▒███ ▒█░ █  ▒▒▒█████▒██░ ▒███       
       ██████████    ▒▒█████░   ███████
      ▒▒▒▒▒▒▒▒▒▒      ▒▒▒░░    ▒▒▒▒▒    ░░░
 ███             ███             ███       
██░            ███░            ███░        
░            ███░            ███░          
           ███░            ███░            
         ███░            ███░            ██
       ███░            ███░            ███░
     ███░            ███░            ███░  
    ░░░             ░░░             ░░░    
             ███             ███           
           ███░            ███░            
         ███░            ███░            ██"""
    # Color mapping
    markup = (banner
        .replace('███', '[bold red]███[/]')
        .replace('██░', '[bold red]██░[/]')
        .replace('██', '[bold red]██[/]')
        .replace('░', '[dim cyan]░[/]')
        .replace('▒▒', '[yellow]▒▒[/]')
        .replace('▒', '[orange1]▒[/]')
        .replace('█', '[bright_red]█[/]')
        )
    rprint(Panel(Text.from_markup(markup), style="on blue"))

print_colorful_banner()
print("""
────────────────────────────────────────────
🤖 EVI — Evidence Investigator
────────────────────────────────────────────

Initializing...

Hello — I'm EVI.
I analyze system logs to detect missing activity, suspicious gaps,
and potential tampering.

Give me logs, and I'll help you understand:
• What happened
• What's missing
• Whether it's normal or suspicious

────────────────────────────────────────────
🔍 What I look for:
• Timestamp gaps in logs
• Inconsistent log sequences
• Signs of deletion or manipulation

📊 How I classify findings:
• LOW       → normal system delay
• MEDIUM    → unusual, worth checking
• CRITICAL  → likely tampering or deleted logs

────────────────────────────────────────────
🤖 EVI Assistant
"Systems are up. I'm ready when you are."
────────────────────────────────────────────

Press ENTER to continue...
""")
input()

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    run_dashboard()
