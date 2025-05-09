from flask import Flask, render_template, request, make_response, redirect, url_for
from data.users import User
from data.recipes import Recipe
from data import db_session
import os

app = Flask(__name__)

IMAGE_FOLDER = 'static/img/images-of-users'
IMAGE_RECIPE_FOLDER = 'static/img/images-of-recipes'
recipes = [{
    "id": 12,
    "name": 'wtf',
    "description": None,
    "image_url": f"/static/uploads/{None}"}]

def allowed_file(filename):
    return filename.count('.') == 1 and filename.split('.')[1].lower() in ['png', 'jpg', 'jpeg']


@app.route('/', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/all_recipes', methods=['GET', 'POST'])
def all_recipes():
    return render_template('all_recipes1.html', recipes=recipes)


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
    db_sess.close()

    return redirect(url_for('profile', username=username))


@app.route("/profile/<username>")
def profile(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == str(username)).first()
    # print(user.name, user.image)
    image = user.image
    return render_template('profile.html', username=username, image=image)


@app.route("/submit_menu_buttons", methods=['POST', 'GET'])
def submit_menu_buttons():
    username = request.form.get("username")
    # print(username)
    if request.form.get("menu-buttons") == "profile":
        return redirect(url_for('my_profile', username
=username))

    if request.form.get("menu-buttons") == "all_recipes":
        return redirect(url_for('all_recipes'))

    if request.form.get("menu-buttons") == "possible_recipes":
        return redirect(url_for('index'))

    if request.form.get("menu-buttons") == "make_recipe":
        return redirect(url_for('make_recipe', username=username))

    if request.form.get("menu-buttons") == "my_recipes":
        return redirect(url_for('index'))


@app.route("/my_profile/<username>")
def my_profile(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == str(username)).first()
    image = user.image
    db_sess.close()
    return render_template('my_profile.html', username=username, image=image)


@app.route("/set_profile/<username>", methods=['POST', 'GET'])
def set_image(username):
    file = request.files['image']

    if file.filename != '':

        if not allowed_file(file.filename):
            return render_template('error2.html', error='файл не соответствует формату(png, jpg, jpeg)')

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == str(username)).first()

        filename = f'image_{user.id}.png'

        user.image = f'/{IMAGE_FOLDER}/{filename}'
        db_sess.commit()

        file.save(os.path.join(IMAGE_FOLDER, filename))

    new_name = request.form.get('username')

    db_sess = db_session.create_session()

    all_names = [i.name for i in db_sess.query(User).filter(User.name != str(username))]

    if new_name not in all_names and new_name:
        user = db_sess.query(User).filter(User.name == str(username)).first()
        user.name = str(new_name)
        db_sess.commit()
    else:
        return render_template('error2.html', error='Такое имя уже существует')

    username = user.name

    return redirect(url_for('profile', username=username))


@app.route("/make_recipe/<username>")
def make_recipe(username):
    return render_template('make_recipe.html', username=username)


@app.route("/submit_make_recipe/<username>", methods=['POST', 'GET'])
def submit_make_recipe(username):
    print(username)
    if request.form.get('make_recipe') == 'make':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == str(username)).first()
        user_id = user.id

        recipe = Recipe()

        recipe.name = request.form.get('name')
        recipe.description = request.form.get('description')
        recipe.author = username

        file = request.files['image']

        if file.filename != '':
            if not allowed_file(file.filename):
                return render_template('error2.html', error='файл не соответствует формату(png, jpg, jpeg)')
            filename = f'image_{len(db_sess.query(Recipe).all()) + 1}.png'
            recipe.image = f'/{IMAGE_RECIPE_FOLDER}/{filename}'
            file.save(os.path.join(IMAGE_RECIPE_FOLDER, filename))
        else:
            recipe.image = f'/static/img/none_image.png'

        db_sess.add(recipe)
        db_sess.commit()

    return redirect(url_for('profile', username=username))


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    app.run(port=8080, host='127.0.0.2')
