from pyfiglet import Figlet
from rich.console import Console

console = Console()

figlet = Figlet(font='big')
text = figlet.renderText("AirCrackX")

# Print colored text using Rich
console.print(f"[cyan]{text}[/cyan]")
