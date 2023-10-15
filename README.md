# Creating Database

Craete a databse flight_game in your mysql

`create database flight_game;`

Select the new database to use:
`use flight_game;`

Run the script below in the MySQL command line client:
`source full\path\tosql\file.sql`

where:

- source is the command to execute the script.
`full\path\tosql\file.sql` is the path to the sql file on your system.
- Save the script file to a location on your system that is easy to find.

Note: The script must be saved with the .sql extension, not as .txt.
Replace the example path in the command with the actual path.
Run the command on the MySQL command line.

After the sucessful installtion of flight_game database on your system, explore the data and see table of airport and see its description using the command: 

`desc airport;`


Create a user that will be used to make connection with database with following credentials:

`CREATE USER flightgameuser@localhost IDENTIFIED BY '123Maa123';`

Grant all permission to the user, this will be use to manipulate data from database in later part.

`GRANT ALL PRIVILEGES ON flight_game.* TO flightgameuser@localhost;`


Setting Python conection with mysql database:

First, run this command on your system:

`import mysql.connector`

After that set the connection with mysql server with following commands:

`connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='flightgameuser',
    password='123Maa123',
    autocommit=True
)`


# Accessing the game

- We have to make a user table in the database to login into the game.
The table can be made using the command as below:

`CREATE TABLE user (
    id int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255),
    PRIMARY KEY (id)
);`


- Install the required packages from the requirements file using the command

`pip install -r requirements.txt `


- Run the python game using python 3.11.4 by executing the following command:

`python3 python_project.py `

# Game logic

- For the current version of game, the maximum height of airport selected is the highest airport of China with elevation ft of 14472.

- The co2 budget points are given as 2500 at base level.

- The user will be able to enter in the safe island, only when the user has gain 4500 points and then the game will end.

- You have to register first to play the game. There are two types of player login:
  . New player
  . Existing player
Enter you username and password to register.

- There will be one question asked and four corresponding choices (including one correct answer).

- For every correct answer the player will get 500 additional points c02 budget points. These co2 budget points help the player to fly to next destination.

- If the user enters the wrong answer, the game will be over.

- The is one random robbed question in the game as well. The robbed question will devoid user of all the points and his co2 budget points will become 0. However, If the user can give correct answer to a trick question, user will be able to regain all his lost points.

- Player can get a random bonus question in form of an artistic shape as well. On guessing the artistic word right, the user gets 700 bonus co2 budget points.

- The player can also buy hints, but that will cost the player 700 of his co2 budget points.

- There is a riddle question that will give user additional 3000 co2 budget points. You must answer 3-digit riddle in 180 seconds before the time is over. If you have less than 4500, this riddle will help you to win the game. If you have more than 4500 points, these extra points by the riddle will be saved for your next game, and you will enter the safe heavens whether you answer the riddle right or wrong.