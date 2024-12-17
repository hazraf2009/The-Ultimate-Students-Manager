

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