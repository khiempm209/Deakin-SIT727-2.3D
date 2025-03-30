from app import create_app, db
from app.models import Question, QuizResult
import pandas as pd

app = create_app()

with app.app_context():
    Question.query.delete()
    QuizResult.query.delete()
    db.session.commit()

    data = pd.read_parquet("hf://datasets/Mihaiii/trivia_single_choice-4-options/data/train-00000-of-00001.parquet")
    # insert questions to the database
    for i, q in data.iterrows():
        question = Question(
            question=q['question'],
            option_a=q['option_A'],
            option_b=q['option_B'],
            option_c=q['option_C'],
            option_d=q['option_D'],
            correct_option=q['correct_option']
        )
        db.session.add(question)
    
    db.session.commit()
    print("Seed data successfully")
