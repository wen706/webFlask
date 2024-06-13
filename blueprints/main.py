import method.sql
from flask import (
    Blueprint,
    request,
    session,
    g,
    render_template,
    url_for,
    redirect)
# 創建第一個藍圖
main = Blueprint('main', __name__)


@main.route('/')
def home():
    if len(method.sql.sqlite3_read('SELECT * FROM users ', ())) == 0:
        return redirect(url_for('main.new_user'))

    loginState = 0
    if 'username' in session:
        loginState = session['op']+1
    return render_template('main/home.html', login=loginState)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if len(method.sql.sqlite3_read('SELECT * FROM users ', ())) == 0:
        return redirect(url_for('main.new_user'))

    if 'username' in session:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        _ = method.sql.sqlite3_read(
            'SELECT * FROM users WHERE username= ? AND password = ? ', (username, password,))
        if len(_) == 1:
            session['username'] = username
            session['op'] = _[0]["op"]
            return redirect(url_for('main.home'))
        else:
            return render_template('main/login.html', error='登入失敗')
    return render_template('main/login.html')


@main.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if 'username' in session and session['op'] != 0:
        return redirect(url_for('main.home'))

    amount_of_users = len(method.sql.sqlite3_read('SELECT * FROM users ', ()))
    if amount_of_users != 0 and session['op'] != 0:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        op = 1
        if amount_of_users == 0:
            op = 0

        if password != password_confirm:
            return render_template('main/new_user.html', error='密碼請一致')

        if len(method.sql.sqlite3_read('SELECT * FROM users WHERE username= ? ', (username,))) == 1:
            return render_template('main/new_user.html', error='已有此用戶')

        method.sql.sqlite3_write(
            "INSERT INTO users (username, password, op) VALUES (?,?,?)",
            (username, password, op,))

        return redirect(url_for('main.login'))

    return render_template('main/new_user.html')


@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.home'))
