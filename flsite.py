import sqlite3
import os


from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'vasdnianvsdnfviuvjvfn'

app = Flask(__name__)
app.config.from_object(__name__)  # ['SECRET_KEY'] = 'thwrthsjdldnahsrtb'

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# menu = [{"name": "Установка", "url": "install-flask"},
#         {"name": "Первое приложение", "url": "first-app"},
#         {"name": "Обратная связь", "url": "contact"}]


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    # print(url_for("index"))
    return render_template("index.html", menu=dbase.getMenu(), posts=dbase.getPostsAnnounce())


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")


@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/about")
def about():
    db = get_db()
    dbase = FDataBase(db)
    print(url_for("about"))
    return render_template("about.html", title="О сайте", menu=dbase.getMenu())


@app.route("/contact", methods=["POST", "GET"])
def contact():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash("Ошибка отправки", category='error')
        print(request.form['username'])

    return render_template("contact.html", title="Обратная связь", menu=dbase.getMenu())


@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=dbase.getMenu())


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Профиль пользователя: {username}"


@app.errorhandler(404)
def pageNotFount(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template("page404.html", title='Страница не найдена', menu=dbase.getMenu()), 404


# @app.route("/profile/<username>")
# def profile(username, path):
#     return f"Пользователь: {username}, {path}"


if __name__ == "__main__":
    app.run(debug=True)
