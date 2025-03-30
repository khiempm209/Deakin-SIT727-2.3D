from .models import Question, QuizResult
from . import db
import random

def get_questions():
    # get all questions from database, select randomly 10 ones
    questions = Question.query.all()
    if len(questions) < 10:
        return questions
    return random.sample(questions, 10)

def get_top_score(top=5):
    top_score = QuizResult.query.order_by(QuizResult.score.desc(), QuizResult.time.asc()).limit(5).all()
    return top_score

def check_name_exist(name):
    exists = QuizResult.query.filter_by(name=name).first() is not None
    return exists

def add_result(name, score, time):
    new_result = QuizResult(name=name, score=score, time=time)
    db.session.add(new_result)
    db.session.commit()