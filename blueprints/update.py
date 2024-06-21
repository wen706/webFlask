from flask import Blueprint, request, session, g
from flask import render_template, url_for, redirect
import method.sql
update = Blueprint('update', __name__)


# 9B117039
def update_comic_tag(comic_id, tag_id):
    exists = method.sql.sqlite3_read(
        "SELECT * FROM Tag WHERE comicid = ? AND tagid = ?", (comic_id, tag_id))

    if len(exists) == 1:
        method.sql.sqlite3_write(
            "DELETE FROM Tag WHERE comicid = ? AND tagid = ?", (comic_id, tag_id))
    else:
        method.sql.sqlite3_write(
            "INSERT INTO Tag (comicid, tagid) VALUES (?, ?)", (comic_id, tag_id))


@update.route('/update/<int:id>', methods=['GET', 'POST'])
def selected(id):
    if 'username' not in session or session['op'] != 0:
        return redirect(url_for('main.login'))

    if not method.sql.select_comic_exist(id):
        return redirect(url_for('main.update_choose'))

    error = ''
    if request.method == 'POST':
        if request.form['TagType'] != "" and request.form['Tag'] != "":
            tag = request.form['Tag']
            update_comic_tag(id, tag)
            return redirect(url_for('update.selected', id=id))
        else:
            error = '請選擇要新增的標籤'

    data = method.sql.select_comic_tag(id)
    img = f'/comicImg/{id}/1.jpg'
    tag = method.sql.select_all_tag()
    name = method.sql.select_comic_name(id)

    return render_template('update/selected.html', id=id, img=img, data=data, tags_dict=tag, error=error, name=name)


@update.route('/update')
def update_choose():
    if 'username' not in session or session['op'] != 0:
        return redirect(url_for('main.login'))

    query = "SELECT ComicId, ComicName FROM Name"
    select = ()
    search = method.sql.sqlite3_read(query, select)
    return render_template('update/choose.html', comic=search)


@update.route('/rename/<int:id>', methods=['GET', 'POST'])
def re_name(id):
    if 'username' not in session or session['op'] != 0:
        return redirect(url_for('main.login'))

    if not method.sql.select_comic_exist(id):
        return redirect(url_for('main.update_choose'))

    if request.method == 'POST':
        name = request.form['comic_name']
        method.sql.sqlite3_write(
            "UPDATE Name SET ComicName = ? WHERE ComicId = ?", (name, id)
        )

    return redirect(url_for('update.selected', id=id))


@update.route('/newtag', methods=['GET', 'POST'])
def new_tags():
    if 'username' not in session or session['op'] != 0:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        new_tag_type = request.form['new_tag_type']
        tag_str = request.form['tag_str']
        if tag_str != '':
            check = method.sql.sqlite3_read(
                "SELECT * FROM TagString WHERE TagType = ? AND TagStr = ?", (new_tag_type, tag_str))
            if len(check) == 0:
                query = "INSERT INTO TagString (TagType, TagStr) VALUES (?, ?)"
                method.sql.sqlite3_write(query, (new_tag_type, tag_str,))

    return render_template('tag/new.html')
