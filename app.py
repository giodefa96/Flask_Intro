from crypt import methods
from curses import meta
from flask import Flask, redirect, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # for relative path we have to put trhee slash
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    

@app.route('/', methods=['POST','GET'])

# adesso creiamo questo if statement che ci permette di
# se la richiesta è post allora aggiungiamo quello che viene
# scritto all'interno del form all'interno del DB
# Sennò non facciamo altro che rimanere nella pagina

def index():

    if request.method == 'POST':
        task_content = request.form['content']
        # cioè vogliamo che la variabile sia uguale al content
        # che abbiamo nel nostro html index
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issues adding your task'

    else:
        tasks = Todo.query.order_by(Todo.data_created).all()
        # quindi in questo caso lui proverà a guardare tutto
        # quello che troviamo all'interno del nostro DB
        # quindi vi facciamo una query e chiederemo di 
        # riordinare il tutto per la data di creazione
        # potremmo fare anche tipo .first() per ridarci solo il più recente
        return render_template('index.html', task=tasks)
    

@app.route('/delete/<int:id>')# devo ora dare un qualcosa per far riverimento alle cose che deve cncellar L'id andrà benissimo
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issues updatin your task'
    else:
        return render_template('update.html', task=task )

if __name__ == '__main__':
    app.run(debug=True)