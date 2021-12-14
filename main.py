from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField
from flask_ckeditor import CKEditor, CKEditorField
import smtplib, ssl
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)
ckeditor = CKEditor(app)


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Table
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    github_url = db.Column(db.String(250), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_path = db.Column(db.String(250), unique=True, nullable=False)

# db.create_all()

# New Project Form
class ProjectForm(FlaskForm):
    title = StringField("Project Title", validators=[DataRequired()])
    img_path = StringField("Image Path", validators=[DataRequired()])
    github_url = StringField("GitHub URL", validators=[DataRequired()])
    body = CKEditorField("Project Description", validators=[DataRequired()])
    submit = SubmitField("Submit Project")

#Contact Form
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired("Please enter your name.")])
    email = EmailField("Email", validators=[DataRequired("Please enter your email."), Email("Please enter a valid email.")])
    body=CKEditorField("Message", validators=[DataRequired("I would love to hear from you!")])
    submit = SubmitField("Send Message")

# Changes footer year to match current year
CURRENT_YEAR = datetime.now().year

# Email info for contact page
EMAIL_PARAMS = {"from_address": os.getenv("YAHOO_EMAIL"), "app_password": os.getenv("APP_PASSWORD"),"to_address": os.getenv("GMAIL_EMAIL")}
# Database structure

@app.route("/")
def redirect_home_page():
    return redirect(url_for("home_page"))

@app.route("/welcome")
def home_page():
    projects = db.session.query(Project).limit(3).all()
    return render_template("index.html", year=CURRENT_YEAR, projects=projects)

@app.route("/projects")
def project_page():
    projects = db.session.query(Project).all()
    return render_template("projects.html",year=CURRENT_YEAR, projects=projects)

@app.route("/contact-me", methods=["POST", "GET"])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL_PARAMS["from_address"], password=EMAIL_PARAMS["app_password"])
            connection.sendmail(
                from_addr=EMAIL_PARAMS["from_address"],
                to_addrs=EMAIL_PARAMS["to_address"],
                msg=f"Subject:Contact Form\n\n{name}\n{email}\n{message}")
        return redirect(url_for("home_page"))

    return render_template("contact.html", year=CURRENT_YEAR, form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', year=CURRENT_YEAR), 404

# @app.route("/new_project", methods=["POST", "GET"])
# def add_project():
#     if request.method == "POST":
#         new_project = Project(
#             title=request.form.get("title"),
#             github_url = request.form.get("github_url"),
#             body=request.form.get("body"),
#             img_path=request.form.get("img_path"),
#         )
#         db.session.add(new_project)
#         db.session.commit()
#         return redirect(url_for('add_project'))
#     else:
#         form = ProjectForm()
#         return render_template("new_project.html", form=form, is_edit=False)
#

if __name__ == "__main__":
    app.run(debug=False)