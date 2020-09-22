import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO (done)
    Write at least one test for each test for
    successful operation and for expected errors.
    """

    #To know more about errors check this https://httpstatusdogs.com/ -------#
    # Or this : https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    # ----------------------------------------------------------------------#
    # Test for Get requests
    #-----------------------------------------------------------------------#
    # These tests are based on Lesson 4: API testing(
    # 2.Testing in flask && 3. Practice testing in flask)

    def test_get_categories_success(self):
        # Setting response: that the client is getting this
        # endpoint
        res = self.client().get('/categories')
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        # Making sure that status code is 200 ( Success )
        self.assertEqual(res.status_code, 200)
        # Success value of body is True
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_null_categories(self):
        # To test this we have to try a path that probably doesn't even exist
        # Setting response: that the client is getting this
        # endpoint
        res = self.client().get('/categories/98765432100000')
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        # Chacking that status code is 404 which means that
        # Success is set to false
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # GET questions endpoint
    def test_get_questions_success(self):
        # Setting response: that the client is getting this
        # endpoint /questions
        res = self.client().get('/questions')
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        # Making sure that status code is 200 ( Success )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_get_category_questions_success(self):
        # Setting response: that the client is getting this
        # endpoint /categories/1/questions
        res = self.client().get('/categories/1/questions')
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

        # Making sure that status code is 200 ( Success )
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_get_category_null_questions(self):
        # Setting response: that the client is getting this endpoint /categories/10000000/questions
        # It doesn't exist so it's gonna raise the 404 error
        res = self.client().get('/categories/10000000/questions')
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # --------------------------------------------------------#
    # DELETE Tests
    # --------------------------------------------------------#
    def test_delete_question_success(self):
        # Creating a test question
        test_question = Question(
            question='Who lives in a pineapple under the sea?',
            answer='Sponge Bob Square Pants!',
            difficulty=1,
            category=1)

        # Adding test question to the database
        test_question.insert()
        test_question_id = test_question.id

        # Delete test question
        res = self.client().delete(
            '/questions/{}'.format(test_question_id))
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        # Making sure that status code is 200 ( Success )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['deleted'], str(test_question_id))

    def test_delete_unprossessable_question(self):
        res = self.client().delete('/questions/10000000')
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'Unprossessable entity')

    # POST Tests
    # ----------------------------------------------------------------------

    def test_create_question_success(self):
        # Creating test question data to add
        test_question_data = {
            'question': 'What is the answer to the meaning '
            'of life and everything in it?',
            'answer': '42.',
            'difficulty': 1,
            'category': 1
        }

        # Attempting to create question with test question
        # data
        res = self.client().post(
            '/questions', json=test_question_data)
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        # Making sure that status code is 200 ( Success )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_questions_found(self):

        new_question_search = {
            'search_term': 'astronomy',
        }

        res = self.client().post(
            '/questions', json=new_question_search)
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    def test_search_questions_404(self):
        new_question_search = {'search_term': ''}

        res = self.client().post('/questions/search',
                                 json=new_question_search)
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'Resource Not Found')

    def test_play_quiz_success(self):
        test_round_data = {
            'quiz_category': {'type': 'Art', 'id': 7}}
        
        #Editted to "quizzes" after first review on Udacity 
        res = self.client().post('/quizzes', json=test_round_data)
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_unprosessable_quiz(self):
        test_data = {'quiz_category': {
            'type': 'Art', 'id': 7}}

        res = self.client().post('/quizzes', json=test_data)
        # Loading data using JSON.loads, To know more check the links below:
        # https://www.w3schools.com/python/python_json.asp
        # https://docs.python.org/3/library/json.html
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'Unprossessable entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
