
import json
import ollama

MODEL_NAME = "gemma3:1b"


def generate_quiz(module_text, question_count=5, difficulty="Medium"):
    """Generate and validate MCQs using the local Gemma model."""

    # Keep the input shorter so the small model can focus on generating questions.
    study_text = module_text[:6000]

    prompt = f"""
Create exactly {question_count} multiple-choice quiz questions
from the study material below.

Difficulty: {difficulty}

Return a JSON object with this exact structure:
{{
  "questions": [
    {{
      "question": "What is ...?",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "answer": "A",
      "explanation": "Why A is correct."
    }}
  ]
}}

Rules:
- Generate exactly {question_count} questions.
- Every question must have four meaningful options: A, B, C, D.
- The answer must be one letter: A, B, C, or D.
- Give a short explanation for each answer.
- Base questions only on the supplied study material.
- Do not return an empty questions list.
- Return only valid JSON, without Markdown fences.

STUDY MATERIAL:
{study_text}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            format="json",
            options={
                "temperature": 0.1,
                "num_predict": 2048
            }
        )

        response_text = response["message"]["content"].strip()

        # Parse the JSON response.
        data = json.loads(response_text)

        questions = data.get("questions", [])

        if not isinstance(questions, list) or len(questions) == 0:
            return None, (
                "Gemma returned an empty quiz. "
                "Try a shorter PDF or generate the quiz again."
            )

        valid_questions = []

        for question in questions:
            if not isinstance(question, dict):
                continue

            options = question.get("options")
            answer = question.get("answer")

            if not isinstance(options, dict):
                continue

            # Ensure the options have the required keys.
            if not all(
                key in options and isinstance(options[key], str)
                and options[key].strip()
                for key in ["A", "B", "C", "D"]
            ):
                continue

            if answer not in ["A", "B", "C", "D"]:
                continue

            if not question.get("question"):
                continue

            if not question.get("explanation"):
                question["explanation"] = (
                    f"The correct answer is {answer}: "
                    f"{options[answer]}"
                )

            valid_questions.append({
                "question": str(question["question"]),
                "options": {
                    key: options[key].strip()
                    for key in ["A", "B", "C", "D"]
                },
                "answer": answer,
                "explanation": str(question["explanation"])
            })

        # Don't silently show a quiz with too few questions.
        if len(valid_questions) < question_count:
            return None, (
                f"Gemma generated {len(valid_questions)} valid questions "
                f"out of {question_count} requested. "
                "Please click Generate Quiz again."
            )

        return valid_questions[:question_count], None

    except json.JSONDecodeError:
        return None, (
            "Gemma returned an unreadable JSON response. "
            "Please try again."
        )

    except ollama.ResponseError as error:
        return None, f"Ollama model error: {error}"

    except Exception as error:
        return None, (
            f"Quiz generation failed: {error}. "
            "Check that Ollama is running and Gemma is installed."
        )
