## game project
import random
import pyfiglet
import threading
import mysql.connector
import simple_colors
from art import *
from rich import print

import time
import datetime

import mysql.connector
connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='flightgameuser',
    password='123Maa123',
    autocommit=True
)

maximum_height_of_airport_selected = "14472"
co2_budget_points = 2500


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
        print(f"[sea_green2]Welcome {query_result[0][1]} to the game![/sea_green2]")
        return True
    else:
        print("[bright_red]User does not exist[/bright_red]")
    return False


def create_questions():
    question_sql = ("SELECT name, iso_country, iso_region, elevation_ft FROM airport "
                    "where elevation_ft > 14472 order by elevation_ft asc")
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
            question = "What is the name of airport in iso country " + row[1] + " with elevation: " + str(row[3]) + " ft"
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
    global co2_budget_points
    list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]
    text_length = 4
    random_text = ''.join(random.choice(list) for _ in range(text_length))
    art_code = pyfiglet.figlet_format(random_text, font='isometric1')
    print(art_code)
    art_code_answer = input("What is the code, type in lowercase: ")
    if art_code_answer == random_text:
        title = pyfiglet.figlet_format('Hurray!! Correct', font='banner3')
        print(f"[sea_green2]{title}[/sea_green2]")
        co2_budget_points = co2_budget_points + 700
        print(f'[dark_slate_gray2]Your have gained 700 points, your new co2_points are: {co2_budget_points}[/dark_slate_gray2]')
    else:
        print("[bright_red]You gain no bonus points[/bright_red]")
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
        print("[bright_red]Too bad, time is up. You die[/bright_red]")
    else:
        print(f"Your answer is: {user_input}")
    return user_input


def riddle_question():
    number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    random.shuffle(number_list)
    code_separate = number_list[:3]
    code = ''.join(code_separate)
    #print(code)
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
    print(f"[bright_red]{title}[/bright_red]")
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
    print(f"[orange3]{title}[/orange3]")


def start_game():
    global co2_budget_points
    tprint("Welcome", font="random")
    time.sleep(2)
    print("[bold magenta]Lets begin the adventure![/bold magenta]")
    time.sleep(1)
    print("[bold magenta]Outline of our story: [/bold magenta] \n")
    time.sleep(3)
    print("[bold magenta]A toxic cloud of unknown origin has destroyed human civilization![/bold magenta] \n")
    time.sleep(3)
    print("[bold magenta]It is known that all the places on Earth with altitude lower than 14472 ft were destroyed.[/bold magenta]\n")
    time.sleep(3)
    print("[bold magenta]You are a pilot of a commercial airplane, and you have to save your crew and passengers. [/bold magenta]\n")
    time.sleep(3)
    print("[bold magenta]You start in the Daocheng Airport (ZUDC) of China and move to higher altitude airports, with the hints provided along the way.[/bold magenta] \n ")
    time.sleep(3)
    print("[bold magenta]You have been given: [/bold magenta]")
    time.sleep(3)
    print("[bold magenta]2500 co2 budget points.[/bold magenta] \n")
    time.sleep(3)
    print("[bold magenta]As you fly to higher airports you co2_budget decreases but you can gain more along the way..[/bold magenta]\n ")
    time.sleep(3)
    print("[bold magenta]You need atleast 4500 co2 budget points to take the final journey into safe heaven..  [/bold magenta]\n ")
    time.sleep(4)
    print("[bold magenta]You have to choose the right airport name to reach it.\n")
    time.sleep(4)
    print("[turquoise2]Get ready!! [/turquoise2]\n")
    time.sleep(3)
    print("[chartreuse1]Kindly choose 1 option below to login the game: \n 1. New Player \n 2. Exisitng player [/chartreuse1] \n")
    login_option = int(input("Enter your answer here: "))
    if login_option == 1:
        name_value = input("Enter your name here: ")
        password_value = input("Enter your password here: ")
        new_user_id = new_player_registration(name_value, password_value)
        if new_user_id > 0:
            print("[chartreuse1]User registered successfully!![/chartreuse1]")
        else:
            print("[bright_red]There was some problem with the registration[/bright_red]")

    elif login_option == 2:
        for i in range(0, 3):
            name_value = input("Enter your name here: ")
            password_value = input("Enter your password here: ")
            is_user_logged_in = existing_player_login(name_value, password_value)
            if is_user_logged_in:
                break
            else:
                if i == 2:
                    print("[bright_red]You have entered wrong credentials for 3 times. Exiting [/bright_red]")
                    return
    else:
        print("[bright_red]Invalid option selected[/bright_red]")
        return

    countdown()
    questions_answers = create_questions()

    robbing_question = random.randint(1, len(questions_answers) - 1)
    bonus_question = random.randint(1, len(questions_answers) - 1)
    for index in range(0, len(questions_answers)):
        if index == robbing_question:
            title = pyfiglet.figlet_format('"YOU ARE ROBBED"!!', font='banner')
            print(f"[green1]{title}[/green1]")
            bonus_question_answer = robbed_question()
            print(f"[green_yellow]{bonus_question_answer['question']} [/green_yellow]")
            bonus_answer = input("Enter your answer here: ")
            if "not peel" in bonus_answer:
                title = pyfiglet.figlet_format('You escaped the robber!!', font='digital')
                print(f"[bright_cyan]{title}[/bright_cyan]")
                print(f"[bright_magenta]YOUR CO2 POINTS REMAIN THE SAME: [/bright_magenta] " + str(co2_budget_points))
            else:
                co2_budget_points = 0
                print(simple_colors.yellow(f"Wrong answer. You loose all your co2 points {co2_budget_points}"))
        if index == bonus_question:
            title = pyfiglet.figlet_format('"Bonus Question"!!', font='3-d')
            print(simple_colors.magenta(f"{title}"))
            art_question()

        print(f"[bright_green]{questions_answers[index]['question']}[/bright_green]")

        answer_choices = questions_answers[index]["choices"]
        answer = questions_answers[index]["answer"]

        for choice_index in range(0, len(answer_choices)):
            print(str(choice_index + 1) + ". " + answer_choices[choice_index])

        print("[deep_sky_blue1]You can buy hint by pressing 'h'. Note: your 300 points will be deducted for the hint.[/deep_sky_blue1]\n ")
        answer_index = input("Enter option number here: ")
        if answer_index == "h":
            print("\n")
            print(f"[bright_green]Your hint is the iso_region of airport : [/bright_green]" + questions_answers[index]["hint"])
            co2_budget_points = co2_budget_points - 300
            print(f"[honeydew2]Now remaining co2_points after deduction are: {co2_budget_points}[/honeydew2] \n")
            answer_index = input("Enter option number here: ")

        if answer_choices[int(answer_index) - 1] == answer:
            title = pyfiglet.figlet_format('Correct', font='doom')
            print(f"[cyan2]{title}[/cyan2]")
            co2_budget_points = co2_budget_points + 500
            print(f"[wheat1]You have gained 500 points. You total co2 budget points are: {co2_budget_points}[/wheat1] \n")
            print("\n")
            time.sleep(3)
        else:
            game_over()
            break

        if (index == len(questions_answers) - 1) and co2_budget_points >= 2000:
            print(f"Your co2_points are: {co2_budget_points}")
            print("[dark_slate_gray2]You have final chance to answer this riddle question to enter in safe heavens'[/dark_slate_gray2]")
            riddle = riddle_question()
            answer = time_limit_answer()
            if riddle["answer"] == answer:
                co2_budget_points = co2_budget_points + 3000
                if co2_budget_points >= 4500:
                    win_game()
                if co2_budget_points < 4500:
                    print(f"[bright_red]You co2_points {co2_budget_points} are not enough to enter the safe zone [/bright_red]")
                    game_over()
                    break
            if riddle["answer"] != answer:
                title = pyfiglet.figlet_format('You lose', font='block')
                print(f"[bright_red]{title}[/bright_red]")
                if co2_budget_points >= 4500:
                    print("[bright_yellow]You have given an extra life.. Since you have more tha 4500 co2_budget points at your end. [/bright_yellow]\n")
                    print("[bright_yellow]Your points above 4500 will be saved for next time you play.. \n[/bright_yellow]")
                    win_game()
                if co2_budget_points < 4500:
                    game_over()
                    break

            else:
                print(f"[bright_red]You co2_points {co2_budget_points} are not enough to enter the safe zone [/bright_red]")
                game_over()


if __name__ == "__main__":
    start_game()
