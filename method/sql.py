import sqlite3
import os


def sqlite3_read(query: str, select: tuple) -> list:
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.dirname(path)
    sql = os.path.join(path, 'library.db')
    conn = sqlite3.connect(sql)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, select)
    _ = c.fetchall()
    conn.close()
    return _


def sqlite3_write(query: str, select: tuple):
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.dirname(path)
    sql = os.path.join(path, 'library.db')
    conn = sqlite3.connect(sql)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")  # 啟用外鍵約束
    c.execute(query, select)
    conn.commit()
    conn.close()


def select_all_comic() -> list:
    """
    尋找所有漫畫id+name
    """
    query = "SELECT ComicId, ComicName FROM Name"
    select = ()
    search = sqlite3_read(query, select)
    return search


def select_comic_tag(Comid: int) -> dict:
    """
    尋找漫畫目前標籤
    """
    select = "SELECT TagType,TagStr FROM TagString INNER JOIN Tag on Tag.TagId = TagString.TagId WHERE Tag.ComicId = ?"
    Tags = sqlite3_read(select, (Comid,))
    data = {}
    data['Role'] = [_['TagStr'] for _ in Tags if _['TagType'] == 'Role']
    data['Tag'] = [_['TagStr'] for _ in Tags if _['TagType'] == 'Tag']
    data['Series'] = [_['TagStr'] for _ in Tags if _['TagType'] == 'Series']
    return data


def select_all_tag() -> dict:
    """
    尋找全部標籤
    """
    select = "SELECT TagId,TagType,TagStr FROM TagString"
    Tags = sqlite3_read(select, ())
    Tag = {}
    Tag['Role'] = [{'TagStr': _['TagStr'], 'TagId': _['TagId']}
                   for _ in Tags if _['TagType'] == 'Role']
    Tag['Tag'] = [{'TagStr': _['TagStr'], 'TagId': _['TagId']}
                  for _ in Tags if _['TagType'] == 'Tag']
    Tag['Series'] = [{'TagStr': _['TagStr'], 'TagId': _['TagId']}
                     for _ in Tags if _['TagType'] == 'Series']
    return Tag


def select_comic_exist(Comid: int) -> bool:
    """
    漫畫存在
    """
    select = "SELECT * FROM Name WHERE ComicId = ?"
    Tags = sqlite3_read(select, (Comid,))
    if len(Tags) == 1:
        return True
    else:
        return False


def select_comic_name(Comid: int) -> str:
    """
    漫畫名稱
    """
    select = "SELECT * FROM Name WHERE ComicId = ?"
    Tags = sqlite3_read(select, (Comid,))
    return Tags[0]["ComicName"]


def select_comic_max_id() -> int:
    """
    漫畫名稱
    """
    select = "SELECT * FROM Name ORDER BY ComicId DESC LIMIT 1"
    Tags = sqlite3_read(select, ())
    return int(Tags[0]["ComicId"])


def init_db():

    # Create tables
    sqlite3_write('''
    CREATE TABLE IF NOT EXISTS Name (
        ComicId INTEGER PRIMARY KEY,
        ComicName TEXT NOT NULL,
        ComicPage INTEGER NOT NULL
    )
    ''', ())

    sqlite3_write('''
    CREATE TABLE IF NOT EXISTS TagString (
        TagId INTEGER PRIMARY KEY,
        TagType TEXT NOT NULL,
        TagStr TEXT NOT NULL
    )
    ''', ())

    # 因為外部鍵所以在Name,TagString後面
    sqlite3_write('''
    CREATE TABLE IF NOT EXISTS Tag (
        ComicId INTEGER,
        TagId INTEGER,
        FOREIGN KEY(ComicId) REFERENCES Name(ComicId) 
                  ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(TagId) REFERENCES TagString(TagId) 
                  ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY(ComicId, TagId)
    )
    ''', ())

    sqlite3_write('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        op INTEGER NOT NULL
    )
    ''', ())
