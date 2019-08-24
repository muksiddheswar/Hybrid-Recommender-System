#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 20:23:03 2019

@author: smkj33
"""
import pymysql
from app import app
from db_config import *

from flask import jsonify
from flask import flash, request


# @app.route('/articles')
# def articles():
# 	try:
# 		conn = pymysql.connect(**connection_properties)
# 		cursor = conn.cursor(pymysql.cursors.DictCursor)
# 		cursor.execute("SELECT * FROM recen_article_map")
# 		rows = cursor.fetchall()
# 		resp = jsonify(rows)
# 		resp.status_code = 200
# 		return resp
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close() 
# 		conn.close()

@app.route('/specific')
def get_articles():
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			# conn = mysql.connect()
			# cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		
if __name__ == "__main__":
    app.run()