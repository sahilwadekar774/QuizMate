# QuizMate — AI-Powered Module Quiz Generator

QuizMate is a Python-based web application that uses local AI to generate multiple-choice questions (MCQs) from uploaded PDF study materials. Students can take interactive quizzes, check their scores, and review explanations for the correct answers.

## Features

- **PDF Text Extraction:** Extracts readable text from uploaded PDF files.
- **AI Quiz Generation:** Uses the Gemma 3 1B model through Ollama to generate MCQs locally.
- **Customizable Quizzes:** Choose the number of questions and difficulty level.
- **Interactive Interface:** Select answers and submit your quiz.
- **Automatic Evaluation:** Displays scores, percentages, and unanswered questions.
- **Answer Explanations:** Review the correct answers and explanations.
- **Local AI Processing:** Uses a locally running language model.

## Technologies Used

- Python
- Streamlit
- Ollama
- Gemma 3 1B
- pypdf

## Requirements

- Python installed on your computer
- Git
- Ollama
- The Gemma 3 1B model

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd QuizMate
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment on Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Install Ollama and download the model

Install Ollama from https://ollama.com/ and run:

```bash
ollama pull gemma3:1b
```

### 6. Start the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## How to Use

1. Launch QuizMate.
2. Upload a PDF containing your study material.
3. Select your preferred quiz settings.
4. Click **Generate Quiz**.
5. Answer the questions and submit the quiz.
6. Review your score and answer explanations.

## Project Structure

```text
QuizMate/
├── app.py
├── gemma.py
├── pdf_utils.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Note

QuizMate requires Ollama and the Gemma model to be installed locally. The quality of generated questions depends on the readable content of the uploaded PDF and the AI model's response.

## Future Improvements

- Export quizzes to PDF.
- Save quiz history and performance.
- Support additional AI models.
- Add more question formats.

---
**QuizMate — Turn your study material into interactive quizzes.**