import random
import requests
import json

def main():
    """Main function to run the Trivia Game.

    This function welcomes the user, fetches trivia questions,
    and starts the game. It also displays the final score.

    Returns:
        None
    """
    print("Welcome to the Trivia Game!")
    player_name = input("Enter your name: ")
    category = select_category()
    difficulty = select_difficulty()
    questions = fetch_trivia_questions(category, difficulty)
    score = play_game(questions)
    print(f"\n{player_name}, your final score is: {score}")
    save_score(player_name, score)
    display_leaderboard()


def fetch_trivia_questions(category, difficulty):
    """Fetches trivia questions from an external API.

    This function retrieves 10 trivia questions based on the selected
    category and difficulty from the Open Trivia Database.

    Parameters:
        category (int): The trivia category ID.
        difficulty (str): The difficulty level ('easy', 'medium', 'hard').

    Raises:
        HTTPError: If the API request fails.

    Returns:
        list: A list of trivia questions.
    """
    url = f"https://opentdb.com/api.php?amount=10&category={category}&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        print("Failed to fetch trivia questions.")
        return []


def select_category():
    """Displays a list of trivia categories for the player to choose from.

    Returns:
        int: The selected category ID.
    """
    categories = {
        9: "General Knowledge",
        10: "Entertainment: Books",
        11: "Entertainment: Film",
        12: "Entertainment: Music",
        13: "Entertainment: Musicals & Theatres",
        14: "Entertainment: Television",
        15: "Entertainment: Video Games",
        16: "Entertainment: Board Games",
        17: "Science & Nature",
        18: "Science: Computers",
        19: "Science: Mathematics",
        20: "Mythology",
        21: "Sports",
        22: "Geography",
        23: "History",
        24: "Politics",
        25: "Art",
        26: "Celebrities",
        27: "Animals",
        28: "Vehicles",
        29: "Entertainment: Comics",
        30: "Science: Gadgets",
        31: "Entertainment: Japanese Anime & Manga",
        32: "Entertainment: Cartoon & Animations"
    }
    print("\nSelect a category:")
    for key, value in categories.items():
        print(f"{key}: {value}")
    while True:
        try:
            category = int(input("Enter the category number: "))
            if category in categories:
                return category
            else:
                print("Invalid category number. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def select_difficulty():
    """Allows the player to select a difficulty level.

    Returns:
        str: The selected difficulty level ('easy', 'medium', 'hard').
    """
    difficulties = ["easy", "medium", "hard"]
    print("\nSelect a difficulty level:")
    for difficulty in difficulties:
        print(difficulty.capitalize())
    while True:
        difficulty = input("Enter difficulty (easy/medium/hard): ").lower()
        if difficulty in difficulties:
            return difficulty
        else:
            print("Invalid difficulty level. Try again.")


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


def save_score(player_name, score):
    """Saves the player's score to a file.

    This function appends the player's name and score to a JSON file
    to maintain a leaderboard.

    Parameters:
        player_name (str): The name of the player.
        score (int): The final score of the player.

    Returns:
        None
    """
    leaderboard = []
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        pass

    leaderboard.append({"name": player_name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file, indent=4)


def display_leaderboard():
    """Displays the leaderboard.

    This function reads and displays the top scores from the
    leaderboard JSON file.

    Returns:
        None
    """
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
            print("\nLeaderboard:")
            for entry in leaderboard[:10]:
                print(f"{entry['name']}: {entry['score']}")
    except FileNotFoundError:
        print("\nNo leaderboard data available.")


if __name__ == "__main__":
    main()
