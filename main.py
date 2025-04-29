from flask import Flask, render_template, request, make_response, redirect, url_for
from data.users import User
from data import db_session

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/index', methods=['GET', 'POST'])
def index_form():
    action = request.form.get("singing")
    if action == "sing_up":
        return redirect(url_for("sing_up"))
    if action == "sing_in":
        return redirect(url_for("sing_in"))


@app.route("/sing_up")
def sing_up():
    return render_template('sing_up.html')


@app.route("/sing_in")
def sing_in():
    return render_template('sing_in.html')


@app.route("/submit_sing_up", methods=['POST', 'GET'])
def submit_sing_up():
    if request.form.get("submit_sing_up") == "go_to_sing_in":
        return redirect(url_for('sing_in'))

    if request.form.get("submit_sing_up") == "exit":
        return redirect(url_for('index'))

    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("confirm_password")
    if "@" not in email or len(email) < 5:
        return render_template("error.html", error="Некорректный Email")
    if len(username) < 3 or '/' in username:
        return render_template("error.html", error="Короткий username")
    if len(password) < 3:
        return render_template("error.html", error="Короткий password")
    if password != password2:
        return render_template("error.html", error="Пароли не совпадают")
    db_sess = db_session.create_session()

    if email in [i.email for i in db_sess.query(User).all()]:
        return render_template("error.html", error="Такой Email уже зарегестрирован")

    if username in [i.name for i in db_sess.query(User).all()]:
        return render_template("error.html", error="Такой Username уже зарегестрирован")

    user = User()
    user.name = username
    user.email = email
    user.password = password

    db_sess.add(user)
    db_sess.commit()

    return redirect(url_for('profile', username=username))


@app.route("/submit_sing_in", methods=['POST', 'GET'])
def submit_sing_in():
    if request.form.get("submit_sing_in") == "go_to_sing_up":
        return redirect(url_for('sing_up'))

    if request.form.get("submit_sing_in") == "exit":
        return redirect(url_for('index'))

    username = request.form.get("username")
    password = request.form.get("password")

    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.name == username).first()
    if not user:
        return render_template('error.html', error='Такого пользователя не существует')

    if user.password != password:
        return render_template('error.html', error='Неправильный пароль')

    db_sess.commit()

    return redirect(url_for('profile', username=username))


@app.route("/profile/<username>")
def profile(username):
    return render_template('profile.html', username=username)


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    app.run(port=8080, host='127.0.0.1')
