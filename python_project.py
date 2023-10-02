## game project
import random

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
co2_points = 2500


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
        print(f"Welcome {query_result[0][1]} to the game!")
        return True
    else:
        print("User does not exist")
    return False


def create_questions():
    question_sql = (" SELECT name, iso_country, municipality, elevation_ft FROM airport where  elevation_ft > 14472 ")
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
            question = "What is the name of airport in iso country " + row[1] + " with municipality " + row[2]
            answer = row[0]
            choices.append(answer)
            for i in range(0, 3):
                choices.append(choices_query_result[random.randint(0, 600)][0])

            qa["question"] = question
            qa["answer"] = answer
            random.shuffle(choices)
            qa["choices"] = choices
            question_answers.append(qa)
    else:
        print("no found")

    return question_answers


def robbed_question():
    print("You have been robbed and all of your points have been gone. But you can gain all of your points by answering"
          " this tricky question")

    bonus_qa = {}
    bonus_question = "Why should oranges wear sunscreen? "
    bonus_answer = "so that they do not peel"
    bonus_qa["question"] = bonus_question
    bonus_qa["answer"] = bonus_answer

    return bonus_qa
# add your bonus question here. If the user answers this question right he gets 2000 bonus points.
def extra_bonus_question():
    print("place holder for extra bonus question")
    return

# add your riddle  question here. If the user answers this question right he gets 3500 bonus points.
def riddle_question():
    print("place holder for riddle question")
    return

def start_game():
    global co2_points
    print("There was a disease break out in China and all the other countries having lower "
          "altitude than China have been destroyed. \n"
          " Your only chance left is to go to countries having higher altitude than China. \n"
          "You have been given 2500 co2 points and you will gain more points as game progress.")
    print("Hi! Good day. Kindly choose 1 option below to login the game: \n 1. New Player \n 2. exisitng player")
    login_option = int(input("Enter your answer here: "))
    if login_option == 1:
        name_value = input("Enter your name here: ")
        password_value = input("Enter your password here: ")
        print(new_player_registration(name_value, password_value))

    elif login_option == 2:
        name_value = input("Enter your name here: ")
        password_value = input("Enter your password here: ")
        existing_player_login(name_value, password_value)
    else:
        print("Invalid option selected")

    questions_answers = create_questions()

    robbing_question = random.randint(0, len(questions_answers)-1)
    for index in range(0, len(questions_answers)):
        if index == robbing_question:
            print("YOU ARE ROBBED")
            bonus_question_answer = robbed_question()
            print(bonus_question_answer["question"])
            bonus_answer = input("Enter your answer here: ")
            if bonus_question_answer["answer"] == bonus_answer:
                print("RIGHT ANSWER")
                print("YOUR CO2 POINTS REMAIN THE SAME: " + str(co2_points))
            else:
                co2_points = 0
                print(f"Wrong answer. You loose all your co2 points {co2_points}")

        print(questions_answers[index]["question"])

        answer_choices = questions_answers[index]["choices"]
        answer = questions_answers[index]["answer"]

        for choice_index in range(0, len(answer_choices)):
            print(str(choice_index + 1) + ". " + answer_choices[choice_index])
        answer_index = int(input("Enter option number here: "))

        if answer_choices[answer_index-1] == answer:
            print("RIGHT ANSWER")
            co2_points = co2_points + 500
            print(f"You have gained 500 points. You total co2 points are: {co2_points}")
        else:
            print("YOU LOSE, GAME OVER")
            break

        if (index == len(questions_answers) - 1) and (4500 <= co2_points <= 5500):
            extra_bonus_question()
        elif (index == len(questions_answers) - 1) and (co2_points < 4500):
            riddle_question()
        else:
            print(f"You co2_points {co2_points} are not enough to enter the safe zone ")


if __name__ == "__main__":
    start_game()
