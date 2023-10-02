# Creating Databse

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

`CREATE USER 'username'@'host' IDENTIFIED BY 'password';`

Grant all permission to the user, this will be use to manipulate data from database in later part.

`GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';`


Setting Python conection with mysql database:

First, run this command on your system:

`import mysql.connector`

After that set the connection with mysql server with following commands:

`connection = mysql.connector.connect(

    host='127.0.0.1',
    port=3306,
    database='database_name',
    user='username',
    password='password',
    autocommit=True
)`


# Accessing the game

We have to make a user table in the database to login into the game.
The table can be made using the command as below:

`CREATE TABLE user (

    id int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255),
    PRIMARY KEY (id)
);`


After successful completion of this command, create a user for yourself in order to play the game.

# Game logic

- For the current version of game the 'maximum_height_of_airport_selected' is the highest airport of china with elevation_ft of 14472.
- The co2 base point are given as 2500 at base level.
- There will be one question asked and four corresponding choices (including one correct answer) will be presented to the user.
- For every correct answer the user will get 500 additional points in his/her present c02_points.
- If the user enters the wrong answer, the game will be over.
- The is one robbed question twist in the game as well. The robbed question will devoid user of all the points and his co2_points will become 0. However, If the user is able to give correct answer of a trick question, user will be able to regain all of his lost points.
- The user will be able to enter in the safe island, only when the user have gain 7000 points and then the game will end.
- If the user have less points and have answered all the question, he will be given one extra bonus question at the end of game and that will decide user fate.
Happy playing.