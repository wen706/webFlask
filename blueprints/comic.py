from flask import (
    Blueprint,
    session,
    request,
    g,
    render_template,
    url_for,
    redirect)
import os
import shutil
import method.sql
import requests
from concurrent.futures import ThreadPoolExecutor
# 創建第一個藍圖
comic = Blueprint('comic', __name__)


@comic.route('/confirm')
def before_request():  # 9B117044
    if 'username' not in session or session['op'] != 0:
        return redirect(url_for('main.login'))

    select = method.sql.sqlite3_read("SELECT ComicId FROM Name", ())
    comic_id_set = set([str(row['ComicId']) for row in select])
    comicimg_folder = set(os.listdir(os.path.join(g.private, 'comicImg')))

    if comic_id_set != comicimg_folder:
        for ComicId in comic_id_set - comicimg_folder:
            method.sql.sqlite3_write(
                "DELETE FROM Name WHERE ComicId = ?", (ComicId,))
        for comicid in comicimg_folder - comic_id_set:
            files = os.listdir(os.path.join(g.private, 'comicImg', comicid))
            if len(files) != 0:
                method.sql.sqlite3_write(
                    "INSERT INTO Name (ComicId, ComicName,ComicPage) VALUES (?, ?, ?)",
                    (comicid, '未命名', len(files)))
            else:
                shutil.rmtree(files)

    select = method.sql.sqlite3_read("SELECT ComicId FROM Name", ())
    comic_id_list = sorted([int(row['ComicId']) for row in select])

    # 重新排列 ComicId，從 1 開始
    new_id = 1
    for old_id in comic_id_list:
        if new_id != old_id:
            method.sql.sqlite3_write(
                "UPDATE Name SET ComicId = ? WHERE ComicId = ?", (new_id, old_id))

            old_folder = os.path.join(g.private, 'comicImg', str(old_id))
            new_folder = os.path.join(g.private, 'comicImg', str(new_id))
            os.rename(old_folder, new_folder)
        new_id += 1
    return redirect(url_for('watch.comic_home'))


@comic.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'username' not in session or session['op'] != 0:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        comic_id = request.form['comic_id']

        if os.path.exists(os.path.join(g.private, 'comicImg', str(comic_id))):
            shutil.rmtree(os.path.join(g.private, 'comicImg', str(comic_id)))
        method.sql.sqlite3_write(
            "DELETE FROM Name WHERE ComicId = ?", (comic_id,))
        return redirect(url_for('finish.delete_finish'))
    return redirect(url_for('finish.delete_fail'))


@comic.route('/download', methods=['GET', 'POST'])
def download_comic():
    if 'username' not in session or session['op'] != 0:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        comic_id = request.form['comic_id']
        comic_name = request.form['comic_name']
        comic_web = request.form['comic_web']
        comic_page = int(request.form['comic_page'])
        return 下載漫畫(comic_web, comic_id, comic_name, comic_page)

    return render_template('comic/download.html')


comic_website_url = {}
comic_website_url["nhentai"] = [
    "https://i3.nhentai.net/galleries/", "/{}.jpg"]
comic_website_url["nhentai(png)"] = [
    "https://i3.nhentai.net/galleries/", "/{}.jpg"]


def 下載漫畫(target_url, id, name, max_comic_page):
    """
    下載
    """
    # 下載圖片的函式
    def download_image(image_number):
        nonlocal max_comic_page
        image_url = url.format(image_number)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(DIR+f"/{image_number}.jpg", "wb") as f:
                f.write(response.content)
        else:
            max_comic_page = min(image_number-1, max_comic_page)
    # 理論上進不去
    if target_url not in comic_website_url:
        return
    # 找一個不存在的資料夾並建立
    dir = method.sql.select_comic_max_id()+1
    DIR = os.path.join(g.private, 'comicImg', str(dir))
    os.mkdir(DIR)
    # 開始下載
    url = comic_website_url[target_url][0]+id+comic_website_url[target_url][1]
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(download_image, range(1, max_comic_page+1))
    #
    if len(os.listdir(DIR)) != max_comic_page or len(os.listdir(DIR)) == 0:
        shutil.rmtree(DIR)
        return redirect(url_for("finish.download_fail"))
    comic_data = (dir, name, max_comic_page)
    method.sql.sqlite3_write(
        "INSERT INTO Name (ComicId, ComicName,ComicPage) VALUES (?, ?, ?)", comic_data)
    return redirect(url_for("finish.download_finish"))
