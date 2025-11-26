# ClearCut

**Think first. Answer second.**

Open-source terminal tool that forces you to clarify any problem before AI helps.

- No blank screen — AI suggests perfect 3-line filter  
- Press **Enter** to accept suggestions instantly  
- Only 2 final choices: “Solved” or “Improve filter”  
- Uses free Groq + Llama-3.3 70B  
- First run asks for API key → saved forever  

### Run in 30 seconds

```bash
git clone https://github.com/aadityamahajn/clearcut.git
cd clearcut
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
python clearcut.py