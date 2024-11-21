# **_whataduudle_**

Welcome to _whataduudle_ django project!

- Visit _whataduudle_ front-end repository [here](https://github.com/Mandy2114/duudle-backend).

- Visit _whataduudle_ back-end repository [here](https://github.com/Mandy2114/duudle-backend).

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

1. As a User (AAU), I want to be able to sign up for an account if I choose to.
2. AAU, I want to be able to sign in and sign out.
3. AAU, I want to be able to see a landing page.
4. AAU, when the game is won or lost, I want to be able to replay.
5. AAU, I want to be able to draw my prompt.
6. AAU, I want to be able to clear my drawing.
7. AAU, I want to see the prompt and word while I am drawing.
8. AAU, I want to see the timer, how much time I have left, and the prompt while I am drawing.
9. AAU, I want a fast and exciting round lasting 20–40 seconds.

#### WireFrame

![alt text](/README.Images/README-whataduudle!.png)
Home Page
![alt text](/README.Images/README-homepage.png)
Start Game
![alt text](/README.Images/README-game-start.png)
Darwing
![alt text](/README.Images/README-draw.png)
Register
![alt text](/README.Images/README-signin-register.png)
Prompt
![alt text](/README.Images/README-prompt-win-lose.png)

#### Color Palette

![alt text](./README.Images/READEM-color-palette.png)

```javascript
  theme: {
    extend: {
      colors: {
        'vanilla': {
          DEFAULT: '#f1e8b8',
          100: '#473e0e',
          200: '#8d7c1c',
          300: '#d4bb2a',
          400: '#e3d270',
          500: '#f1e8b8',
          600: '#f4edc5',
          700: '#f6f1d4',
          800: '#f9f6e2',
          900: '#fcfaf1'
        },
        'flax': {
          DEFAULT: '#f9e784',
          100: '#493f03',
          200: '#927d07',
          300: '#dbbc0a',
          400: '#f6da3c',
          500: '#f9e784',
          600: '#faec9e',
          700: '#fcf1b6',
          800: '#fdf6ce',
          900: '#fefae7'
        },
        'atomic-tangerine': {
          DEFAULT: '#e58f65',
          100: '#39190a',
          200: '#713313',
          300: '#aa4c1d',
          400: '#dc682e',
          500: '#e58f65',
          600: '#eaa785',
          700: '#efbda3',
          800: '#f5d3c2',
          900: '#fae9e0'
        },
        'indian-red': {
          DEFAULT: '#d05353',
          100: '#2e0d0d',
          200: '#5b1919',
          300: '#892626',
          400: '#b73232',
          500: '#d05353',
          600: '#d97575',
          700: '#e39898',
          800: '#ecbaba',
          900: '#f6dddd'
        },
        'eerie-black': {
          DEFAULT: '#191919',
          100: '#050505',
          200: '#0a0a0a',
          300: '#0f0f0f',
          400: '#141414',
          500: '#191919',
          600: '#474747',
          700: '#757575',
          800: '#a3a3a3',
          900: '#d1d1d1'
        }
      }
    }
  },
```

#### REACT Components

![alt text](/README.Images/README-REACT-Components.png)

#### Trello

- Visit the [Trello board](https://trello.com/b/RlAy2kky/pics)

### BACK-END

#### ERD

MVP
![alt text](./README.Images/README-MVP.png)
POST MVP
![alt text](./README.Images/README-POST-MVP.png)
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

![alt text](/README.Images/README-Routes.png)

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

![alt text](image.png)

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

- **Purpose:** (GET)/(POST) The list of all words and create a word.

## WordDetail(generics.RetrieveUpdateDestroyAPIView)

- **Purpose:** (GET)/(POST)/(DELETE) Get a single word and its details.

## WordGame(generics.CreateAPIView)

- **Purpose:** (POST) Creates game for user with the retrieved word.

## DrawingList(generics.ListCreateAPIView)

- **Purpose** (GET)/(POST) The list of words.

## DrawingDetails(generics.RetrieveUpdateDestroyAPIView)

- **Purpose** (GET)/(PUT)/(DELETE) Get a single word.

### Post-MVP

1. AAU, I want a different color to draw with.
2. AAU, I want an eraser button.
3. AAU, I want a difficulty option.
4. AAU, I want an undo button.
5. AAU, I want a high-score leaderboard.
6. AAU, I want multiple modes.
7. AAU, I want both a redo and an undo button.
