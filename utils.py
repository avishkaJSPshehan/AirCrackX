from pyfiglet import Figlet
from rich.console import Console
import itertools

console = Console()

figlet = Figlet(font='big')
text = figlet.renderText("AirCrackX")

# Print colored text using Rich
console.print(f"[cyan]{text}[/cyan]")

password_list = []

def load_password_list():
    file = open("password.txt","r")
    l1 = file.readlines()
    for i in l1:
        new_password,emptySpace,extra = i.split(" ")
        password_list.append(new_password)

load_password_list()

print(password_list)
