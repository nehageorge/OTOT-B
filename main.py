from urllib.parse import urlparse
from api.classes.image import Image
from api.classes.user import User
from flask import Flask, request, redirect
import importlib
import pymongo
import api.databaseconfig as cfg
import sys
import json
import jwt
from bson.json_util import dumps

app = Flask(__name__)

client = pymongo.MongoClient(cfg.client, connect=False)
db = client.NUS
imageCol = db["ImageRepo"]
userCol = db["User"]


@app.route('/<user>/index', methods=['GET'])
def index(user):
	encodedToken = request.headers.get('Authorization')
	if not encodedToken:
		return json_response('User is not authenticated', 401)
	decodedToken = jwt.decode(encodedToken, 'secret', algorithms="HS256")
	if not decodedToken['id']:
		return json_response('User is not authenticated', 401)
	authUser = User.get_by_id(decodedToken['id'], userCol)
	if authUser['username'] != user:
		return json_response('User is not authorized', 403)
	all_images = Image.load_all_images(imageCol, user)
	images = Image.get_images_ready_for_display(all_images)
	res = json_response(images)
	return res


@app.route('/<user>/new_image', methods=['GET','POST'])
def new_image(user):
	if request.method == 'POST':
		name = request.form['name']
		labels = request.form['labels']
		url = request.form['url']

		try:
			img = Image(name, labels, url, user)
			img.add_to_db(imageCol)
		except Exception as e:
			return json_response(str(e), 400)

		return json_response("Image created.", 200)
	else:
		return json_response("")

@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		name = request.form['username']
		password = request.form['password']

		try:
			user = User(name, password)
			user.add_to_db(userCol)
		except Exception as e:
			return json_response(str(e), 400)

		return json_response("Success", 200)
	else:
		return json_response("")

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		name = request.form['username']
		password = request.form['password']

		try:
			token = User.login(name, password, userCol)
		except Exception as e:
			return json_response(str(e), 401)

		return json_response(token, 200)
	else:
		return json_response("")




@app.route('/<user>/get_image/<name>', methods=['GET'])
def get_image(user, name):
	result = Image.get_by_name(imageCol, name)
	if not result: return json_response("Image not found", 400)
	resultDct = dict(result)
	resultDct.pop("_id")
	return json_response(resultDct)
	

@app.route('/<user>/delete_image/<name>', methods=['DELETE'])
def delete_image(user, name):
	try:
		Image.remove_from_db(imageCol, name)
		return json_response("")
	except Exception as e:
		return json_response(str(e), 400)
	

@app.route('/<user>/update_image/<name>', methods=['PUT'])
def update_image(user, name):
	labels = request.json['labels']
	url = request.json['url']

	try:
		Image.update_in_db(imageCol, name, labels, url)
	except Exception as e:
		return json_response(str(e), 400)

	return redirect('/index')

def json_response(payload, status=200):
  return (json.dumps(payload), status, {'content-type': 'application/json'})


if __name__ == '__main__':
	app.run()
