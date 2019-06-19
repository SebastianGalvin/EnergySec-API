# Made by Sebastian Galvin
# Made for EnergySec staff to help automate repetitive tasks
# Project started 6/14/19

# Imports
from flask import Flask, request
from flask_restful import reqparse, abort, Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import mysql.connector
import subprocess

# Open credentials file to get credentials for MySQL
f = open('credentials.txt', "r")
lines = f.readlines()
ESusername = lines[0]
ESpassword = lines[1]

# Define Tables in DB
add_member = ("INSERT INTO members "
			 "(domains, company) "
			 "VALUES (%s, %s)")


# Define App and API
app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True

# API Functions

class ImportEventbrite(Resource):
	def post(self, first, last, email, event):
		'''
			1. run on event end.
			2. get information on all attendees.
			3. add attendees into infusionsoft.
		'''
		pass

class PTOCheck(Resource):
	def get(self, user):
		'''
			1. Search user in database.
			2. return PTO of user.
		'''
		pass

class AddCommunityUser(Resource):
	def post(self, first, last, email, tags):
		'''
			1. Add user to Azure AD.
			2. Add to proper groups using tags.
		'''
		subprocess.call(["Script Location -{first} -{last} -{email}"])

class AddEmployee(Resource):
	def post(self, first, last):
		pass

@app.route('/addMember', methods=['POST'])
def addMember():

	company = request.args.get('company')
	domains = request.args.get('domains')


	cnx = mysql.connector.connect(user=ESusername, password=ESpassword, host='127.0.0.1', database='energysecapi')
	cursor = cnx.cursor()

	data_member = (domains, company)

	cursor.execute(add_member, data_member)
	
	cnx.commit()

	cursor.close()
	cnx.close()

	returned_string = company + ' was succesfully added with domains: ' + domains

	return jsonify(returned_string)

@app.route('/MemberCheck', methods=['GET'])
def memberCheck():
	companies = ''
	cnx = mysql.connector.connect(user=ESusername, password=ESpassword, host='127.0.0.1', database='energysecapi')
	cursor = cnx.cursor()

	query = ("SELECT company, domains FROM members WHERE id BETWEEN 0 AND 1000")
	cursor.execute(query)

	for (domain, company) in cursor:
		companies += '{company} is an EnergySec member with domains: {domains} \n'

	return jsonify(companies)

	cursor.close()
	cnx.close()

app.run()