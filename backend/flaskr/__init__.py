# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException
from models import setup_db, Question, Category

# ----------------------------------------------------------------------------#
# Pagination
# ----------------------------------------------------------------------------#
QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins.
    '''
    cors = CORS(app, resources={r'/*': {'origins': '*'}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            return abort(404, 'Categories not found')
        return jsonify({
          'success': True,
          'categories': {
            category.id: category.type for category in categories
            }
        })
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()

        if len(current_questions) == 0:
            return abort(404, 'Questions not found')

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(Question.query.all()),
          'current_category': None,
          'categories': {
            category.id: category.type for category in categories
            },

        })
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id
            ).one_or_none()

            if question is None:
                return abort(404, f'Question with id: {question_id} not found')

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except Exception as e:
            return abort(e)
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get_json('question', None)
        answer = body.get_json('answer', None)
        category = body.get_json('category', None)
        difficulty = body.get_json('difficulty', None)
        if not (question and answer and category and difficulty):
            return abort(400, 'Required object keys missing from request')
        try:
            question = Question(
                question=question, answer=answer,
                category=category, difficulty=difficulty
                )
            question.insert()

            selection = Question.query.order_by(Question.category).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_question': len(Question.query.all())
                })
        except Exception as e:
            return abort(e)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            search = body.get('searchTerm', None)

            if search:
                selection = Question.query.filter(
                    Question.question.ilike(f'%{search}%')
                    ).all()

                if selection:
                    current_questions = paginate_questions(request, selection)

                else:
                    return jsonify({
                        'selection': False,
                        'questions': None,
                        'total_questions': None,
                        'current_category': None
                    })
        except Exception as e:
            return abort(e)

        return jsonify({
            'selection': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': None
            })
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            selection = Question.query.filter(
                Question.category == str(category_id)
                ).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                return jsonify({
                    'success': False,
                    'questions': None,
                    'total_questions': len(Question.query.all()),
                    'current_category': category_id
                })
        except Exception as e:
            return abort(e)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_category': category_id
            })
    '''
    @TODO:
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
            body = request.get_json()
            quiz_category = body.get('quiz_category', None)
            previous_question = body.get('previous_question', None)

            if quiz_category['id'] == 0:
                if previous_question is None:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(
                        Question.id.notin_(previous_question)
                        ).all()

            elif quiz_category['id'] != 0:
                if previous_question is None:
                    questions = Question.query.filter(
                        Question.category == quiz_category['id']
                        ).all()
                else:
                    questions = Question.query.filter(
                        Question.category == quiz_category['id'],
                        Question.id.notin_(previous_question)
                        ).all()

            else:
                return abort(422, 'unprocessable')

            question = random.choice(questions) if len(questions) > 0 else ''

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception as e:
            return abort(e)
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        return jsonify({
          'Success': False,
          'error': error.code,
          'message': error.description
          }), error.code

    @app.errorhandler(Exception)
    def exception_handler(error):
        return jsonify({
          'Success': False,
          'error': 500,
          'message': f'Internal Server error: {error}'
        }), 500
    return app
