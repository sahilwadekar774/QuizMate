
import streamlit as st
from pdf_utils import extract_text_from_pdf
from gemma import generate_quiz


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="QuizMate | AI Learning Studio",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #7257E8;
    --primary-dark: #5A3FD1;
    --ink: #20213A;
    --muted: #777B91;
    --surface: #FFFFFF;
    --border: #E8E9F2;
    --soft-purple: #F2EFFF;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F7F8FC;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E8E9F2;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #20213A;
    font-weight: 700;
}

h1, h2, h3 {
    color: #20213A;
    letter-spacing: -0.6px;
}

p, label, .stMarkdown {
    color: #50546B;
}

.hero {
    background: linear-gradient(120deg, #28214F 0%, #5C46C8 55%, #8B6AF1 100%);
    padding: 34px 36px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 12px 32px rgba(74, 55, 160, 0.15);
}

.hero h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
    margin: 12px 0 8px 0;
}

.hero p {
    color: #E6E0FF;
    font-size: 15px;
    line-height: 1.7;
    max-width: 650px;
}

.eyebrow {
    color: #E6DEFF;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    color: #5F46D4;
    letter-spacing: -1px;
}

.section-label {
    color: #7257E8;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.panel {
    background: white;
    border: 1px solid #E8E9F2;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
}

.panel-title {
    color: #20213A;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 5px;
}

.panel-description {
    color: #777B91;
    font-size: 13px;
    line-height: 1.6;
}

.tip {
    background: #F2EFFF;
    border-left: 4px solid #7257E8;
    border-radius: 8px;
    padding: 13px 16px;
    color: #51418C;
    font-size: 13px;
    margin: 12px 0;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 44px;
    border: 1px solid #E1DDF8;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #7257E8, #8A6CF0);
    color: white;
    border: none;
    box-shadow: 0 5px 12px rgba(114, 87, 232, 0.18);
}

.stButton > button[kind="primary"]:hover {
    background: #5A3FD1;
    color: white;
    border: none;
}

.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

[data-testid="stFileUploader"] {
    background: #FAF9FF;
    border: 1px dashed #B8A9F4;
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E8E9F2;
    border-radius: 14px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #777B91;
}

[data-testid="stMetricValue"] {
    color: #5F46D4;
    font-weight: 800;
}

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid #E8E9F2;
    border-radius: 12px;
    margin-bottom: 10px;
}

.stRadio > div {
    gap: 10px;
}

.stProgress > div > div > div > div {
    background: #7257E8;
}

hr {
    border-color: #E8E9F2;
    margin-top: 24px;
    margin-bottom: 24px;
}

.footer {
    text-align: center;
    color: #9295A8;
    font-size: 12px;
    padding: 25px 0 5px 0;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 24px 20px;
    }

    .hero h1 {
        font-size: 28px;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "questions": [],
    "submitted": False,
    "quiz_title": "",
    "quiz_difficulty": "Medium",
    "quiz_count": 5,
    "last_error": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">✦ QuizMate</div>',
        unsafe_allow_html=True
    )
    st.caption("AI LEARNING STUDIO")
    st.divider()

    st.markdown("### ⚙️ Quiz settings")

    question_count = st.selectbox(
        "Number of questions",
        [5, 10],
        index=0
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        index=1
    )

    st.divider()

    st.markdown("### ✨ Your learning assistant")
    st.caption(
        "Turn your study notes into interactive quizzes "
        "with AI-generated questions and explanations."
    )

    st.markdown(
        """
        <div class="tip">
        <b>Privacy-first AI</b><br>
        Quiz generation uses your local Gemma model through Ollama.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Version 1.0 · QuizMate")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">YOUR PERSONAL AI STUDY PARTNER</div>
        <h1>Study smarter. Test yourself.</h1>
        <p>
            Turn your module PDFs into personalized quizzes.
            Practice at your own pace, discover what you know,
            and learn from every answer.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-label">01 — GET STARTED</div>',
    unsafe_allow_html=True
)
st.markdown("## Create your quiz")
st.markdown(
    "Upload your study material and let QuizMate prepare your practice test."
)


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

with st.container(border=True):
    st.markdown("### 📄 Upload study material")
    st.caption(
        "Supported format: PDF · For best results, use a PDF with selectable text."
    )

    uploaded_file = st.file_uploader(
        "Choose your module PDF",
        type=["pdf"],
        key="module_pdf"
    )

    if uploaded_file:
        st.success(f"Ready to use: {uploaded_file.name}")

    st.markdown(
        f"""
        <div class="tip">
        <b>Your quiz configuration</b><br>
        {question_count} questions &nbsp; · &nbsp;
        {difficulty} difficulty &nbsp; · &nbsp;
        Powered by Gemma 3 1B
        </div>
        """,
        unsafe_allow_html=True
    )

    generate_clicked = st.button(
        "✦ Generate my quiz",
        type="primary",
        use_container_width=True,
        disabled=uploaded_file is None
    )

    if generate_clicked and uploaded_file is not None:
        # Clear previous quiz and answers.
        st.session_state.questions = []
        st.session_state.submitted = False
        st.session_state.last_error = ""

        for key in list(st.session_state.keys()):
            if key.startswith("answer_"):
                del st.session_state[key]

        with st.spinner(
            "Reading your module and creating your questions..."
        ):
            module_text, pdf_error = extract_text_from_pdf(
                uploaded_file
            )

            if pdf_error:
                st.session_state.last_error = pdf_error

            elif len(module_text.strip()) < 100:
                st.session_state.last_error = (
                    "This PDF has too little readable text. "
                    "Please upload a text-based module with more content."
                )

            else:
                questions, quiz_error = generate_quiz(
                    module_text=module_text,
                    question_count=question_count,
                    difficulty=difficulty
                )

                if quiz_error:
                    st.session_state.last_error = quiz_error
                else:
                    st.session_state.questions = questions
                    st.session_state.quiz_title = uploaded_file.name
                    st.session_state.quiz_difficulty = difficulty
                    st.session_state.quiz_count = question_count

        if st.session_state.last_error:
            st.error(st.session_state.last_error)
        elif st.session_state.questions:
            st.success("Your quiz is ready!")

    if st.session_state.last_error and not generate_clicked:
        st.error(st.session_state.last_error)


# --------------------------------------------------
# QUIZ
# --------------------------------------------------

questions = st.session_state.questions

if questions:
    st.divider()

    st.markdown(
        '<div class="section-label">02 — PRACTICE TIME</div>',
        unsafe_allow_html=True
    )
    st.markdown("## Your knowledge check")

    st.caption(
        f"📘 {st.session_state.quiz_title}  ·  "
        f"{len(questions)} questions  ·  "
        f"{st.session_state.quiz_difficulty} difficulty"
    )

    with st.form("quiz_form"):
        for index, question in enumerate(questions):
            st.markdown(
                f"**Question {index + 1} of {len(questions)}**"
            )
            st.markdown(f"### {question['question']}")

            options = question["options"]

            st.radio(
                "Choose one answer",
                options=["A", "B", "C", "D"],
                format_func=lambda letter, opts=options: (
                    f"{letter}. {opts[letter]}"
                ),
                key=f"answer_{index}",
                index=None,
                label_visibility="collapsed"
            )

            if index < len(questions) - 1:
                st.divider()

        submitted = st.form_submit_button(
            "Submit my answers",
            type="primary",
            use_container_width=True
        )

    if submitted:
        st.session_state.submitted = True

    # ----------------------------------------------
    # RESULTS
    # ----------------------------------------------

    if st.session_state.submitted:
        correct_count = 0
        unanswered_count = 0

        for index, question in enumerate(questions):
            selected = st.session_state.get(f"answer_{index}")

            if selected is None:
                unanswered_count += 1
            elif selected == question["answer"]:
                correct_count += 1

        total = len(questions)
        percentage = round((correct_count / total) * 100)

        st.divider()

        st.markdown(
            '<div class="section-label">03 — YOUR PERFORMANCE</div>',
            unsafe_allow_html=True
        )
        st.markdown("## Quiz results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Your score", f"{correct_count}/{total}")
        col2.metric("Accuracy", f"{percentage}%")
        col3.metric("Not answered", unanswered_count)

        st.progress(
            percentage / 100,
            text=f"You scored {percentage}%"
        )

        if percentage == 100:
            st.balloons()
            st.success("Outstanding! You got every question correct.")
        elif percentage >= 60:
            st.success("Good work! Review the answers below to improve further.")
        else:
            st.info(
                "Keep practising. The explanations below will help you "
                "understand the material better."
            )

        st.markdown("### Review your answers")

        for index, question in enumerate(questions):
            selected = st.session_state.get(f"answer_{index}")
            correct_answer = question["answer"]

            if selected == correct_answer:
                status = "✓ Correct"
            elif selected is None:
                status = "○ Unanswered"
            else:
                status = "✕ Review"

            with st.expander(
                f"{status}  ·  Question {index + 1}"
            ):
                st.markdown(f"**{question['question']}**")

                if selected is None:
                    st.warning("You did not answer this question.")
                elif selected == correct_answer:
                    st.success(
                        f"Your answer: {selected}. "
                        f"{question['options'][selected]}"
                    )
                else:
                    st.error(
                        f"Your answer: {selected}. "
                        f"{question['options'][selected]}"
                    )

                st.markdown(
                    f"**Correct answer:** {correct_answer}. "
                    f"{question['options'][correct_answer]}"
                )

                st.markdown("**Explanation**")
                st.write(question["explanation"])

        if st.button(
            "↻ Create another quiz",
            type="primary",
            use_container_width=True
        ):
            for key in list(st.session_state.keys()):
                if key.startswith("answer_"):
                    del st.session_state[key]

            st.session_state.questions = []
            st.session_state.submitted = False
            st.session_state.quiz_title = ""
            st.session_state.last_error = ""
            st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <b>QuizMate</b> · AI-Powered Learning Studio<br>
        Built with Python, Streamlit, pypdf and Gemma
    </div>
    """,
    unsafe_allow_html=True
)
