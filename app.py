from flask import Flask, render_template, session, redirect, url_for, request, g
from blueprints import register_blueprints
import os
import method.sql
app = Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key = 'regogkeogko'
register_blueprints(app)

app_dir = os.path.abspath(os.path.dirname(__file__))

method.sql.init_db()  # 初始化

os.makedirs(os.path.join(app_dir, 'private', 'comicImg'), exist_ok=True)


@app.before_request
def before_request():
    # 在每次請求之前設置共享變數
    g.private = os.path.join(app_dir, 'private')
    g.public = os.path.join(app_dir, 'public')
    g.SQL = os.path.join(app_dir, 'library.db')


@app.errorhandler(404)
def not_found_error(error):
    errorBeginning = '錯誤'
    errorMessage = '沒有這個網頁'
    return render_template(
        'main/error.html', error_h2=errorBeginning, error_p=errorMessage), 404


@app.errorhandler(500)
def internal_error(error):
    errorBeginning = '錯誤'
    errorMessage = '無法回應你的請求'
    return render_template(
        'main/error.html', error_h2=errorBeginning, error_p=errorMessage), 500


if __name__ == '__main__':
    app.run(debug=True)
