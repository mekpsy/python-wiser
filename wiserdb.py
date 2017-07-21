# -*- coding: utf-8 -*-

import mysql.connector
from pprint import pprint

def db_get_document_id(title) :
    connection = mysql.connector.connect(
        host = "localhost",
        db = "wiser",
        user = "root",
        password = "5efvtw7e"
    )

    cursor = connection.cursor()

    sql = "SELECT id FROM documents WHERE title = %s"
    cursor.execute(sql, (title,))

    row = cursor.fetchone()
    if row is not None :
        return row[0]
    else :
      return 0


def db_get_token_id(str) :
    connection = mysql.connector.connect(
        host = "localhost",
        db = "wiser",
        user = "root",
        password = "5efvtw7e"
    )

    cursor = connection.cursor()

    query = "SELECT id, docs_count FROM tokens WHERE token = %s"
    cursor.execute(query, (str, ))
    row = cursor.fetchone()
    if row is not None :
        info = (row[0], row[1])
    else :
        insert = "INSERT IGNORE INTO tokens (token, docs_count) VALUES (%s, 1)"
        cursor.execute(insert, (str, ))
        connection.commit()

        # 登録したトークンのIDを得る
        cursor.execute(query, (str, ))
        row = cursor.fetchone()
        if row is not None :
            info = (row[0], row[1])
        else :
            info = None

    cursor.close()
    connection.close()

    return info


def db_add_document(title, body) :
    connection = mysql.connector.connect(
        host = "localhost",
        db = "wiser",
        user = "root",
        password = "5efvtw7e"
    )

    cursor = connection.cursor()

    document_id = db_get_document_id(title)
    if document_id != 0 :
        sql = "UPDATE documents set body = %s WHERE id = %s"
        cursor.execute(sql, (body, document_id))
        connection.commit()
    else :
        sql = "INSERT INTO documents (title, body) VALUES (%s, %s)"
        cursor.execute(sql, (title, body))
        connection.commit()

    cursor.close()
    connection.close()


def db_get_postings(token_id) :
    connection = mysql.connector.connect(
        host = "localhost",
        db = "wiser",
        user = "root",
        password = "5efvtw7e"
    )

    cursor = connection.cursor()

    sql = "SELECT docs_count, postings FROM tokens WHERE id = %s"
    cursor.execute(sql, (token_id, ))
    row = cursor.fetchone()
    if row is not None :
        ret = (row[0], row[1])
    else :
        ret = (0, None)

    cursor.close()
    connection.close()

    return ret

def db_update_postings(token_id, docs_count, postings_list) :
    connection = mysql.connector.connect(
        host = "localhost",
        db = "wiser",
        user = "root",
        password = "5efvtw7e"
    )

    cursor = connection.cursor()

    sql ="UPDATE tokens SET docs_count=%s, postings=%s WHERE id=%s"
    cursor.execute(sql, (docs_count, postings_list, token_id))
    connection.commit()

    cursor.close()
    connection.close()

def db_insert_wiki(title, body) :
    connection = mysql.connector.connect(
        host = "localhost",
        db = "wiser",
        user = "root",
        password = "5efvtw7e"
    )

    cursor = connection.cursor()

    insert = "INSERT INTO documents (title, body) VALUES (%s, %s)"
    cursor.execute(insert, (title, body))
    connection.commit()

    cursor.close()
    connection.close()
