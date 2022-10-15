import pymongo
import bcrypt
import jwt
from urllib.parse import urlparse
from bson.objectid import ObjectId

class User():
	def __init__(self, name, password):
		if not(name and password):
			raise ValueError("Input validation failed. Username and password required.")

		self.username = name

		salt = bcrypt.gensalt()
		hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
		self.password = hashed

	@staticmethod
	def get_by_name(col, name):
		query = { "username" : name }
		result = col.find_one(query)
		return result
	
	@staticmethod
	def get_by_id(id, col):
		query = { "_id" : ObjectId(id) }
		result = col.find_one(query)

		if result is None:
			raise ValueError("User not found") 
		
		return result
		

	@staticmethod
	def login(name, password, col):
		query = { "username" : name }
		result = col.find_one(query)

		if result is None:
			raise ValueError("Username not found") 
		
		hashedPw = result['password']
		isSuccess = bcrypt.hashpw(password.encode('utf-8'), hashedPw) == hashedPw

		if not isSuccess:
			raise ValueError("Password is incorrect") 

		userForToken = {
			'username': name,
			'id': str(result['_id']),
		}

		encoded_jwt = jwt.encode(userForToken, 'secret', algorithm='HS256')

		return encoded_jwt


	def add_to_db(self, col):
		if col.find_one({"username" : self.username}) is not None:
			raise ValueError("User with this username already exists. Unique name required.") 

		document = {
			'username': self.username,
			'password': self.password
		}

		result = col.insert_one(document)
		return result