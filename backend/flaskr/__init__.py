import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.urls import url_quote
from werkzeug.wrappers import Request, Response
from models import *
from config import *
import unittest

QUESTIONS_PER_PAGE = 10

# EVERY FUNCTION AND METHOD HAS ITS RESOURCES ATTACHED ABOVE
# IT IN A COMMENT♥
# I had a lot of trouples setting up autopep8
# so if it didn't work for you as well, neighter did black
# or yapf try this: python -m autopep8 --max-line-length 60
# --in-place --aggressive --aggressive <yourfile.py>


def paginate_questions(request, selection):
    # This code is inspired from: Lesson 3: Endpoints and Payloads (Concept 5. Flask Part II)
    # First: we request the page
    # The following formula is based on "get(key, default=None, type=None)"
    # So, if there isn't a given page, It's gonna be page 1 by default
    # To know more:
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request.args
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # Formatting questions https://www.geeksforgeeks.org/python-format-function/
    # and looping through questions that we intend to paginate using for-in loop
    # https://www.w3schools.com/python/python_for_loops.asp
    questions = [question.format()
                 for question in selection]
    current_page = questions[start:end]

    # Returns the paginated questions
    return current_page


# test_config=None explained in the flask documentation:
# https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/


def create_app(test_config=None):
    # Creating the flask app
    # To know more read the Quick start section :
    # https://flask.palletsprojects.com/en/1.1.x/quickstart/
    app = Flask(__name__)
    setup_db(app)
    '''
   @TODO (Done): Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
   '''
    # CORS(app)
    # RESOURCES:Check example 2 in here:
    # https://www.programcreek.com/python/example/91987/flask_cors.CORS
    # And also check Lesson 3: Endpoints and Payloads in
    # Part : 3. API Development and Documentation
    cors = CORS(app, resources={
                r"/api/*": {"origins": "*"}})
    '''
   @TODO(Done): Use the after_request decorator to set Access-Control-Allow
   '''
    @app.after_request
    def set_access_allow_control(response):
        # Resource:On MDN:  https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
        # and https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
        # And also check Lesson 3: Endpoints and Payloads in
        # Part : 3. API Development and Documentation,
        # Concept number 3
        response.headers.add(
            'Access-Control-Allow-Headers',
            'ContentType,Authorization, True')

        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,UPDATE,OPTIONS,PUT')

        return response

    '''
    @TODO (Done):
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Using SQLAlchemy for creating a list of categories
        # and ordering (Arranging them ) by type
        categories = Category.query.order_by(
            Category.type).all()

        # If there are no categories, abort 404 ( Category
        # not found )
        if not categories:
            abort(404)
        # Return the categories
        return jsonify({
            'success': True,
            'categories':
            {category.id: category.type
             for category in categories}
        })

    '''
    @TODO(Done):
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            # Querying all questions available in the Question table in db using query.
            # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
            all_questions = Question.query.order_by(
                Question.id).all()
            # Getting available categories from Category
            # table in db and ordering them by type
            categories = Category.query.order_by(
                Category.type).all()
            questions_list = paginate_questions(request, all_questions)
            if len(questions_list) == 0:
                abort(404)
                
            all_categories = [category.format() for category in categories]
            """
             Reviewer's feedback: 
             Endpoint to handle GET requests for questions,
             including pagination (every 10 questions).
             This endpoint should return a list of questions,
             number of total questions,
             current category, categories.
            """
            return jsonify({
                'success': True,
                'questions_list': questions_list,
                'categories':
                {category.id: category.type
                 for category in categories},
                'total_questions': len(all_questions),
                'current_category': None
            })
        except BaseException:
            abort(422)

    '''
  @TODO (Done):
  Create an endpoint to DELETE question using a question ID.
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    @app.route('/questions/<int:question_id>',
               methods=['DELETE'])
    def delete_questions(question_id):
        # Storing questions in a variable by getting all
        # questions from the "Question" table in the
        # database
        question = Question.query.get(question_id)

        if not question:
            # If it's not a question ( Or the ID doesn't
            # exist) raise 404 error " Question not found "
            abort(404)

        try:
            # If it's a question, delete it
            question.delete()

            # On a successful delete return a success
            # message
            return jsonify({
                'success': True,
                # Returns the ID  of the deleted question
                'deleted': question_id
            })

        except BaseException:
            abort(422)

    '''
  @TODO(Done):
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():

        body = request.get_json()
        # If the user didn't set any value, set it to None
        # as default ( It's explained in the classroom)
        add_question = body.get('question', None)
        add_answer = body.get('answer', None)
        add_category = body.get('category', None)
        add_difficulty = body.get('difficulty', None)

        if not (add_question and add_answer and add_difficulty
                and add_category):
            abort(
                400, {
                    'message': 'Please, Fill all the required fields'})

        try:
            # Inserting the new question to the database
            # inside " Question" table
            question = Question(question=add_question,
                                answer=add_answer,
                                difficulty=add_difficulty,
                                category=add_category)

            question.insert()

            return jsonify(
                {'success': True, 'created': question.id})

        except BaseException:
            # If anything went wrong, handle the 422 error
            abort(422)
        '''
    @TODO(Done):
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('search_term')
        print(search_term)

        if search_term:
            search_results = Question.query.filter(
                # Learn about like operator:
                # https://www.postgresqltutorial.com/postgresql-like/
                Question.question.like(f'%{search_term}%')).all()
            if len(search_results) == 0:
                # Learn more about raising exceptions:
                # https://docs.python.org/3/tutorial/errors.html
                # part (8.3. Handling Exceptions¶)
                raise Exception(
                    "Oops! Search term not found, Try something else or write fewer words "
                )

            return jsonify(
                {
                    'success': True,
                    'questions': [
                        question.format() for question in search_results],
                    'total_questions': len(search_results),
                })

        abort(404)  # Search term not found

    '''
  @TODO(Done):
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    """
    I hope the reviewer who reviewed my last submission to see that
    the TODO says : Create a "GET" endpoint and
    How can I GET a question using POST ?
    And I also don't understand clearly,
    how can I "POST" while I need to "GET" it ?
    I'm confused, I need a little help
    Thanks in advance ♥ <3 :D
    p.S: I editted it to POST anyway
    """
    @app.route('/categories/<int:category_id>/questions',
               methods=['POST'])
    def get_questions_by_category(category_id):
        try:
            # Creating a list (Query) of all the questions
            # in a category
            questions = Question.query.filter(
                Question.category == category_id).all()

            # Returning the questions in a category
            return jsonify(
                {
                    'success': True,
                    'questions': [
                        question.format() for question in questions],
                    'total_questions': len(questions),
                    'current_category': category_id})
        except BaseException:
            # Handling 404 error
            # Or if len(questions) == 0: abort(404)
            abort(404)

            # Just in case you wanna find out which way is better,
            # (try-except ) or ( if-else) Well, (try-except) is a bit faster
            # To know more:
            # https://www.geeksforgeeks.org/try-except-vs-if-in-python/

    '''
  @TODO(Done):
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            # To parse data as JSON we use get_json, To know
            # more:
            # https://flask.palletsprojects.com/en/1.1.x/api/
            # flask.Request.get_json
            body = request.get_json()
            # setting None as the default value as it was
            # explained in the lessons
            previous_questions = body.get(
                'previous_questions', None)
            quiz_category = body.get('quiz_category')['id']

            if (quiz_category == 0):
                questions = Question.query.all()
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category).all()

            # In order to remove the previous questions
            questions = Question.query.filter(
                Question.id.in_(previous_questions)).all()
            # Another way by using " notin" instead of "in":
            # Question.query.filter_by(category=category['id'])
            # .filter(Question.id.notin_((previous_questions))).all()

            if (len(questions) > 0):
                # For creating random questions
                # randit: Return random questions.
                # https://docs.python.org/3/library/random.html#functions-for-integers
                # (Functions for integers¶)
                question = questions[random.randint(
                    0, len(questions))].format()
            else:
                question = None

            return jsonify(
                {'success': True, 'question': question})

        except BaseException:
            abort(422)  # unprocessable

    # @TODO(Done): Create error handlers for all expected errors including 404 and 422.
    # To know more about errors check this https://httpstatusdogs.com/
    # https://www.flickr.com/photos/girliemac/sets/72157628409467125-------#
    # Or this :
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
