# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.


## API Endpoint Documentation

### Categories

POST ```/categories```
* Create a new category
* Request Body:
```
{
    type:string
}
```
* Returns: True if successfully created
* Example Response:
```
{
    'success': True,
    'created': 7,
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports",
        '7' : "a"
                },
    'total_categories': 7
                }
```
GET ```/categories```
* Fetches a dictionary of categories
* Request Arguments: None
* Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
* Example Response:
```
{
    'success': True,
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
        }
}
```
DELETE ```/categories/<int:category_id>```
* Deletes a category from the categories list.
* Request parameters: `category_id`
* Returns: True if successfully deleted
* Example Response:
```
{
    'success': True,
    'deleted': '2',
    'categories': {
        '1' : "Science",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
        }
    'total_categories': '5'
}

GET ```/categories/<int:category_id>/questions```
* Fetch questions by category
* Request parameters: `category_id`
* Example Response:
```
{
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?",
            "rating": 1
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?",
            "rating": 3
        }
    ],
    "success": true,
    "total_questions": 19
}
### Questions

POST ```questions```
* Create a new question
* Request Body:
```
{
    question: string,
    answer: string,
    category: int,
    difficulty: int,
    rating: int
}
```
* Returns: True if successfully created
* Example Response:
```
{
    'success': True,
    'created': 2,
    'questions': {
            {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
            "rating": 3
        }
    },
    'total_question': 1
}
```
GET ```/questions?page=<page_number>```
* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Fetches a dictionary of questions in which the keys are the answer, category, difficulty, id, question and rating
* Request Arguments: 'page number'
* Returns: List of questions, number of total questions, current category and categories.
* Example Response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
            "rating": 3
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
            "rating": 4
        }
        ],
    "success": true,
    "total_questions": 19
}
```
DELETE ```/questions/<int:question_id>```
* Deletes a question from the questions list.
* Request parameters: `question_id`
* Returns: True if successfully deleted
* Example Response:
```
{
    'success': True,
    'deleted': '2',
    'questions': [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 3,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
            "rating": 3
        }
    ]
    'total_questions': '1'
}
```
POST ```/search```
* Fetch questions based on search term
* Request Body:
```
{
    searchTerm: string
}
```
* Example Response:
```
{
    'success': True,
    'questions': [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
            "rating": 4
        }
    ],
    'total_questions': 1
            }
```
POST ```/quizzes```
* Fetch questions to play quiz
* Request body:
```
{
    "quiz_category": string,
    "previous_questions": []
}
```
* Example Response:
```
{
    "question":{
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?",
        "rating": 5
        },
    "success": True
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

Note:
if "psql trivia_test < trivia.psql" doesn't work try
psql -d trivia -U postgres -a -f trivia.psql
where postgres is the userid
```
