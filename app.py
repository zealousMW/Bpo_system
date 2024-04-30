from flask import Flask , render_template, redirect , url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user,logout_user,login_remembered, current_user


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

app.config["SECRET_KEY"] = "NisNigga"

db = SQLAlchemy()


login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Task', backref='client', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Task', backref='employee', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    client_username = db.Column(db.String(250), db.ForeignKey('users.username'), nullable=False)
    employee_username = db.Column(db.String(250), db.ForeignKey('users.username'), nullable=True)

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

db.init_app(app)
with app.app_context():
	db.create_all()
	
@app.route('/register', methods=["GET", "POST"])

def register():
	if request.method == "POST":
		user = Users(username=request.form.get("username"),
					password=request.form.get("password"))
		
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		
		if user.password == request.form.get("password"):
			
			login_user(user)
			return redirect(url_for("home"))
		
	return render_template("login.html")

@app.route("/")
@login_required
def home():
	client = Client.query.filter_by(username=current_user.username).first()
	tasks = client.tasks
	return "welcome nigga " + tasks

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)