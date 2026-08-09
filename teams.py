"""
core/teams.py
-------------
Yeh module individual players ki rating ko combine karke
ek "team strength score" banata hai. Match predictor isi score
ko use karega.
"""

from players import get_players_by_team, get_team_form


def calculate_team_strength(team_name: str, seed: int | None = None) -> dict:
    """
    Team ka overall strength calculate karta hai.

    Formula (simple weighted average):
        strength = (avg_rating * 0.6) + (avg_form * 0.4)

    Return karta hai:
        {
            "team": team_name,
            "strength": float,   # 0-100 ke beech
            "top_player": str,   # highest rated player (star player)
            "player_count": int
        }
    """
    players = get_players_by_team(team_name)

    if not players:
        return {
            "team": team_name,
            "strength": 0.0,
            "top_player": None,
            "player_count": 0,
        }

    form = get_team_form(team_name, seed=seed)

    avg_rating = sum(p["rating"] for p in players.values()) / len(players)
    avg_form = sum(form.values()) / len(form)

    # Weighted combination -> rating zyada matter karti hai, form thoda kam
    strength = (avg_rating * 0.6) + (avg_form * 0.4)

    top_player = max(players.items(), key=lambda item: item[1]["rating"])[0]

    return {
        "team": team_name,
        "strength": round(strength, 2),
        "top_player": top_player,
        "player_count": len(players),
    }
