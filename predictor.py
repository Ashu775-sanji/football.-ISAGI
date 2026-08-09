"""
core/predictor.py
------------------
Yeh humara MAIN prediction engine hai.

Approach: "Rule-based + Randomness"
    1. Rule-based part -> team strength (players ki rating/form se)
       decide karti hai ki kaun favourite hai.
    2. Randomness part -> asli football me upsets hote rehte hain
       (weak team bhi kabhi kabhi jeet jaati hai), isliye hum har
       strength difference par ek "luck factor" add karte hain.

Isse output har baar thoda different aata hai, jaise real match
predictions/betting odds behave karte hain.
"""

import random

from teams import calculate_team_strength


class MatchPredictor:
    def __init__(self, home_advantage: float = 3.0):
        # Home advantage -> ghar pe khelne waali team ko chhota sa bonus
        self.home_advantage = home_advantage

    def predict_match(self, team_a: str, team_b: str, home_team: str | None = None):
        """
        Do teams ke beech match predict karta hai.

        Returns dict with:
            win_prob_a, win_prob_b, draw_prob (%),
            predicted_score "2-1" style,
            man_of_the_match,
            summary text
        """
        seed = random.randint(0, 999999)  # har call par fresh randomness
        strength_a = calculate_team_strength(team_a, seed=seed)
        strength_b = calculate_team_strength(team_b, seed=seed + 1)

        if strength_a["player_count"] == 0 or strength_b["player_count"] == 0:
            return {"error": "Ek ya dono teams ka data nahi mila. Team name check karo."}

        score_a = strength_a["strength"]
        score_b = strength_b["strength"]

        # Home advantage apply karo
        if home_team and home_team.lower() == team_a.lower():
            score_a += self.home_advantage
        elif home_team and home_team.lower() == team_b.lower():
            score_b += self.home_advantage

        # ---- RULE-BASED PART: strength difference se base probability ----
        diff = score_a - score_b
        # Sigmoid-jaisa curve -> difference jitna zyada, favourite ki
        # jeetne ki probability utni zyada (but kabhi 100% nahi hoti)
        base_prob_a = 1 / (1 + pow(2.71828, -diff / 8))

        # ---- RANDOMNESS PART: upset factor (real matches unpredictable hote hain) ----
        upset_swing = random.uniform(-0.15, 0.15)
        prob_a = min(max(base_prob_a + upset_swing, 0.05), 0.90)

        # Draw probability -> teams jitni close hoti hain utna zyada draw chance
        closeness = 1 - abs(prob_a - 0.5) * 2
        draw_prob = 0.15 + (closeness * 0.15)

        prob_b = 1 - prob_a - draw_prob
        if prob_b < 0:
            prob_b = 0.05
            draw_prob = 1 - prob_a - prob_b

        # ---- Scoreline simulation (simple random goals weighted by strength) ----
        goals_a = self._simulate_goals(score_a)
        goals_b = self._simulate_goals(score_b)

        # Agar winner probability se scoreline match nahi karti, thoda adjust karo
        winner = max(
            [("a", prob_a), ("b", prob_b), ("draw", draw_prob)],
            key=lambda x: x[1],
        )[0]
        if winner == "a" and goals_a <= goals_b:
            goals_a = goals_b + 1
        elif winner == "b" and goals_b <= goals_a:
            goals_b = goals_a + 1
        elif winner == "draw":
            goals_b = goals_a

        motm = strength_a["top_player"] if goals_a >= goals_b else strength_b["top_player"]

        return {
            "team_a": team_a,
            "team_b": team_b,
            "win_prob_a": round(prob_a * 100, 1),
            "win_prob_b": round(prob_b * 100, 1),
            "draw_prob": round(draw_prob * 100, 1),
            "predicted_score": f"{goals_a} - {goals_b}",
            "man_of_the_match": motm,
            "strength_a": strength_a,
            "strength_b": strength_b,
        }

    @staticmethod
    def _simulate_goals(strength: float) -> int:
        """
        Team strength ko lambda (average goals) me convert karke
        Poisson-jaisi random distribution se goals nikalta hai.
        Simple version — asli Poisson formula use nahi kiya, taaki
        beginner ko samajhna easy rahe.
        """
        avg_goals = max(0.5, (strength - 60) / 15)  # strength 60-100 -> 0 se 2.5 goals
        goals = round(random.gauss(avg_goals, 0.9))
        return max(0, goals)
