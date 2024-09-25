import random
import requests

def main():
    """Main function to run the Trivia Game.

    This function welcomes the user, fetches trivia questions,
    and starts the game. It also displays the final score.

    Returns:
        None
    """
    print("Welcome to the Trivia Game!")
    player_name = input("Enter your name: ")
    questions = fetch_trivia_questions()
    score = play_game(questions)
    print(f"\n{player_name}, your final score is: {score}")


def fetch_trivia_questions():
    """Fetches trivia questions from an external API.

    This function retrieves 10 trivia questions of medium
    difficulty from the Open Trivia Database.

    Raises:
        HTTPError: If the API request fails.

    Returns:
        list: A list of trivia questions.
    """
    url = "https://opentdb.com/api.php?amount=10&category=11&difficulty=medium&type=multiple"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        print("Failed to fetch trivia questions.")
        return []


def ask_question(question):
    """Displays a trivia question and its possible answers.

    This function takes a trivia question, formats it by replacing
    HTML entities, and shuffles the answer options before displaying
    them.

    Parameters:
        question (dict): The trivia question containing the question text,
                         correct answer, and incorrect answers.

    Raises:
        ValueError: If the question format is invalid.

    Returns:
        list: A list of shuffled answer options including the correct answer.
    """
    QUOTE_ENTITY = "&quot;"
    APOSTROPHE_ENTITY = "&#039;"
    
    question['question'] = question['question'].replace(QUOTE_ENTITY, '"').replace(APOSTROPHE_ENTITY, "'")
    question["correct_answer"] = question["correct_answer"].replace(QUOTE_ENTITY, '"').replace(APOSTROPHE_ENTITY, "'")
    question["incorrect_answers"] = [answer.replace(QUOTE_ENTITY, '"').replace(APOSTROPHE_ENTITY, "'") for answer in question["incorrect_answers"]]

    print("\n" + question["question"])
    options = question["incorrect_answers"]
    options.append(question["correct_answer"])
    random.shuffle(options)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    return options


def check_answer(question, user_answer):
    """Checks if the user's answer is correct.

    This function compares the user's answer to the correct answer
    of the trivia question.

    Parameters:
        question (dict): The trivia question containing the correct answer.
        user_answer (str): The answer provided by the user.

    Returns:
        bool: True if the answer is correct, False otherwise.
    """
    correct_answer = question["correct_answer"]
    return correct_answer == user_answer


def play_game(questions):
    """Runs the trivia game, asking questions and scoring answers.

    This function iterates through the list of trivia questions,
    asks each question to the user, and tracks their score.

    Parameters:
        questions (list): A list of trivia questions.

    Returns:
        int: The final score of the user.
    """
    score = 0

    for i, question in enumerate(questions):
        print(f"\nQuestion {i + 1}:")
        options = ask_question(question)
        try:
            answer_index = int(input("Your answer (1-4): ")) - 1
            user_answer = options[answer_index]
        except (ValueError, IndexError):
            print("Invalid answer. Moving to the next question.")
            continue
        if check_answer(question, user_answer):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {question['correct_answer']}")
    return score


if __name__ == "__main__":
    main()
