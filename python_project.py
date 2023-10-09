## game project
import random
import pyfiglet
import threading
import mysql.connector
import simple_colors
from art import *
# from rich import print

import time
import datetime
from PIL import Image

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='flightgameuser',
    password='123Maa123',
    autocommit=True
)

maximum_height_of_airport_selected = "14472"
co2_points = 2500


def countdown():
    global timer
    total_seconds = 0 * 3600 + 0 * 60 + 5
    while total_seconds > 0:
        timer = datetime.timedelta(seconds=total_seconds)
        print(f"The game will began in {timer}", end="\r")
        time.sleep(1)
        total_seconds -= 1


def execute_query(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor


def new_player_registration(name, password):
    sql = "INSERT INTO user (username,password) VALUES ('" + name + "','" + password + "')"
    return execute_query(sql).lastrowid


def existing_player_login(name, password):
    sql = " select * from user where  username = '" + name + "' and password = '" + password + "'"
    cursor = execute_query(sql)
    query_result = cursor.fetchall()
    if cursor.rowcount > 0:
        print(simple_colors.red(f"Welcome {query_result[0][1]} to the game!"))
        return True
    else:
        print(simple_colors.yellow("User does not exist"))

    return False


def create_questions():
    question_sql = "SELECT name, iso_country, iso_region, elevation_ft FROM airport where  elevation_ft > 14472 order by elevation_ft asc"
    question_cursor = execute_query(question_sql)
    question_query_result = question_cursor.fetchall()

    choices_sql = " SELECT name FROM airport where elevation_ft < 14472 limit 600"
    choices_cursor = execute_query(choices_sql)
    choices_query_result = choices_cursor.fetchall()

    question_answers = []
    if len(question_query_result) > 0:
        for row in question_query_result:
            qa = {}
            choices = []
            question = "What is the name of airport in iso country " + row[1]
            answer = row[0]
            hint = row[2]
            choices.append(answer)
            for i in range(0, 3):
                choices.append(choices_query_result[random.randint(0, 600)][0])

            qa["question"] = question
            qa["answer"] = answer
            random.shuffle(choices)
            qa["choices"] = choices
            qa["hint"] = hint
            question_answers.append(qa)
    else:
        print("no found")

    return question_answers


def robbed_question():
    print("You have been robbed and all of your points have been gone. But you can gain all of your points by answering"
          " this tricky question")

    bonus_qa = {}
    bonus_question = "Why should oranges wear sunscreen? "
    bonus_qa["question"] = bonus_question

    return bonus_qa


def art_question():
    global co2_points
    list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]
    text_length = 4
    random_text = ''.join(random.choice(list) for _ in range(text_length))
    art_code = pyfiglet.figlet_format(random_text, font='isometric1')
    print(art_code)
    art_code_answer = input("What is the code, type in lowercase: ")
    if art_code_answer == random_text:
        title = pyfiglet.figlet_format('Hurray!! Correct', font='banner3')
        print(simple_colors.green(f"{title}"))
        co2_points = co2_points + 700
        print(simple_colors.green(f'Your have gained 700 points, your new co2_points are: {co2_points}'))
    else:
        print(simple_colors.yellow("You gain no bonus points"))
    return


def time_limit_answer():
    user_input = None

    def get_input():
        nonlocal user_input
        user_input = input("You have 180 seconds to answer: ")

    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout=180)

    if input_thread.is_alive():
        print("Too bad, time is up. You die")
    else:
        print(f"Your answer is: {user_input}")
    return user_input


def riddle_question():
    number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    random.shuffle(number_list)
    code_separate = number_list[:3]
    code = ''.join(code_separate)
    remaining_numbers = [item for item in number_list if item not in code_separate]
    hint1 = []
    hint1.append(code_separate[1])
    hint1.insert(0, remaining_numbers[0])
    hint1.insert(2, remaining_numbers[1])
    hint2 = []
    hint2.append(code_separate[2])
    hint2.insert(0, remaining_numbers[0])
    hint2.insert(2, remaining_numbers[2])
    hint3 = []
    hint3.append(code_separate[1])
    hint3.insert(1, remaining_numbers[3])
    hint3.append(code_separate[2])
    hint4 = []
    hint4.append(remaining_numbers[2])
    hint4.append(remaining_numbers[3])
    hint4.append(remaining_numbers[4])
    hint5 = []
    hint5.append(remaining_numbers[2])
    hint5.append(remaining_numbers[3])
    hint5.append(code_separate[1])
    print("Congratulations, you have reached the gate of the safe haven.")
    time.sleep(3)
    print("The council wants to give you a final test before entering.")
    time.sleep(3)
    print("Stands in front of you is a lock that opens with a 3-digit code.")
    time.sleep(3)
    print("The council gives you hints to solve.")
    time.sleep(2)
    print("However, you only have 180 seconds until the toxic clouds reach you.")
    time.sleep(3)
    print("Hints:")
    time.sleep(1)
    print(hint1, " One number is correct and right placed")
    time.sleep(2)
    print(hint2, " One number is correct but wrong placed")
    time.sleep(2)
    print(hint3, " Two numbers are correct but wrong placed")
    time.sleep(2)
    print(hint4, " Nothing is correct")
    time.sleep(2)
    print(hint5, " One number is correct but wrong placed")
    time.sleep(2)
    riddle = {"answer": code}
    return riddle


def game_over():
    title = pyfiglet.figlet_format('YOU LOSE, GAME OVER', font='doom')
    print(simple_colors.red(f"{title}"))
    print('   _____ \n'
          '  |     | \n'
          '  |     | \n'
          '  |     | \n'
          '  |     O \n'
          '  |    /|\ \n'
          '  |    / \ \n'
          '__|__\n')


def win_game():
    title = pyfiglet.figlet_format('Welcome to Safe Heavens', font='doom')
    print(simple_colors.blue(f"{title}"))


def start_game():
    global co2_points
    tprint("Welcome", font="random")
    time.sleep(2)
    print(simple_colors.red('Lets begin the adventure!', ['bold']))
    time.sleep(1)
    print(simple_colors.yellow('Outline of our story: ', ['bold']))
    time.sleep(3)
    print(simple_colors.yellow('There was a disease break out in China and all the other countries having lower '
                               'altitude than China have been destroyed.'))
    time.sleep(3)
    print(simple_colors.yellow('Your only chance of survival is to go to countries having higher altitude than China'))
    time.sleep(3)
    print(simple_colors.yellow('You have been given: '))
    time.sleep(1)
    print(simple_colors.yellow('2500 co2 points.', ['bold', 'underlined']))
    time.sleep(1)
    print(simple_colors.yellow('You will gain more points as game progress..'))
    time.sleep(3)
    print(simple_colors.red("Get ready!!", ['bold']))
    time.sleep(3)
    print(
        simple_colors.yellow('Kindly choose 1 option below to login the game: \n 1. New Player \n 2. exisitng player'))
    login_option = int(input("Enter your answer here: "))
    if login_option == 1:
        name_value = input("Enter your name here: ")
        password_value = input("Enter your password here: ")
        print(new_player_registration(name_value, password_value))

    elif login_option == 2:
        name_value = input("Enter your name here: ")
        password_value = input("Enter your password here: ")
        is_user_logged_in = existing_player_login(name_value, password_value)
        if is_user_logged_in == False:
            return
    else:
        print("Invalid option selected")
        return

    countdown()
    questions_answers = create_questions()

    robbing_question = random.randint(1, len(questions_answers) - 1)
    bonus_question = random.randint(1, len(questions_answers) - 1)
    for index in range(0, len(questions_answers)):
        if index == robbing_question:
            title = pyfiglet.figlet_format('"YOU ARE ROBBED"!!', font='banner')
            print(simple_colors.magenta(f"{title}"))
            bonus_question_answer = robbed_question()
            print(simple_colors.blue(bonus_question_answer["question"], ['bold']))
            bonus_answer = input("Enter your answer here: ")
            if "not peel" in bonus_answer:
                title = pyfiglet.figlet_format('You escaped the robber!!', font='digital')
                print(simple_colors.cyan(f"{title}"))
                print(
                    simple_colors.yellow("YOUR CO2 POINTS REMAIN THE SAME: " + str(co2_points), ['bold', 'underlined']))
            else:
                co2_points = 0
                print(simple_colors.yellow(f"Wrong answer. You loose all your co2 points {co2_points}"))
        if index == bonus_question:
            title = pyfiglet.figlet_format('"Bonus Question"!!', font='3-d')
            print(simple_colors.magenta(f"{title}"))
            art_question()

        print(simple_colors.blue(questions_answers[index]["question"], ['bold', 'underlined']))

        answer_choices = questions_answers[index]["choices"]
        answer = questions_answers[index]["answer"]

        for choice_index in range(0, len(answer_choices)):
            print(str(choice_index + 1) + ". " + answer_choices[choice_index])

        print(simple_colors.red("Press h for hint. Note: your 300 points will be deducted for the hint."))
        answer_index = input("Enter option number here: ")
        if answer_index == "h":
            print(simple_colors.yellow("Your hint is the iso_region of airport : " + questions_answers[index]["hint"],
                                       ['bold']))
            co2_points = co2_points - 300
            print(simple_colors.magenta(f"Now remaining co2_points after deduction are: {co2_points}", ['bold']))
            answer_index = input("Enter option number here: ")

        if answer_choices[int(answer_index) - 1] == answer:
            title = pyfiglet.figlet_format('Correct', font='doom')
            print(simple_colors.yellow(f"{title}"))
            co2_points = co2_points + 500
            print(simple_colors.yellow(f"You have gained 500 points. You total co2 points are: {co2_points}"))
            time.sleep(3)
        else:
            title = pyfiglet.figlet_format('You lose', font='doom')
            print(simple_colors.yellow(f"{title}"))
            game_over()
            break

        if (index == len(questions_answers) - 1) and co2_points >= 4500:
            print(f"Your co2_points are: {co2_points}")
            print('riddle question: ', simple_colors.red(
                'The points are less than 4000. You have final chance to answer this riddle question to enter in safe heavens',
                'bold'))
            riddle = riddle_question()
            answer = time_limit_answer()
            if riddle["answer"] == answer:
                co2_points = co2_points + 2000
                if co2_points >= 5500:
                    win_game()
                else:
                    print(f"You co2_points {co2_points} are not enough to enter the safe zone ")
                    game_over()
                    break
            if riddle["answer"] != answer:
                print("Wrong answer")
                if co2_points >= 5500:
                    win_game()
                else:
                    game_over()
                    break

            else:
                print(f"You co2_points {co2_points} are not enough to enter the safe zone ")
                game_over()


if __name__ == "__main__":
    start_game()
