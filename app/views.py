from flask import render_template, request, redirect, url_for, session
from . import create_app, db
from .controllers import *
from .models import Question, QuizResult
import time

app = create_app()

@app.route('/')
def start():
    # initialize a new session
    session.clear()
    top_score_obj = get_top_score()
    return render_template('start.html', top_score = top_score_obj)

@app.route('/begin', methods=['POST'])
def begin_quiz():
    # get randomly 10 questions 
    questions = get_questions()
    session['questions'] = [q.id for q in questions]
    session['current'] = 0
    session['score'] = 0
    session['time'] = time.time()
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'questions' not in session:
        return redirect(url_for('start'))
    
    # get the index of the current question
    current = session.get('current', 0)
    questions_ids = session['questions']
    if request.method == 'POST':
        selected = request.form.get('option')
        question_id = questions_ids[current - 1]
        question_obj = Question.query.get(question_id)
        if selected == question_obj.correct_option:
            session['score'] = session.get('score', 0) + 1
        if current == len(questions_ids):
            session['time'] = time.time() - session['time']
            return redirect(url_for('result'))
        
    question_id = questions_ids[current]
    question_obj = Question.query.get(question_id)
    session['current'] = current + 1

    return render_template('question.html', question=question_obj, current=current+1, total=len(questions_ids))

@app.route('/result', methods=['GET', 'POST'])
def result():
    score = session.get('score', 0)
    time = session.get('time', 0)
    if request.method == 'POST':
        name = request.form.get('name')
        exists = check_name_exist(name)
        if exists:
            return render_template('result.html', score=score, time=time, saved=False, name_exist=True)
        add_result(name, score, time)
        return render_template('result.html', score=score, name=name, time=time, saved=True, name_exist=False)
    return render_template('result.html', score=score, time=time, saved=False, name_exist=False)