"""
utils/helpers.py
-----------------
Chatbot ke "language understanding" aur "response formatting" wala part.
Real NLP model nahi use kar rahe (keep it simple) — bas keyword matching
se user ke message me se team names dhoondte hain.
"""

from players import get_all_teams


def extract_teams_from_text(text: str):
    """
    User ke message me se do team names dhoondhta hai.
    Example: "who wins between Real Madrid and Barcelona"
             -> ["Real Madrid", "Barcelona"]
    """
    text_lower = text.lower()
    found = [team for team in get_all_teams() if team.lower() in text_lower]
    return found[:2]  # sirf pehli 2 teams lo agar zyada mil jaayein


def format_prediction_response(result: dict) -> str:
    """Prediction dict ko ek friendly chat message me convert karta hai."""
    if "error" in result:
        return f"⚠️ {result['error']}"

    return (
        f"**{result['team_a']} vs {result['team_b']}**\n\n"
        f"🔵 {result['team_a']} win chance: **{result['win_prob_a']}%**\n"
        f"🔴 {result['team_b']} win chance: **{result['win_prob_b']}%**\n"
        f"⚪ Draw chance: **{result['draw_prob']}%**\n\n"
        f"⚽ Predicted Score: **{result['predicted_score']}**\n"
        f"🌟 Man of the Match (predicted): **{result['man_of_the_match']}**"
    )


def welcome_message() -> str:
    teams = ", ".join(get_all_teams())
    return (
        "👋 Hi! Main tumhara Football Match Predictor Chatbot hoon.\n\n"
        "Bas mujhe do team names bhejo, jaise: *'Real Madrid vs Barcelona kaun jeetega?'*\n\n"
        f"**Available teams:** {teams}"
    )
