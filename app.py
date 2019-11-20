from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy as sqla

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATAVASE_URI'] = 'sqlite://db/task.db'
db = sqla(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    content = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean)


@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', list_tasks = tasks)

@app.route('/create-task', methods=['POST'])
def create_task():
    task = Task(content=request.form['content'], done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('edit-task/<id>', methods=['PUT'])
def edit_task(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.coomit()
    return redirect(url_for('home'))


@app.route('delete-task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
