from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import random

# =========================
# 1) QUESTIONS (TODO)
# =========================
# Structure recommandée :
# QUESTIONS_BY_LEVEL[category][difficulty] = [(question, answer), ...]
# Categories : "Culture", "Maths", "Python"
# Difficultés : "Facile", "Moyen", "Difficile"

QUESTIONS_BY_LEVEL: Dict[str, Dict[str, List[Tuple[str, str]]]] = {
    "Culture": {
        "Facile": [
            ("Capital du Maroc ?", "Rabat"),
            ("Couleur du drapeau marocain ?", "Rouge"),
        ],
        "Moyen": [
            ("Quelle mer borde le nord du Maroc ?", "Méditerranée"),
        ],
        "Difficile": [
            ("Quelle ville est surnommée la 'perle du sud' ?", "Marrakech"),
        ],
    },
    "Maths": {
        "Facile": [
            ("2 + 2 = ?", "4"),
            ("10 - 3 = ?", "7"),
        ],
        "Moyen": [
            ("12 / 3 = ?", "4"),
        ],
        "Difficile": [
            ("(5 * 3) + 2 = ?", "17"),
        ],
    },
    "Python": {
        "Facile": [
            ("En Python, une liste utilise [ ] ou ( ) ? (écris [] ou ())", "[]"),
        ],
        "Moyen": [
            ("'PYTHON'.lower() donne quoi ?", "python"),
        ],
        "Difficile": [
            ("range(5) contient combien de nombres ?", "5"),
        ],
    },
}

def normalize(text: str) -> str:
    """Nettoie un texte pour comparer facilement (TODO: ajuster si besoin)."""
    return (text or "").strip().lower()

# =========================
# 2) STATE (MÉMOIRE)
# =========================
@dataclass
class QuizState:
    category: str = "Culture"
    difficulty: str = "Facile"
    index: int = 0
    score: int = 0
    total: int = 0
    # BONUS (option) : garder une liste des erreurs
    mistakes: Optional[List[Tuple[str, str, str]]] = None  # (question, user_answer, correct_answer)

def get_questions(category: str, difficulty: str) -> List[Tuple[str, str]]:
    """Retourne la liste de questions pour une catégorie + difficulté."""
    return QUESTIONS_BY_LEVEL.get(category, {}).get(difficulty, [])

def get_badge(score: int, total: int) -> str:
    if total <= 0:
        return "—"
    if score <= total * 0.4:
        return "🥉 Bronze"
    elif score < total:
        return "🥈 Silver"
    else:
        return "🥇 Gold"

def get_progress(st: QuizState) -> Tuple[str, str]:
    """Retourne (progress_text, score_text) pour l'UI."""
    if st.total <= 0:
        return "Question 0/0", "Score : 0"
    current = min(st.index + 1, st.total)
    return f"Question {current}/{st.total}", f"Score : {st.score}"

# =========================
# 3) LOGIQUE QUIZ (TODO)
# =========================
def start_quiz(category: str, difficulty: str) -> Tuple[str, QuizState, str]:
    """
    Démarre un quiz :
    - crée un state
    - charge les questions selon category + difficulty
    - retourne (question_text, state, feedback_text)
    TODO : gérer le cas 0 question.
    """
    questions = get_questions(category, difficulty)
    st = QuizState(category=category, difficulty=difficulty, index=0, score=0, total=len(questions), mistakes=[])
    if st.total == 0:
        return "Pas de questions 😅", st, "Ajoute des questions dans utils.py"
    return questions[0][0], st, "Quiz démarré ✅"

def check_answer(user_answer: str, st: QuizState) -> Tuple[str, QuizState, str]:
    """
    Vérifie la réponse :
    - si vide: demander de répondre
    - si correcte: +1 score
    - sinon: enregistrer erreur (option)
    - avancer à la question suivante
    - si fini: retourner message final score+badge
    TODO : implémenter.
    """
    questions = get_questions(st.category, st.difficulty)
    if st.total <= 0:
        return "Pas de questions 😅", st, "Ajoute des questions dans utils.py"

    # Already finished
    if st.index >= st.total:
        return f"Quiz terminé! Score: {st.score}/{st.total} — {get_badge(st.score, st.total)}", st, "Quiz terminé 🎉"

    # Require a non-empty answer
    if not (user_answer or "").strip():
        return questions[st.index][0], st, "Veuillez entrer une réponse avant de valider."

    correct_answer = normalize(questions[st.index][1])
    given = normalize(user_answer)

    if given == correct_answer:
        st.score += 1
        feedback = "✅ Correct!"
    else:
        feedback = f"❌ Incorrect. Réponse correcte : {questions[st.index][1]}"
        if st.mistakes is None:
            st.mistakes = []
        st.mistakes.append((questions[st.index][0], user_answer, questions[st.index][1]))

    # Advance to next question
    st.index += 1

    # If finished, return final summary as the 'question' text
    if st.index >= st.total:
        return f"Quiz terminé! Score: {st.score}/{st.total} — {get_badge(st.score, st.total)}", st, feedback

    # Otherwise return next question
    return questions[st.index][0], st, feedback

def skip_question(st: QuizState) -> Tuple[str, QuizState, str]:
    """
    Skip :
    - avancer à la question suivante sans changer le score
    - si fini: message final score+badge
    TODO : implémenter.
    """
    questions = get_questions(st.category, st.difficulty)
    if st.total <= 0:
        return "Pas de questions 😅", st, "Ajoute des questions dans utils.py"

    # Already finished
    if st.index >= st.total:
        return f"Quiz terminé! Score: {st.score}/{st.total} — {get_badge(st.score, st.total)}", st, "Quiz terminé 🎉"

    # Move to next question without changing score
    st.index += 1
    feedback = "⏭️ Question passée"

    if st.index >= st.total:
        return f"Quiz terminé! Score: {st.score}/{st.total} — {get_badge(st.score, st.total)}", st, feedback

    return questions[st.index][0], st, feedback

def restart_quiz(st: QuizState) -> Tuple[str, QuizState, str]:
    """Recommencer le quiz avec la même catégorie/difficulté."""
    return start_quiz(st.category, st.difficulty)


def get_random_category_difficulty() -> Tuple[str, str]:
    """Retourne un couple (category, difficulty) choisi aléatoirement
    à partir de `QUESTIONS_BY_LEVEL`.
    """
    categories = list(QUESTIONS_BY_LEVEL.keys())
    if not categories:
        return "Culture", "Facile"
    category = random.choice(categories)
    difficulties = list(QUESTIONS_BY_LEVEL.get(category, {}).keys())
    difficulty = random.choice(difficulties) if difficulties else "Facile"
    return category, difficulty
