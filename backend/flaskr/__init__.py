# ----------------------------------------------------------------------------#
# IMPORTS
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException
from models import setup_db, Question, Category

# ----------------------------------------------------------------------------#
# PAGINATION
# ----------------------------------------------------------------------------#
QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


# ----------------------------------------------------------------------------#
# APP
# ----------------------------------------------------------------------------#
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    CORS. Allow '*' for origins.
    '''
    cors = CORS(app, resources={r'/*': {'origins': '*'}})
    '''
    Decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response
    # ----------------------------------------------------------------------------#
    # CATEGORIES
    # ----------------------------------------------------------------------------#

    # Create
    # ----------------------------------------------------------------------------#
    @app.route('/categories', methods=['POST'])
    def create_category():
        body = request.get_json()

        category_type = body.get('type', None)

        if not category_type:
            return abort(400, 'Required object keys missing from request')
        try:
            category = Category(type=category_type)
            category.insert()

            categories = Category.query.all()

            return jsonify({
                'success': True,
                'created': category.id,
                'categories': {
                    category.id: category.type for category in categories
                },
                'total_categories': len(categories)
                })
        except Exception:
            return abort(422, "unprocessable")

    # Read
    # ----------------------------------------------------------------------------#
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

    # Delete
    # ----------------------------------------------------------------------------#
    @app.route('/categories/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):
        try:
            category = Category.query.filter(
                Category.id == category_id
            ).one_or_none()
            if category is None:
                return abort(404, f'Category with id:{category_id} not found')

            category.delete()
            categories = Category.query.all()

            return jsonify({
                'success': True,
                'deleted': category_id,
                'categories': categories,
                'total_categories': len(categories)
                })

        except Exception:
            return abort(404, f'Category with id:{category_id} not found')

    # Search by Category
    # ----------------------------------------------------------------------------#
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            selection = Question.query.filter(
                Question.category == str(category_id)
                ).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                return abort(422, "unprocessable")

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category_id
            })

        except Exception:
            return abort(422, "unprocessable")

    # ----------------------------------------------------------------------------#
    # QUESTIONS
    # ----------------------------------------------------------------------------#

    # Create
    # ----------------------------------------------------------------------------#
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        rating = body.get('rating', None)
        if not (question and answer and category and difficulty and rating):
            return abort(400, 'Required object keys missing from request')
        try:
            question = Question(
                question=question, answer=answer,
                category=category, difficulty=difficulty,
                rating=rating
                )
            question.insert()

            selection = Question.query.order_by(Question.category).all()
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                return abort(422, "unprocessable")

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_question': len(Question.query.all())
                })
        except Exception:
            return abort(422, "unprocessable")

    # Read
    # ----------------------------------------------------------------------------#
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        try:
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                return abort(422, "unprocessable")

            categories = Category.query.all()

            if len(categories) == 0:
                return abort(404, 'Categories not found')

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'current_category': None,
                'categories': {
                    category.id: category.type for category in categories
                    }
                })
        except Exception:
            abort(404, 'Questions not found')

    # Delete
    # ----------------------------------------------------------------------------#
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id
            ).one_or_none()
        if question is None:
            return abort(404, f'Question with id:{question_id} not found')
        try:
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                return abort(422, "unprocessable")

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
                })
        except Exception:
            return abort(500)

    # Search by text
    # ----------------------------------------------------------------------------#
    @app.route('/search', methods=['POST'])
    def search_questions():
        if not request.data:
            abort(422, 'unprocessable')

        body = request.get_json()
        search_term = body.get('searchTerm', None)

        selection = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))
            ).all()

        if not selection:
            abort(404, 'Question not found')

        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            return abort(422, "unprocessable")

        return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(current_questions)
            })

    # ----------------------------------------------------------------------------#
    # QUIZ
    # ----------------------------------------------------------------------------#
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            if quiz_category['id'] == 0:
                if previous_questions is None:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(
                        Question.id.notin_(previous_questions)
                        ).all()

            elif quiz_category['id'] != 0:
                if previous_questions is None:
                    questions = Question.query.filter(
                        Question.category == quiz_category['id']
                        ).all()
                else:
                    questions = Question.query.filter(
                        Question.category == quiz_category['id'],
                        Question.id.notin_(previous_questions)
                        ).all()

            question = random.choice(questions) if len(questions) > 0 else []

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception:
            return abort(422, "unprocessable")

    # ----------------------------------------------------------------------------#
    # ERROR HANDLERS
    # ----------------------------------------------------------------------------#
    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        return jsonify({
          'success': False,
          'error': error.code,
          'message': error.description
          }), error.code

    @app.errorhandler(Exception)
    def exception_handler(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': f'Internal Server error: {error}'
        }), 500
    return app
