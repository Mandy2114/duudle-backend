# **_WhatADuudle_**

**Project Created By:**

**_Mandy DeCamp, Norman Lee, Tim Lim, Nyunt Sein and Emmanuel Rosario_**

## **Technologies**

### **_FRONT-END_**

- Tailwind - CSS
- React
- Tensor Flow
- CanvasAPI
- Javascript
- Vite

### **_BACK-END_**

- Python
- Django
- POSTGRESQL
- Django REST Framework
- CORS
- rest_API

## What is **_WhatADuudle_**?

**_WhatADuudle_** is a drawing game where players can have an quick, exciting and fun time, testing their drawing skills.

**HOW TO PLAY**

1. Press the **_'Play'_** button and recieve a word.
2. Once you are ready, click **_'Start Drawing'_** and begin to draw within the time-limit.
3. Once timer is up, the computer will guess and if it guesses the drawing to the word provided, **YOU WIN!**
   Else You lose and you can try again
4. **\_**Repeat and HAVE FUN!!**\_**

## USER STORIES

### FRONT-END

#### WireFrame

[Whataduudle WireFrame](README.Images/WireFrame.jpg, "Whataduudle WireFrame")

### BACK-END

#### Set-Up

1. Clone the repo
1. Run command
   `pipenv shell`
   and install the dependences...
   `pipenv install`
1. Create the Databases using this command. Make sure to uncomment the lines shown...
   `psql -f create-database.sql`
   [Create Database commands](/README.Images/CreateDataBaseCommand.png "MVP ERD")
   Image of CREATE DATABASE
1. Once Created run these commands to make migrations for the models.
   `python manage.py makemigrations`
   `python manage.py migrate`
   1. To see if migrations were succussful use the command...
      `python manage.py showmigrationss `
1. Run the server
   `python manage.py runserver`
1. Create An Admin for your database
   `python manage.py createsuperuser`
   1. Fill out the username and password of your choosing. (Email field can be left blank).

#### ERD

[MVP ERD](README.Images/ERD.MVP.jpeg "MVP ERD")

**User**

- **Id:** The identification number of a user. This is an auto-created field.
- **username:** The name that the user will be recognized as. (This is a String)
- **password:** A password created by the user in order to sign-in to their account. (This is a String)
- **email:** The email used to verify the user. (This is a String)

**Games**

- **Id:** The identification number of a game. This is an auto-created field.
- **status:** The status of the game. Whether a game is in session or has ended. (This is a Boolean)
- **current_word:** The word that the user will try to replicate. (This is a String)
- **Winner:** The identifier to see if the user has made a sufficient drawing that matches the word. (This is a Boolean)
- **date_played:** The date the game was played. (This is a time-stamp).

**Word**

- **Id:** The identification number of a word. This is an auto-created field.
- **game_id:** (Foreign Key) References the Game Id.
- **prompt:** The word that will be shown to the user. (This is a String)

**Drawing**

- **Id:** The identification number of a drawing. This is an auto-created field.
- **game_Id:** (Foreign Key) References the Game Id.
- **drawing:** The drawing that the user will draw. This will be store as JSON, to save space.

### Routes

# API Endpoints Documentation

## User Endpoints

### User Sign-Up

- **Endpoint:** `/users/register/`
- **Method:** `POST`
- **Description:** Creates a new user account.

### User Login

- **Endpoint:** `/users/login/`
- **Method:** `POST`
- **Description:** Authenticates a user and returns a token.

---

## Game Endpoints

### List of Games

- **Endpoint:** `/games/`
- **Method:** `GET`
- **Description:** Retrieves a list of all games.

### Individual Game

- **Endpoint:** `/games/<game_id>/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific game.

---

## Word Endpoints

### List of Words

- **Endpoint:** `/words/`
- **Method:** `GET`
- **Description:** Retrieves a list of all words.

### Individual Word

- **Endpoint:** `/words/<word_id>/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific word.

### Start a Game

- **Endpoint:** `/words/<word_id>/games/`
- **Method:** `POST`
- **Description:** Starts a new game with the specified word.

---

## Drawing Endpoints

### List of Drawings for a Game

- **Endpoint:** `/games/<game_id>/drawings/`
- **Method:** `GET`
- **Description:** Retrieves a list of drawings for a specific game.

### Add Drawing to a Game

- **Endpoint:** `/games/<game_id>/drawings/`
- **Method:** `POST`
- **Description:** Adds a new drawing to a specific game.

---

## Game Update Endpoints

### Player Passed

- **Endpoint:** `/games/<game_id>/`
- **Method:** `PATCH`
- **Description:** Updates the game state to indicate a player has passed.

### Update Game State

- **Endpoint:** `/games/<game_id>/`
- **Method:** `PATCH`
- **Description:** Updates the game state with a new word, difficulty, and winner information.

### Models

## Word

- **Prompt (CharField):**
- **Difficulty (CharField):**
- **Category (ForeignKey):**

## Game

- **Result (BooleanField):**
- **word (ManytoManyField):**
- **user (OneToOneField):**
- **created_at (DateTimeField):**
- **difficulty (CharField):**

## Drawing

- **game (OneToOneField):**
- **art (TextFirld):**

### Views

## Home(APIView)

- **Purpose:** Show home page..

## CreateUserView(generics.CreateAPIView)

- **Purpose:** ????

## LoginView(APIView)

- **Purpose:** User login page..

## VerifyUserView(APIView)

- **Purpose:** Check an authentication for user..

## GameDetails(generics.RetrieveUpdateDestroyAPIView)

- **Purpose:** Create a game.(POST)

## GameDetails(generics.RetrieveUpdateDestroy)

- **Purpose:** (GET)/(POST)/(DELETE) for game.

## WordList(generics.ListCreateAPIView)

- **Purpose:** (POST) ???

## WordDetail(generics.RetrieveUpdateDestroyAPIView)

- **Purpose:** (GET)/(POST)/(DELETE) ???

## WordGame(generics.CreateAPIView)

- **Purpose:** (POST) ???

## DrawingList(generics.ListCreateAPIView)

- **Purpose** (POST) ???

## ClearDrawings(APIView)

- **Purpose** (DELETE) ???

## DESIGNS
