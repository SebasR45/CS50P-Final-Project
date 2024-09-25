import pytest
from project import fetch_trivia_questions, ask_question, check_answer

def test_fetch_trivia_questions():
    questions = fetch_trivia_questions(9, 'medium')  # Using category ID 9 and medium difficulty for testing
    assert len(questions) > 0
    assert isinstance(questions, list)
    assert "question" in questions[0]
    assert "correct_answer" in questions[0]
    assert "incorrect_answers" in questions[0]

def test_ask_question():
    question = {
        "question": "Who played Baron Victor Frankestein in the 1957 Hammer horror film &quot;The Curse of Frankenstein&quot;?",
        "correct_answer": "Peter Cushing",
        "incorrect_answers": ["Boris Karloff", "Vincent Price", "Lon Chaney Jr."]
    }
    options = ask_question(question)
    assert len(options) == 4
    assert "Peter Cushing" in options
    assert "Boris Karloff" in options
    assert "&quot;" not in options
    assert "&#039;" not in options

def test_check_answer():
    question = {
        "question": "Who played Baron Victor Frankestein in the 1957 Hammer horror film &quot;The Curse of Frankenstein&quot;?",
        "correct_answer": "Peter Cushing",
        "incorrect_answers": ["Boris Karloff", "Vincent Price", "Lon Chaney Jr."]
    }
    assert check_answer(question, "Peter Cushing") == True
    assert check_answer(question, "Boris Karloff") == False
