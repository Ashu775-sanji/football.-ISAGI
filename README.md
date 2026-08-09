# ⚽ Football Team Predictor Chatbot

Pure-Python chatbot jo do football teams ke naam lekar match outcome
predict karta hai — player ratings + form (rule-based) aur thoda
randomness (real match jaisa unpredictable feel) combine karke.

## 📁 Project Structure

```
football_predictor/
├── app.py                 # Streamlit chatbot UI (entry point)
├── data/
│   ├── __init__.py
│   └── players.py         # Player "database" (Messi, Ronaldo, Haaland, etc.)
├── core/
│   ├── __init__.py
│   ├── teams.py           # Team strength calculation
│   └── predictor.py        # Match prediction engine (rules + randomness)
├── utils/
│   ├── __init__.py
│   ├── helpers.py          # Chat parsing + response formatting
│   └── styles.py           # Custom CSS + UI components (badges, probability bars, cards)
├── requirements.txt
└── README.md
```

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Browser me `http://localhost:8501` khul jayega.

## 💬 Kaise use karein

App ke andar do modes hain (top pe tabs milenge):

- **🔮 Match Predictor tab** — Home aur Away team select karo, team badges dikhenge,
  "Predict this match" dabao — animated probability bars, scoreline, aur
  Man of the Match badge dikhega. Agar koi team 60%+ favourite ho to confetti bhi chalega! 🎉
- **💬 Chat Mode tab** — normal chatbot jaisa, type karo `"Real Madrid vs Barcelona kaun jeetega?"`
- Sidebar me kisi bhi team ke players card-style me dikhte hain (rating ke hisaab se sorted).

## 🧠 Prediction Logic (kaise kaam karta hai)

1. **Team Strength** — har team ki strength uske players ki
   `rating` (60%) aur random `form` (40%) se calculate hoti hai.
2. **Rule-based probability** — strength difference se base win %
   nikalta hai (jo team strong hai uska chance zyada).
3. **Randomness / Upset factor** — ±15% ka random swing add hota hai,
   taaki weak team bhi kabhi upset kar sake — real football jaisa!
4. **Scoreline simulation** — random goals generate hote hain jo
   team ki strength ke around hote hain.

## 🗺️ Roadmap (aage kya add kar sakte ho)

- [x] Step 1: Player database (ratings, teams, positions)
- [x] Step 2: Team strength calculation
- [x] Step 3: Rule-based + random prediction engine
- [x] Step 4: Streamlit chatbot interface
- [ ] Step 5: Real player data ko live API (e.g. football-data.org) se fetch karna
- [ ] Step 6: Head-to-head history factor add karna
- [ ] Step 7: Real NLP (LLM) se chat understanding better banana
- [ ] Step 8: Match simulation ko minute-by-minute commentary jaisa banana
- [ ] Step 9: Save predictions history (SQLite database)
- [ ] Step 10: Deploy on Streamlit Cloud / Hugging Face Spaces

## ➕ Naye players/teams add kaise karein

`data/players.py` me `PLAYERS` dictionary me bas ek naya entry add karo:

```python
"Neuer Kimmich": {
    "team": "Bayern Munich",
    "position": "MID",
    "rating": 85,
    "pace": 70,
    "shooting": 75,
    "passing": 88,
},
```
Bas — baaki sab (team list, sidebar, prediction) automatically update ho jaayega.
