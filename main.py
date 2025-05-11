from flask import Flask, render_template, request, make_response, redirect, url_for
from data.users import User
from data.recipes import Recipe
from data import db_session
import datetime
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

def log_move(name_move, user):
    f = open("static/logs.txt", 'a')
    print(f.write(f'User {user} {name_move} at {datetime.datetime.now()} \n'))
    f.close()

def transliteration(word):
    slob = {
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "E",
        "Ж": "Zh",
        "З": "Z",
        "И": "I",
        "Й": "I",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "Kh",
        "Ц": "Tc",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Shch",
        "Ы": "Y",
        "Э": "E",
        "Ю": "Iu",
        "Я": "Ia",
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "tc",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ы": "y",
        "э": "e",
        "ю": "iu",
        "я": "ia",
    }
    fol = word.split()
    gol = []
    g = len(fol)
    hkl = 0
    for i in fol:
        for j in i:
            if j in slob:
                gol.append(slob[j])
            elif j != "ь" and j != "ъ" and j != 'Ь' and j != 'Ъ':
                gol.append(j)
        hkl += 1
        if hkl != g:
            gol.append(" ")
    return "".join(gol)

@app.route('/', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/index', methods=['GET', 'POST'])
def index_form():
    action = request.form.get("singing")
    if action == "sing_up":
        log_move('is trying to sing_up', 'someone')
        return redirect(url_for("sing_up"))
    if action == "sing_in" :
        log_move('is trying to sing_in', 'someone')
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
        log_move('mistakes at email', username)
        return render_template("error.html", error="Некорректный Email")
    if len(username) < 3 or '/' in username:
        log_move('mistakes at username', username)
        return render_template("error.html", error="Короткий username")
    if len(password) < 3:
        log_move('mistakes at password(too short)', username)
        return render_template("error.html", error="Короткий password")
    if password != password2:
        log_move('mistakes at password(they are different)', username)
        return render_template("error.html", error="Пароли не совпадают")
    db_sess = db_session.create_session()

    if email in [i.email for i in db_sess.query(User).all()]:
        log_move('mistakes at Email(already exist)', username)
        return render_template("error.html", error="Такой Email уже зарегестрирован")

    if username in [i.name for i in db_sess.query(User).all()]:
        log_move('mistakes at Username(already exist)', username)
        return render_template("error.html", error="Такой Username уже зарегестрирован")

    user = User()
    user.name = username
    user.email = email
    user.password = password

    db_sess.add(user)
    db_sess.commit()
    log_move('is sing up', username)
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
        log_move('mistakes at smthg(user is not founded)', username)
        return render_template('error.html', error='Такого пользователя не существует')

    if user.password != password:
        log_move('mistakes at password(password is wrong)', username)
        return render_template('error.html', error='Неправильный пароль')

    db_sess.commit()
    db_sess.close()
    log_move('is sing in', username)
    return redirect(url_for('profile', username=username))


@app.route("/profile/<username>")
def profile(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == str(username)).first()
    # print(user.name, user.image)
    image = user.image

    return render_template('profile.html', username=username, image=image)

@app.route("/recipe_filter/<username>", methods=['GET', 'POST'])
def recipe_filter(username):
    return render_template('recipe_filter.html', username=username)


@app.route("/submit_recipe_filter/<username>", methods=['POST', 'GET'])
def submit_recipe_filter(username):
    if request.form.get('ifexit') == 'exit_':
        log_move('is leaving submit_recipe_filter', 'someone')
        return render_template('profile.html', username=username)
    if request.form.get('search_recipe') == 'search':
        print('dsfapk[jmdpas')
        name = request.form.get('name')
        name1 = transliteration(name)
        description = request.form.get('description')
        products = request.form.getlist('ingredients')
        difficult = request.form.get('recipe_dif')
        type = request.form.getlist('recipe_types')
        needofall = request.form.get('needofall')
        author = username
        db_sess = db_session.create_session()
        recipes1 = db_sess.query(Recipe).all()
        recipes1 = [[i.id, i.name, i.description, i.image, i.author, i.products, i.difficult, i.type] for i in recipes1]
        recipes = []
        log_move(f'is search with this objects - Name: {name}, Products: {products}, Difficult: {difficult}, Type: {type}', username)

        for i in recipes1:
            g = [0, len(products), len(type)]
            goggole = 0
            print(name, i[1])
            if (name.lower() in i[1].lower() or name1.lower() in i[1].lower()) and name:
                goggole += 1
            if difficult and i[6]:
                print(difficult.lower(), i[6])
                if difficult.lower() in i[6].lower():
                    goggole += 1
            if products and i[5]:
                print(products, i[5])
                for j in products:
                    print(j, i[5])
                    if j.lower() in i[5]:
                        goggole += 1
            if type and i[7]:
                print(type, i[7])
                for j in type:
                    print(j, i[7])
                    if j.lower() in i[7].lower():
                        goggole += 1
            print('-----------------------')
            print(goggole)
            if name:
                g[0] += 1
            if difficult:
                g[0] += 1
            print(sum(g))
            print('-----------------------')
            if needofall == 'Yes':
                print('YES')
                if goggole == sum(g):
                    print(goggole)
                    recipes.append(i)
            else:
                if goggole >= 1:
                    recipes.append(i)
        print(recipes)
        log_move(f'is finding these recipes - {recipes}', 'someone')
        return render_template('all_recipes.html', recipes=recipes)


@app.route("/recipe_filter_search", methods=['POST', 'GET'])
def recipe_filter_search():
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipe).all()
    recipes = [[i.id, i.name, i.description, i.image, i.author] for i in recipes]
    # print(recipes)
    return render_template('all_recipes.html', recipes=recipes)



@app.route("/submit_menu_buttons", methods=['POST', 'GET'])
def submit_menu_buttons():
    username = request.form.get("username")
    # print(username)
    if request.form.get("menu-buttons") == "profile":
        log_move('is tap button profile', username)
        return redirect(url_for('my_profile', username
=username))

    if request.form.get("menu-buttons") == "all_recipes":
        log_move('is tap button all_recipes', username)
        return redirect(url_for('all_recipes'))

    if request.form.get("menu-buttons") == "possible_recipes":
        log_move('is tap button possible_recipes', username)
        return redirect(url_for('recipe_filter', username=username))

    if request.form.get("menu-buttons") == "make_recipe":
        log_move('is tap button make_recipe', username)
        return redirect(url_for('make_recipe', username=username))

    if request.form.get("menu-buttons") == "my_recipes":
        log_move('is tap button my_recipes', username)
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
        log_move(f'set new image at their profile - {filename}', username)

        db_sess.commit()

        file.save(os.path.join(IMAGE_FOLDER, filename))

    new_name = request.form.get('username')

    db_sess = db_session.create_session()

    all_names = [i.name for i in db_sess.query(User).filter(User.name != str(username))]

    if new_name not in all_names and new_name:
        log_move(f'set new name at their profile - {new_name}', username)
        user = db_sess.query(User).filter(User.name == str(username)).first()
        user.name = str(new_name)
        db_sess.commit()
    else:
        return render_template('error2.html', error='Такое имя уже существует')

    username = user.name
    log_move('set smthg new at their profile', username)

    return redirect(url_for('profile', username=username))


@app.route("/make_recipe/<username>")
def make_recipe(username):
    return render_template('make_recipe.html', username=username)


@app.route("/submit_make_recipe/<username>", methods=['POST', 'GET'])
def submit_make_recipe(username):
    print(username)
    if request.form.get('make_recipe') == 'make':
        log_move('is trying to make new recipe', username)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == str(username)).first()
        user_id = user.id

        recipe = Recipe()

        recipe.name = request.form.get('name')
        recipe.description = request.form.get('description')
        recipe.products = str(request.form.getlist('ingredients'))
        print(request.form.get('ingredients'))
        recipe.difficult = request.form.get('recipe_dif')
        recipe.type = str(request.form.getlist('recipe_types'))
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
        log_move('add a new recipe', username)
        db_sess.add(recipe)
        db_sess.commit()

    return redirect(url_for('profile', username=username))

@app.route("/all_recipes", methods=['POST', 'GET'])
def all_recipes():
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipe).all()
    recipes = [[i.id, i.name, i.description, i.image, i.author] for i in recipes]
    # print(recipes)
    return render_template('all_recipes.html', recipes=recipes)


@app.route("/submit_all_recipes", methods=['POST', 'GET'])
def submit_all_recipes():
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipe).all()
    recipes = [int(i.id) for i in recipes]
    print(request.form.get('action'))
    print(recipes)
    if int(request.form.get('action')) in recipes:
        recipe = db_sess.query(Recipe).filter(Recipe.id == int(request.form.get('action'))).first()
        log_move(f'tap on recipe {Recipe.id}', 'someone')
        return str(recipe.description)
    return redirect(url_for('all_recipes'))


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    app.run(port=8080, host='127.0.0.1')
