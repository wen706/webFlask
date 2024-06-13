from flask import (
    Blueprint,
    render_template)

finish = Blueprint('finish', __name__)


@finish.route('/download/finish')
def download_finish():
    return render_template(
        'main/error.html', error_h2="下載完成", error_p="請返回首頁")


@finish.route('/download/fail')
def download_fail():
    return render_template(
        'main/error.html', error_h2="下載失敗", error_p="請返回首頁")


@finish.route('/delete/finish')
def delete_finish():
    return render_template(
        'main/error.html', error_h2="刪除完成", error_p="請返回首頁")


@finish.route('/delete/fail')
def delete_fail():
    return render_template(
        'main/error.html', error_h2="刪除失敗", error_p="請返回首頁")
