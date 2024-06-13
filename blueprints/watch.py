from flask import (
    Blueprint,
    session,
    request,
    g,
    render_template,
    url_for,
    redirect,
    send_file,
    abort)
import os
import re
import method.sql
# 創建第一個藍圖
watch = Blueprint('watch', __name__)


@watch.route('/comic/<int:id>/<int:page>', methods=['GET'])
def comic_look(id, page):
    if 'username' not in session:
        return redirect(url_for('main.login'))

    if not method.sql.select_comic_exist(id):
        return redirect(url_for('watch.comic_home'))

    select = "SELECT ComicPage FROM Name WHERE ComicId = ?"
    totopage = method.sql.sqlite3_read(select, (id,))[0]['ComicPage']
    select = "SELECT TagType,TagStr FROM TagString INNER JOIN Tag on Tag.TagId = TagString.TagId WHERE Tag.ComicId = ?"
    data = method.sql.select_comic_tag(id)
    return render_template('watch/comic_watch.html', id=id, page=page, totopage=totopage, data=data)


@watch.route('/comic/<int:id>', methods=['GET'])
def comic_detailed(id):
    if 'username' not in session:
        return redirect(url_for('main.login'))

    if not method.sql.select_comic_exist(id):
        return redirect(url_for('watch.comic_home'))
    select = "SELECT ComicPage FROM Name WHERE ComicId = ?"
    totopage = method.sql.sqlite3_read(select, (id,))[0]['ComicPage']
    select = "SELECT TagType,TagStr FROM TagString INNER JOIN Tag on Tag.TagId = TagString.TagId WHERE Tag.ComicId = ?"
    Tags = method.sql.sqlite3_read(select, (id,))
    data = method.sql.select_comic_tag(id)
    return render_template('watch/comic_detailed.html', id=id, totopage=totopage, data=data)


@watch.route('/comic')
def comic_home():  # url_for('comic.comicHome')
    if 'username' not in session:
        return redirect(url_for('main.login'))

    if len(request.args) > 0:
        param_value = request.args.get('search')
        query = """
            SELECT ComicId, ComicName
            FROM (
                SELECT Name.ComicId, Name.ComicName
                FROM Name
                INNER JOIN Tag ON Tag.ComicId = Name.ComicId
                INNER JOIN TagString ON Tag.TagId = TagString.TagId
                WHERE TagString.TagStr = ?
                
                UNION
                
                SELECT ComicId, ComicName
                FROM Name
                WHERE ComicName LIKE ?
            ) AS combined_results
            ORDER BY ComicId DESC
        """
        select = (param_value, '%' + param_value + '%')
    else:
        query = "SELECT ComicId, ComicName FROM Name ORDER BY ComicId DESC"
        select = ()
    search = method.sql.sqlite3_read(query, select)
    search = [[str(_['ComicId']), _['ComicName']] for _ in search]
    return render_template('watch/comic_home.html', search=search)


@watch.route('/comicImg/<int:id>/<file_name>')
def protected_images(id, file_name):
    if 'username' not in session:
        abort(404)  # 如果用戶未登錄，返回404(為了迷惑有心人士,不然應該是403)
    if not re.match(r'^\d+\.jpg$', file_name):
        abort(404)  # 確保路徑合法
    file_path = os.path.join(g.private, 'comicImg', str(id), file_name)
    # 確保圖片在private內，並且路徑參數是整數

    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return redirect(url_for('main.login'))
