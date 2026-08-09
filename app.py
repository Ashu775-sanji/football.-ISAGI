"""
app.py
------
Main entry point — ab ek polished, professional-looking interface ke saath.
Run karne ke liye:
    streamlit run app.py
"""

import streamlit as st

from predictor import MatchPredictor
from players import get_all_teams, get_players_by_team
from helpers import extract_teams_from_text, format_prediction_response
from styles import (
    get_team_color,
    inject_custom_css,
    render_hero,
    render_player_card,
    render_prob_bar,
    render_team_badge,
)

st.set_page_config(
    page_title="Football Predictor AI",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
predictor = MatchPredictor()

# ---------- Sidebar: team & player browser ----------
with st.sidebar:
    st.markdown("### 📋 Squad browser")
    selected_team = st.selectbox("Select a team", get_all_teams())
    players = get_players_by_team(selected_team)
    for name, info in sorted(players.items(), key=lambda x: -x[1]["rating"]):
        render_player_card(name, info)

    st.divider()
    st.caption("Made by Ashu · Python + Streamlit")

# ---------- Hero ----------
render_hero()

tab1, tab2 = st.tabs(["🔮 Match Predictor", "💬 Chat Mode"])

# ---------- TAB 1: Visual match predictor ----------
with tab1:
    col_a, col_vs, col_b = st.columns([5, 1, 5])

    all_teams = get_all_teams()
    with col_a:
        team_a = st.selectbox("Home team", all_teams, index=0, key="pick_a")
        render_team_badge(team_a)

    with col_vs:
        st.markdown(
            "<div style='text-align:center; font-size:1.8rem; font-weight:700; padding-top:2.2rem;'>VS</div>",
            unsafe_allow_html=True,
        )

    with col_b:
        default_b_index = 1 if all_teams[0] == team_a else 0
        team_b = st.selectbox(
            "Away team",
            [t for t in all_teams if t != team_a],
            index=default_b_index,
            key="pick_b",
        )
        render_team_badge(team_b)

    st.write("")
    predict_clicked = st.button("🔮 Predict this match", use_container_width=True, type="primary")

    if predict_clicked:
        result = predictor.predict_match(team_a, team_b, home_team=team_a)

        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown('<div class="match-card">', unsafe_allow_html=True)

            st.markdown(
                f'<div class="score-display">{result["predicted_score"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="text-align:center; margin-bottom:1rem;">'
                f'<span class="motm-badge">🌟 Man of the Match: {result["man_of_the_match"]}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )

            render_prob_bar(f"{team_a} win", result["win_prob_a"], get_team_color(team_a))
            render_prob_bar("Draw", result["draw_prob"], "#9e9e9e")
            render_prob_bar(f"{team_b} win", result["win_prob_b"], get_team_color(team_b))

            st.markdown("</div>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.metric(
                    label=f"{team_a} strength",
                    value=result["strength_a"]["strength"],
                    delta=f"Star: {result['strength_a']['top_player']}",
                )
            with c2:
                st.metric(
                    label=f"{team_b} strength",
                    value=result["strength_b"]["strength"],
                    delta=f"Star: {result['strength_b']['top_player']}",
                )

            if result["win_prob_a"] > 60 or result["win_prob_b"] > 60:
                st.balloons()

# ---------- TAB 2: Chatbot mode ----------
with tab2:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown("Type something like: *'Real Madrid vs Barcelona kaun jeetega?'*")

    for msg in st.session_state.messages:
        bubble_class = "bubble-user" if msg["role"] == "user" else "bubble-bot"
        st.markdown(f'<div class="{bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask about any match...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        teams_found = extract_teams_from_text(user_input)

        if len(teams_found) == 2:
            result = predictor.predict_match(teams_found[0], teams_found[1])
            reply = format_prediction_response(result)
        elif len(teams_found) == 1:
            reply = (
                f"Sirf ek team mili: <b>{teams_found[0]}</b>. Do team names bhejo predict karne ke liye."
            )
        else:
            reply = "Team samajh nahi aayi 🤔. Available teams: " + ", ".join(get_all_teams())

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
