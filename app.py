from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<question %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        question_content = request.form['content']
        new_question = Todo(content=question_content)
        
        try:
            db.session.add(new_question)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your question"
    
    else:
        questions = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', questions=questions)
    
@app.route('/answer/<int:id>', methods=['GET','POST'])
def answer(id):
    question = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        question.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding answer'
    else:
        return render_template('answer.html', question=question)
    
@app.route('/delete/<int:id>')
def delete(id):
    question_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(question_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that question'
    
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    question = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        question.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your question'
    else:
        return render_template('update.html', question=question)

if __name__ == "__main__":
    app.run(debug = True)
        
