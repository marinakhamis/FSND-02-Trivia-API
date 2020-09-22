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

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API documentation
___ 
## Getting Started
- Prerequisites: 
  1. **Python 3.7**

        Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

  2. **Virtual Enviornment**

        We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

  3. Install the **PIP dependencies** by running this command 
        ```bash
        pip install -r requirements.txt
        ```
  
  
  
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

## Error Handling
- Errors are returned as JSON objects in the following format:
    ```javaScript
    {
        "success": False, 
        "error": 400,
        "message": "bad request"
    }
    ```
- The API will return six error types when requests fail:

    - 400: Bad Request
    - 404: Resource Not Found
    - 405: Method not allowed
    - 422: Not Processable
    - 500: Internal server error 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Available Endpoints

These are the required endpoints according to the TODOs

                          Allowed Methods
| Endpoints   | GET | POST | DELETE |
|-------------|-----|------|--------|
| /questions  | [x] | [x]  | [x]    |
| /categories | [x] | [x]  | [x]    |
| /quizzes    |     | [x]  |        |

Now I'll illustrate them in details 

## **1.** GET Method
Before talking about the endpoints, we have to understand what GET means
- **Definition**: The get() method returns the value of the item with the specified key.
- **Syntax**: ``` dictionary.get(keyname, value) ```
- To know more: https://www.w3schools.com/python/ref_dictionary_get.asp 

Now let's explain each GET request:
### 1.  GET /categories: 
   - This method returns the categories
   - **Request parameters**: None 
   - For example it returns: 
        ```
        {
        "success": true,
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
            }
        }

        ```
### 2.  GET /questions: 
- Fetches a paginated dictionary of questions of all available questions
- **Request parameters**: None
- For example:
    ```
    return jsonify({
        'success': True,
        'questions_list': [
            {
            "question": "Who lives in a pineapple under the sea?",
            "answer": "Sponge Bob Square Pants!", 
            "categories": 1, 
            "difficulty": 1, 
            "id": 1, 
            "total_questions": 1,
            "current_category": None
            }
    })
    ```
## **2.** POST Method
**Definition**:

The ```post()``` method sends a POST request to the specified url.

The ```post()``` method is used when you want to send some data to the server.

**Syntax**

```requests.post(url, data={key: value}, json={key: value}, args) ```
Now let's explain each POST request:


### 1.  POST /questions: 

 To POST (create) a new question,
  which will require the question and answer text,
  category, and difficulty score.
- **Request body:** {question:string, answer:string, difficulty:int, category:string} and they are "None" by default
- For example :
    ```js
        {
        "success": true,
        "created": 25 # This is the ID of the added question
        }
    ```
### 2. POST /questions by categories:
 To get questions based on category. (It was a GET request but the reviewer told me to make it a post request)
- **Request body:** {questions: arr, current_category: {id:int, type:string}}
- **Example:**
    ```js
        {
        'success': True,
        'questions': "who said that the truth is rarely pure and never simple?",
        'total_questions': 16,
        'current_category': 2}
    ```
### 3. POST /quizzes
To get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Art", "id" : "2"}} ' -H 'Content-Type: application/json'
```

- **Request parameters**: None

## **3.** DELETE Method:
**Definition**
The delete() method sends a DELETE request to the specified url.

DELETE requests are made for deleting the specified resource (file, record etc).

**Syntax**

``` requests.delete(url, args) ```

1. DELETE /questions/<int:question_id >
    Delete Questions
    ```bash
    curl -X DELETE http://127.0.0.1:5000/questions/8
    ```
    - Deletes specific question based on given id
    - Request Arguments: 
    - **integer** `question_id`
    - Request Headers : **None**
    - Returns: 
        - **integer** `deleted` Id from deleted question.
        - **boolean** `success`
    ```js
    {
    "deleted": 10,
    "success": true
    }
    ```