from flask import Flask, render_template, request, make_response
from data.users import User
from data import db_session

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/sing_up")
def sing_up():
    return render_template('sing_up.html')


@app.route("/sing_in")
def sing_in():
    return render_template('sing_in.html')


@app.route("/submit_sing_up", methods=['POST', 'GET'])
def submit_sing_up():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("confirm_password")
    if "@" not in email or len(email) < 5:
        return render_template("error.html", error="Плохой Email")
    if len(username) < 3 or '/' in username:
        return render_template("error.html", error="Короткий username")
    if len(password) < 3:
        return render_template("error.html", error="Короткий password")
    if password != password2:
        return render_template("error.html", error="Пароли не совпадают")


    user = User()
    user.name = username
    user.email = email
    user.hashed_password = password
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    return f"Спасибо, за регистрацию {username}!"


@app.route("/submit_sing_in", methods=['POST', 'GET'])
def submit_sing_in():
    username = request.form.get("username")
    password = request.form.get("password")

    return f"Спасибо, за регистрацию {username}!"



if __name__ == '__main__':
    db_session.global_init('db/db.db')
    app.run(port=8080, host='127.0.0.1')
