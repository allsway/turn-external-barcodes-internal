#!/usr/bin/python
import requests
import sys
import csv
import configparser
import logging
import re
import xml.etree.ElementTree as ET

# Returns the API key
def get_key():
	return config.get('Params', 'apikey')

# Returns the Alma API base URL
def get_base_url():
	return config.get('Params', 'baseurl')

# Returns the location mapping file, taken from the Alma Migration Form
def get_id_type():
	return config.get('Params', 'idtype')
	
def get_total_users():
	return config.get('Params', 'total')

# gets the high-level user records in batches of 100, so that we can retrieve every user record by ID
def get_user_chunk(offset, limit):
	chunk_url = get_base_url() + '/almaws/v1/users?apikey=' + get_key() + '&offset=' + str(offset) + '&limit=' + str(limit);
	response = requests.get(chunk_url)
	if response.status_code == 200:
		return ET.fromstring(response.content)
	else:
		print ('fail' + chunk_url)
	

# Calls the individual user API
def get_user_barcode(id):
	# do some checks on ID
	user_url = get_base_url() + '/almaws/v1/users/' + id + '?apikey=' + get_key();
	response = requests.get(user_url)
	if response.status_code == 200:
		xml = ET.fromstring(response.content)
		parse_user(xml)
		
	
# Goes to user ID field and calls function to change segment_type to Internal	
def parse_user(xml):
	id_code = get_id_type()
	for ids in xml.findall('user_identifiers/user_identifier'):
		if ids.find('id_type').text == id_code:
			print (ids.find('id_type').text)
	
config = configparser.ConfigParser()
config.read(sys.argv[1]) #reads in parameter file
apikey = config.get('Params', 'apikey')
baseurl = config.get('Params','baseurl')
id =  config.get('Params', 'idtype')	
total_users = config.get('Params', 'total')


limit = 5
for i in range(0, int(total_users), limit):
	response = get_user_chunk(i, limit)
	if response:
		for primary_id in response.findall('user/primary_id'):
			print (primary_id.text)
			barcode = get_user_barcode(primary_id.text)

		
	
	
	
	
	
	
	
	
	
	
	
	
	
