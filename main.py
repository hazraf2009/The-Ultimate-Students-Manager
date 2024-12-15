from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tugas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    deadline = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<tugas {self.id}>'
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/task')
def Task():
    page = request.args.get('page', 1, type=int)
    tasks = Tugas.query.order_by(Tugas.date_created).paginate(page=page, per_page=5)
    return render_template('Task.html', tasks=tasks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/create')
def create():
    return render_template('create_task.html')

@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        ape = request.form['nama']
        deadline = request.form['dead']

        deadline = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')

        new = Tugas(isi=ape, deadline=deadline)
        try:
            db.session.add(new)
            db.session.commit()

            return redirect('/task')
        except:
            return 'error'
    
    else:
        return render_template('create_task.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Tugas.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/task')
    
    except:
        return 'error'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Tugas.query.get_or_404(id)
    if request.method == 'POST':
        task.isi= request.form['nama']
        task.deadline = request.form['dead']

        task.deadline = datetime.strptime(task.deadline, '%Y-%m-%dT%H:%M')
        try:
            db.session.commit()
            return redirect('/task')
        except:
            return 'error'

    else:
        return render_template('update_task.html', task=task)
    

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        # Query for a user with matching login and password
        user = User.query.filter_by(login=email, password=password).first()

        if user:
            return redirect('/index')
        else:
            error = 'Login atau kata sandi tidak tepat'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
    
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        regis = User(login=email, password=password)

        try:
            db.session.add(regis)
            db.session.commit()
            return render_template('login.html')
        except:
            return 'error'
    else:
        return render_template('registrasi.html')
        
if __name__ == '__main__':
    app.run(debug=True)

