from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin ,login_required,login_user, logout_user, current_user


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "thekey"

db = SQLAlchemy()

login_manager = LoginManager()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False, unique=True)
    password = db.Column(db.String(20), nullable = False)

class employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20),db.ForeignKey(Users.username), nullable = False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    client_username = db.Column(db.String(250), db.ForeignKey(Users.username), nullable=False)
    employee_username = db.Column(db.String(250), db.ForeignKey(Users.username), nullable=True)


login_manager.init_app(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
@login_required
def home():
    
    emp = employee.query.filter_by(Username=current_user.username).first()
    task = Task.query.all()
    return render_template('home.html', ph = emp, tasks = task)



@app.route('/createAccount', methods=["GET","POST"] )
def createAccount():
    if request.method == 'POST':
        User = Users(username=request.form.get('username'),
                     password=request.form.get("password")
                     )
        db.session.add(User)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method =='POST':
        user = Users.query.filter_by(username=request.form.get("username")).first()

        if user.password == request.form.get("password"):
            print('pass wroung')
            login_user(user)
            return redirect(url_for("home"))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/update', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        username = current_user.username
        email = request.form['email']
        phone = request.form['phone']

        emp = employee(Username=username, email=email, phone=phone)
        db.session.add(emp)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('update.html', username= current_user.username)


@app.route('/post_task', methods=['GET', 'POST'])
def post_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        client_username = current_user.username
        task = Task(title=title, description=description, client_username=client_username)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('post.html', username = current_user.username)

if __name__ == "__main__":
    app.run(debug=True)

