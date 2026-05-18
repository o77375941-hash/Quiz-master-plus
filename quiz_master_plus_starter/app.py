import gradio as gr
from utils import start_quiz, check_answer, skip_question, restart_quiz, get_progress, QuizState # type: ignore # type ignore

# =========================
# Quiz Master Plus — UI (Gradio)
# =========================

with gr.Blocks(title="Quiz Master Plus") as demo:
    gr.Markdown("# 🎮 Quiz Master Plus\n### Capstone Starter (AI Creators)")

    # --- Sélecteurs ---
    with gr.Row():
        category_dd = gr.Dropdown(["Culture", "Maths", "Python"], value="Culture", label="Catégorie")
        difficulty_dd = gr.Dropdown(["Facile", "Moyen", "Difficile"], value="Facile", label="Difficulté")

    # --- State ---
    state = gr.State(QuizState())

    # --- Affichages ---
    question_box = gr.Textbox(label="Question", interactive=False)
    answer_box = gr.Textbox(label="Ta réponse", placeholder="Écris ta réponse ici...")
    feedback_box = gr.Textbox(label="Feedback", interactive=False)

    with gr.Row():
        progress_box = gr.Textbox(label="Progression", interactive=False)
        score_box = gr.Textbox(label="Score", interactive=False)

    # --- Boutons ---
    with gr.Row():
        start_btn = gr.Button("▶️ Démarrer")
        submit_btn = gr.Button("✅ Valider")
        skip_btn = gr.Button("⏭️ Skip")
        restart_btn = gr.Button("🔄 Recommencer")

    # =========================
    # Callbacks
    # =========================
    def on_start(category, difficulty): # type: ignore # pyright: ignore[reportUnknownParameterType] # type: ignore  # type : ignore 
        q, st, fb = start_quiz(category, difficulty) # type: ignore
        progress, score = get_progress(st) # type: ignore
        return q, "", fb, progress, score, st # type: ignore # type : ignore 

    def on_submit(answer, st): # type: ignore
        q, st, fb = check_answer(answer, st) # type: ignore
        progress, score = get_progress(st) # type: ignore
        return q, "", fb, progress, score, st # type: ignore

    def on_skip(st): # type: ignore
        q, st, fb = skip_question(st) # type: ignore
        progress, score = get_progress(st) # type: ignore
        return q, "", fb, progress, score, st # type: ignore

    def on_restart(st): # type: ignore
        q, st, fb = restart_quiz(st) # type: ignore
        progress, score = get_progress(st) # type: ignore
        return q, "", fb, progress, score, st # type: ignore

    # --- Wiring ---
    start_btn.click(on_start, inputs=[category_dd, difficulty_dd], # type: ignore
                    outputs=[question_box, answer_box, feedback_box, progress_box, score_box, state])

    submit_btn.click(on_submit, inputs=[answer_box, state], # type: ignore
                     outputs=[question_box, answer_box, feedback_box, progress_box, score_box, state])

    skip_btn.click(on_skip, inputs=[state], # type: ignore
                   outputs=[question_box, answer_box, feedback_box, progress_box, score_box, state])

    restart_btn.click(on_restart, inputs=[state], # type: ignore
                      outputs=[question_box, answer_box, feedback_box, progress_box, score_box, state])

demo.launch()
