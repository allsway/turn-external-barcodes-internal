#!/usr/bin/python
import requests
import sys
import configparser
import logging
import xml.etree.ElementTree as ET

# Returns the API key
def get_key():
	return config.get('Params', 'apikey')

# Returns the Alma API base URL
def get_base_url():
	return config.get('Params', 'baseurl')
	

# gets the high-level user records in batches of {limit}, so that we can retrieve every user record by ID
def get_user_chunk(offset, limit):
	chunk_url = get_base_url() + '/almaws/v1/users?apikey=' + get_key() + '&offset=' + str(offset) + '&limit=' + str(limit);
	response = requests.get(chunk_url)
	if response.status_code == 200:
		return ET.fromstring(response.content)
	else:
		print ('fail: ' + chunk_url)
	

# Calls the individual user API
def get_user_record(id, idtype):
	# do some checks on ID
	user_url = get_base_url() + '/almaws/v1/users/' + id + '?apikey=' + get_key();
	response = requests.get(user_url)
	if response.status_code == 200:
		xml = ET.fromstring(response.content)
		parse_user(xml,id,idtype)
	else:
		print ('failed to get user: ' + user_url)
	
# Iterates to user ID field and changes segment_type to Internal	
def parse_user(xml,userid,idtype):
	switch = False
	for id in xml.findall('user_identifiers/user_identifier'):
		if id.find('id_type').text == idtype:
			switch = True
			print (id.find('id_type').text)
			id.attrib['segment_type'] = 'Internal'
	if switch: # if no ID field to switch, continue
		put_user(xml,userid)
			
# Makes a put request to user API with updated ID fields to internal fields
def put_user(xml,id):
	headers = {"Content-Type": "application/xml"}
	print (id)
	user_url = get_base_url() + '/almaws/v1/users/' + id + '?apikey=' + get_key();
	r = requests.put(user_url,data=ET.tostring(xml),headers=headers)
	print (r.content)
		
	
# parsing configuration file for API information, number of users and the ID type that we are switching to an internal ID type. 	
config = configparser.ConfigParser()
config.read(sys.argv[1]) #reads in parameter file
apikey = config.get('Params', 'apikey')
baseurl = config.get('Params','baseurl')
idtype =  config.get('Params', 'idtype')	
total_users = config.get('Params', 'total')


limit = 5
offset = int(sys.argv[2])
total_users = int(total_users) + int(offset)
print (total_users)
for i in range(offset, int(total_users), limit):
	response = get_user_chunk(i, limit)
	if response:
		for primary_id in response.findall('user/primary_id'):
			print (primary_id.text)
			get_user_record(primary_id.text, idtype)

	print ('i: ' + str(i))
	
	
	
	
	
	
	
	
	
	
	
	
	
