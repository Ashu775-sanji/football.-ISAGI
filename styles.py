"""
utils/styles.py
----------------
Yahan saara custom styling (CSS) aur reusable UI-building functions hain,
taaki app.py saaf-suthra rahe. Streamlit khud thoda plain UI deta hai,
isliye hum custom HTML/CSS inject karte hain "st.markdown(..., unsafe_allow_html=True)"
ke through — isse app professional dikhti hai.
"""

import streamlit as st

# Har team ko ek color diya hai (jersey-inspired), taaki UI me
# consistently wahi color use ho — cards, badges, probability bars sab me.
TEAM_COLORS = {
    "Real Madrid": "#5E72EB",
    "Barcelona": "#A50044",
    "Manchester City": "#6CABDD",
    "Al-Nassr": "#FFD700",
    "Inter Miami": "#F7B5CD",
    "Liverpool": "#C8102E",
    "Bayern Munich": "#DC052D",
    "Manchester United": "#DA291C",
    "Arsenal": "#EF0107",
    "Al-Hilal": "#1E56A0",
}


def get_team_color(team_name: str) -> str:
    return TEAM_COLORS.get(team_name, "#7F77DD")


def inject_custom_css():
    """Ek baar app ke start me call karo — poori app ka look badal deta hai."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        /* Hero banner */
        .hero {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #0f2027 100%);
            padding: 2rem 2rem 1.6rem 2rem;
            border-radius: 18px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 24px rgba(15, 32, 39, 0.35);
        }
        .hero h1 {
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 4px 0;
        }
        .hero p {
            font-size: 0.95rem;
            opacity: 0.85;
            margin: 0;
        }

        /* Team badge / avatar circle */
        .team-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 54px;
            height: 54px;
            border-radius: 50%;
            font-weight: 700;
            font-size: 1.1rem;
            color: white;
            margin-bottom: 6px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.25);
        }

        /* Match preview card */
        .match-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 1.4rem;
            margin-bottom: 1rem;
        }

        /* Probability bar */
        .prob-row {
            margin: 10px 0;
        }
        .prob-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .prob-track {
            width: 100%;
            height: 12px;
            border-radius: 8px;
            background: rgba(255,255,255,0.08);
            overflow: hidden;
        }
        .prob-fill {
            height: 100%;
            border-radius: 8px;
            transition: width 0.6s ease;
        }

        /* Scoreline */
        .score-display {
            text-align: center;
            font-size: 2.4rem;
            font-weight: 700;
            letter-spacing: 2px;
            margin: 0.5rem 0;
        }

        /* MOTM badge */
        .motm-badge {
            display: inline-block;
            background: linear-gradient(90deg, #f7b733, #fc4a1a);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        /* Player mini card */
        .player-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 8px;
        }
        .player-card .name {
            font-weight: 600;
            font-size: 0.9rem;
        }
        .player-card .meta {
            font-size: 0.75rem;
            opacity: 0.7;
        }

        /* Chat bubbles */
        .bubble-user {
            background: linear-gradient(135deg, #2a5298, #1e3c72);
            color: white;
            padding: 10px 16px;
            border-radius: 16px 16px 4px 16px;
            max-width: 80%;
            margin-left: auto;
            margin-bottom: 8px;
        }
        .bubble-bot {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 10px 16px;
            border-radius: 16px 16px 16px 4px;
            max-width: 80%;
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="hero">
            <h1>⚽ Football Predictor AI</h1>
            <p>Player-rating based match predictions with a touch of real-world unpredictability</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_team_badge(team_name: str, size_label: str = ""):
    color = get_team_color(team_name)
    initials = "".join(w[0] for w in team_name.split()[:2]).upper()
    st.markdown(
        f"""
        <div style="text-align:center;">
            <div class="team-badge" style="background:{color};">{initials}</div>
            <div style="font-weight:600; font-size:0.9rem;">{team_name}</div>
            <div style="font-size:0.75rem; opacity:0.65;">{size_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prob_bar(label: str, percent: float, color: str):
    st.markdown(
        f"""
        <div class="prob-row">
            <div class="prob-label"><span>{label}</span><span>{percent}%</span></div>
            <div class="prob-track">
                <div class="prob-fill" style="width:{percent}%; background:{color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_player_card(name: str, info: dict):
    st.markdown(
        f"""
        <div class="player-card">
            <div class="name">{name}</div>
            <div class="meta">{info['position']} · Rating {info['rating']} · {info['team']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
