# -*- coding: utf-8 -*-

try:
  # import
  import mysql.connector
  # 接続
  connect = mysql.connector.connect(user='root', password='5efvtw7e', host='127.0.0.1', database='wiser', charset='utf8')
  # カーソル
  cursor = connect.cursor()
  # SQL 発行
  cursor.execute('select * from documents', ())
  # フェッチ
  rows = cursor.fetchall()
  print(rows)
  cursor.close()
  # 切断
  connect.close()
except Exception as e:
  print(e)
