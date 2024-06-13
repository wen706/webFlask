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
    loginState = 0
    if 'username' in session:
        loginState = 1
    return render_template('main/home.html', login=loginState)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        _ = method.sql.sqlite3_read(
            'SELECT * FROM users WHERE username= ? AND password = ? ', (username, password,))
        if len(_) == 1:
            session['username'] = username
            return redirect(url_for('main.home'))
        else:
            return render_template('main/login.html', error='登入失敗')
    return render_template('main/login.html')


@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.home'))
