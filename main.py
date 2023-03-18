from flask import Flask, render_template, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, InputRequired, Email
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ.get('db_user_name')}:" \
                                        f"{os.environ.get('db_user_password')}@" \
                                        f"{os.environ.get('db_ip_addr')}/"  \
                                        f"{os.environ.get('db_name')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # init flask-migrate

# name form
class NameForm(FlaskForm):
    name = StringField("Enter Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[InputRequired(), Email()])
    submit_btn = SubmitField("Submit")

# database table definitions
class UserSubmit(db.Model):
    __tablename__ = "user_submit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    email = db.Column(db.String(320), unique=False, nullable=False)
    ts = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __repr__(self):
        return f"{self.id} {self.name} submitted on {self.ts}"

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = UserSubmit(name=form.name.data,
                          email=form.email.data)
        db.session.add(user)
        db.session.commit()
        session["name"] = form.name.data
        return redirect(url_for("index"))
    return render_template("index.html", form=form, name=session.get("name"))
