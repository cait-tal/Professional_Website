from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

CURRENT_YEAR = datetime.now().year
@app.route("/")
def redirect_home_page():
    return redirect(url_for("home_page"))

@app.route("/welcome")
def home_page():
    return render_template("main_base.html", year=CURRENT_YEAR)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', year=CURRENT_YEAR), 404

if __name__ == "__main__":
    app.run(debug=True)