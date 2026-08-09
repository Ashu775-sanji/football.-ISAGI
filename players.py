"""
data/players.py
----------------
Yeh file humara "database" hai — sab players ki info yahan stored hai.
Real DB (SQLite/MySQL) ki jagah abhi Python dictionary use kar rahe hain,
taaki beginner-friendly rahe. Baad me isko easily DB me convert kar sakte ho.

Har player ka structure:
{
    "team": str,          -> player kis team ke liye khelta hai
    "position": str,      -> FWD / MID / DEF / GK
    "rating": int,        -> overall skill rating (0-99, FIFA/FC style)
    "pace": int,
    "shooting": int,
    "passing": int,
    "form": int           -> recent match form (0-99), thoda random rakha
                             hai taaki har prediction thoda alag lage
}
"""

import random

# Base player database (aap yahan aur players add kar sakte ho)
PLAYERS = {
    "Lionel Messi": {
        "team": "Inter Miami",
        "position": "FWD",
        "rating": 90,
        "pace": 80,
        "shooting": 88,
        "passing": 91,
    },
    "Cristiano Ronaldo": {
        "team": "Al-Nassr",
        "position": "FWD",
        "rating": 88,
        "pace": 78,
        "shooting": 92,
        "passing": 80,
    },
    "Erling Haaland": {
        "team": "Manchester City",
        "position": "FWD",
        "rating": 91,
        "pace": 88,
        "shooting": 93,
        "passing": 70,
    },
    "Kevin De Bruyne": {
        "team": "Manchester City",
        "position": "MID",
        "rating": 89,
        "pace": 74,
        "shooting": 82,
        "passing": 93,
    },
    "Kylian Mbappe": {
        "team": "Real Madrid",
        "position": "FWD",
        "rating": 91,
        "pace": 97,
        "shooting": 89,
        "passing": 80,
    },
    "Vinicius Jr": {
        "team": "Real Madrid",
        "position": "FWD",
        "rating": 89,
        "pace": 95,
        "shooting": 84,
        "passing": 82,
    },
    "Jude Bellingham": {
        "team": "Real Madrid",
        "position": "MID",
        "rating": 90,
        "pace": 80,
        "shooting": 86,
        "passing": 86,
    },
    "Robert Lewandowski": {
        "team": "Barcelona",
        "position": "FWD",
        "rating": 89,
        "pace": 75,
        "shooting": 91,
        "passing": 79,
    },
    "Pedri": {
        "team": "Barcelona",
        "position": "MID",
        "rating": 87,
        "pace": 75,
        "shooting": 76,
        "passing": 90,
    },
    "Mohamed Salah": {
        "team": "Liverpool",
        "position": "FWD",
        "rating": 89,
        "pace": 90,
        "shooting": 89,
        "passing": 82,
    },
    "Virgil van Dijk": {
        "team": "Liverpool",
        "position": "DEF",
        "rating": 89,
        "pace": 78,
        "shooting": 60,
        "passing": 78,
    },
    "Harry Kane": {
        "team": "Bayern Munich",
        "position": "FWD",
        "rating": 90,
        "pace": 70,
        "shooting": 91,
        "passing": 83,
    },
    "Jamal Musiala": {
        "team": "Bayern Munich",
        "position": "MID",
        "rating": 87,
        "pace": 85,
        "shooting": 82,
        "passing": 85,
    },
    "Bruno Fernandes": {
        "team": "Manchester United",
        "position": "MID",
        "rating": 87,
        "pace": 72,
        "shooting": 84,
        "passing": 88,
    },
    "Marcus Rashford": {
        "team": "Manchester United",
        "position": "FWD",
        "rating": 84,
        "pace": 93,
        "shooting": 82,
        "passing": 76,
    },
    "Bukayo Saka": {
        "team": "Arsenal",
        "position": "FWD",
        "rating": 87,
        "pace": 87,
        "shooting": 82,
        "passing": 83,
    },
    "Martin Odegaard": {
        "team": "Arsenal",
        "position": "MID",
        "rating": 87,
        "pace": 75,
        "shooting": 81,
        "passing": 88,
    },
    "Neymar Jr": {
        "team": "Al-Hilal",
        "position": "FWD",
        "rating": 87,
        "pace": 84,
        "shooting": 83,
        "passing": 87,
    },
}


def get_all_teams():
    """Sabhi unique team names ki list return karta hai."""
    return sorted({info["team"] for info in PLAYERS.values()})


def get_players_by_team(team_name: str):
    """Ek team ke sab players ka dict return karta hai (case-insensitive match)."""
    return {
        name: info
        for name, info in PLAYERS.items()
        if info["team"].lower() == team_name.lower()
    }


def get_team_form(team_name: str, seed: int | None = None):
    """
    Team ke har player ko ek random 'current form' number deta hai (85-100%).
    Yeh isliye taaki same team ka prediction har baar thoda different
    aa sake — real football me bhi form roz change hoti hai.
    """
    rng = random.Random(seed)
    players = get_players_by_team(team_name)
    return {name: rng.randint(85, 100) for name in players}
