from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
import json
import os
from pathlib import Path

console = Console()
CONFIG_FILE = Path("config.json")
HISTORY_FILE = Path("clearcut_history.txt")

# Load or create config
if CONFIG_FILE.exists():
    config = json.loads(CONFIG_FILE.read_text())
    API_KEY = config.get("api_key", "")
else:
    API_KEY = ""

# First-time API key setup
if not API_KEY:
    console.print(Panel("Welcome to ClearCut! Need your free Groq API key", style="bold yellow"))
    console.print("[dim]→ Get it in 10 seconds: https://console.groq.com/keys[/dim]")
    key = console.input("\n[cyan]Paste your Groq API key → [/cyan]").strip()
    if not key.startswith("gsk_"):
        console.print("[red]Invalid key. Exiting.[/red]")
        exit()
    API_KEY = key
    CONFIG_FILE.write_text(json.dumps({"api_key": API_KEY}))
    console.print(Panel("API key saved forever!", style="bold green"))

client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
MODEL = "llama-3.3-70b-versatile"  

def ask(prompt):
    try:
        resp = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=1200
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}\nCheck internet or API key."

def save_history(problem, want, happy, avoid, card, answer):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\nProblem: {problem}\nWant: {want}\nDone: {happy}\nAvoid: {avoid}\n\nCard:\n{card}\n\nAnswer:\n{answer}\n→ SOLVED ✓\n{'='*60}\n")

console.print(Panel("[bold white on black] ClearCut — Think first. Answer second. [/bold white on black]", expand=False))

# Step 1
console.print(Panel("Step 1 → Paste your messy problem", style="bold yellow"))
problem = console.input("[cyan]→ [/cyan]").strip()
if not problem:
    console.print("[red]Nothing pasted. Bye![/red]")
    exit()

# Step 2 
console.print(Panel("Step 2 → I read your problem. Here are my suggestions:", style="bold magenta"))
suggestions = ask(f"From this problem suggest exactly 3 short lines:\nProblem: {problem}\n\nReply exactly:\n1. What you really want → [short]\n2. When you’ll be happy → [short]\n3. What to be careful about → [short]")
console.print(Panel(suggestions + "\n\n→ Press Enter to accept all\n→ Or type 1, 2, or 3 to change one line", title="Suggested filter", border_style="bright_blue"))

lines = [l.strip() for l in suggestions.split('\n') if l.strip().startswith(('1.', '2.', '3.'))]
s1 = lines[0].split('→', 1)[1].strip() if len(lines)>0 else ""
s2 = lines[1].split('→', 1)[1].strip() if len(lines)>1 else ""
s3 = lines[2].split('→', 1)[1].strip() if len(lines)>2 else ""

want, happy, avoid = s1, s2, s3

edit = console.input("[cyan]Press Enter = accept • or type 1/2/3 to change → [/cyan]").strip()
if edit == "1":
    want = console.input(f"   1. Change → ").strip() or want
elif edit == "2":
    happy = console.input(f"   2. Change → ").strip() or happy
elif edit == "3":
    avoid = console.input(f"   3. Change → ").strip() or avoid

if not (want and happy and avoid):
    console.print(Panel("All 3 required!", style="bold red"))
    exit()

console.print(Panel(f"Filter locked:\n1. {want}\n2. {happy}\n3. {avoid}", title="Moving on →", border_style="green"))

# Step 3 
console.print(Panel("Making your Clear Card…", style="dim"))
card = ask(f"Summarize into 5 short lines only:\nProblem: {problem}\nWant: {want}\nDone: {happy}\nAvoid: {avoid}")
console.print(Panel(card, title="Your Clear Card", border_style="green"))

# Step 4
console.print(Panel("Step 4 → How much help do you want?", style="bold cyan"))
console.print("   A) Only thinking steps\n   B) Small code example\n   C) One good pattern\n   D) Full ready answer")
choice = console.input("\n[cyan]A / B / C / D → [/cyan]").upper()
help_text = {"A":"Only thinking steps. No code.","B":"Small code example only.","C":"One good pattern.","D":"Full ready answer."}.get(choice,"Only thinking steps.")

console.print(Panel("Working…", style="dim"))
answer = ask(f"{help_text}\n\nClear Card:\n{card}")
console.print(Panel(answer, title="Your Answer", border_style="bold green"))

# Step 5 
while True:
    console.print(Panel("Step 5 → Is the problem now 100% solved?", style="bold white on black"))
    console.print("   [1] Yes — problem solved!\n   [2] No — improve filter")
    final = console.input("\n[cyan]Type 1 or 2 → [/cyan]").strip()
    if final == "1":
        console.print(Panel("VICTORY! You own this solution.", title="Problem Dead ✓", border_style="bold green"))
        save_history(problem, want, happy, avoid, card, answer)
        break
    elif final == "2":
        console.print(Panel("Improving filter → think harder!", style="bold red"))
        # Repeat Step 2
        want = console.input("   1. What do you really want? → ").strip() or want
        happy = console.input("   2. When you’ll be happy? → ").strip() or happy
        avoid = console.input("   3. What to be careful about? → ").strip() or avoid
        card = ask(f"Summarize into 5 short lines:\nProblem: {problem}\nWant: {want}\nDone: {happy}\nAvoid: {avoid}")
        console.print(Panel(card, title="New Clear Card", border_style="green"))
        answer = ask(f"{help_text}\n\nClear Card:\n{card}")
        console.print(Panel(answer, title="New Answer", border_style="bold green"))
    else:
        console.print("[red]Type 1 or 2 only![/red]")

console.print("[dim]Thanks for thinking first.[/dim]")