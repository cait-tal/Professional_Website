from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
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
    body = CKEditorField("Project Description")
    submit = SubmitField("Submit Project")

# Changes footer year to match current year
CURRENT_YEAR = datetime.now().year

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', year=CURRENT_YEAR), 404

@app.route("/new_project", methods=["POST", "GET"])
def add_project():
    if request.method == "POST":
        new_project = Project(
            title=request.form.get("title"),
            github_url = request.form.get("github_url"),
            body=request.form.get("body"),
            img_path=request.form.get("img_path"),
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('add_project'))
    else:
        form = ProjectForm()
        return render_template("new_project.html", form=form, is_edit=False)


if __name__ == "__main__":
    app.run(debug=True)