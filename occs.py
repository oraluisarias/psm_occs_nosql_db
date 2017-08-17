#!/usr/bin/env python
#################################################################################
#************************************************************************************************#
# Script: occs.py                                                                                 #
# Usage : GSE - Python wrapper to execute REST calls on Oracle Container Cloud Services            #
# Date                                  Who                           What                       #
#------------------------------------------------------------------------------------------------#
# Oct-2016                           LUISARIA.MX                  Initial Version                #
#------------------------------------------------------------------------------------------------#
import requests, json, os, time, sys, traceback, subprocess, re
import xml.etree.ElementTree

class OCCS:		
	def __init__(self, occs_URL, environment, occs_user, occs_password):
		self.proxies = { }
		self.url = occs_URL
		self.user = occs_user
		self.password = occs_password
		self.environment = environment
		self.login_info = self.login()
		self.auth_bearer = self.login_info["token"]		
		self.token = self.retrieveToken()["token"]

	def getToken(self):
		return self.token

	def getAuthBearer(self):
		return self.auth_bearer
				
	def retrieveToken(self):
		headers = { 'Authorization': "Session " + self.auth_bearer}		
		endpoint = self.url + "/api/token"
		data = { "username" : self.user, "password" : self.password }
		print("Trying to log in with username/password", self.user, self.password, endpoint)
		r = requests.post(endpoint, headers=headers, proxies=self.proxies, verify=False)	
		response = r.text.encode('utf-8').strip()
		print (json.loads(response))
		return json.loads(response)

	def login(self):
		headers = {}		
		endpoint = self.url + "/api/auth"
		data = { "username" : self.user, "password" : self.password }
		print("Trying to log in with username/password", self.user, self.password, endpoint)
		try: 
			r = requests.post(endpoint, proxies=self.proxies, data=json.dumps(data), verify=False)					
			# self.password =  self.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]				
		except: 
			print("Tried to connect to ", endpoint)
			print("Facing network problems or OCCS account is down :(")
			traceback.print_exc(file=sys.stdout)
			sys.exit(1)
		response = r.text.encode('utf-8').strip()
		print (json.loads(response))
		return json.loads(response)
				
	def changeAdminPassword(self, newPassword=False):		
		headers = {"Authorization" : "Bearer " + self.token}		
		endpoint = self.url + "/api/users/admin"
		if newPassword is False : newPassword = self.getRandomPwdDemoCentral()
		data = { 
			"first_name": "GSE",
   			"last_name": "Admin",
			'password': newPassword
		}	
		r = requests.put(endpoint, proxies=self.proxies, data=json.dumps(data), headers=headers, verify=False)		
		print (r.text)			
		data["response"] = json.loads(re.sub('[\s+]', '', r.text))
		return data

	def uploadSnapshot(self, snapshotName):		
		headers = {"Authorization" : "Bearer " + self.token}		
		print ( headers )	
		endpoint = self.url + "/api/v2/import"
		snapshot = { 'upload.bin': ( 'upload.bin', open( snapshotName, 'rb' ) ) }		
		r = requests.post(endpoint, proxies=self.proxies, files=snapshot, headers=headers, verify=False)					
		print ( r.text )	
		return json.loads(re.sub('[\s+]', '', r.text))

	def stopContainer(self, containerId):
		headers = {"Authorization" : "Bearer " + self.token}		
		endpoint = self.url + "/api/v2/containers/" + containerId + "/stop"
		data = { }
		r = requests.post(endpoint, proxies=self.proxies, data=json.dumps(data), headers=headers, verify=False)			
		# return json.loads(r.text.strip())
		return json.loads(re.sub('[\s+]', '', r.text))

	def getAllContainers(self):
		headers = {"Authorization" : "Bearer " + self.token}		
		endpoint = self.url + "/api/containers"
		print (headers)
		r = requests.get(endpoint, proxies=self.proxies, headers=headers, verify=False)
		response_text = r.text
		response_obj = json.loads( response_text )
		print ( response )
		return response

	def createBootableVolume(self,  size, name):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/volume/"
		volume_data = {"size" : size, "name" : name, "properties" : ["/oracle/public/storage/default"]}
		r = requests.post(endpoint, proxies=self.proxies, data=json.dumps(volume_data), headers=headers, verify=False)	
		print ("endpoint: " , endpoint	)
		print( r.text)
		return json.loads(r.text)

	def getContainers(self,  user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+directory+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/imagelist/Compute-" + self.identity_domain + "/" + user + "/"
		r = requests.get(endpoint, proxies=self.proxies, headers=headers, verify=False)	
		print ("endpoint: " , endpoint)	
		print (r.text)
		return json.loads(r.text)
 
	def getRandomPwdDemoCentral(self):
		demo_central_pwd_url = "https://adsweb-ws.oracleads.com/dumservice/common/password?policy=USER_FRIENDLY_PASSWORD_POLICY"
		content = requests.get(demo_central_pwd_url).text
		print (content)
		root = xml.etree.ElementTree.fromstring(content)

		for child in root:
			if child.text is not None:
				return child.text			

	def getImageLists(self,  user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+directory+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/imagelist/Compute-" + self.identity_domain + "/" + user + "/"
		r = requests.get(endpoint, proxies=self.proxies, headers=headers, verify=False)	
		print ("endpoint: " , endpoint)	
		print (r.text)
		return json.loads(r.text)
	
	def getIpAssocs(self,  user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+directory+json"}		
		endpoint = "https://psm.europe.oraclecloud.com/ip/association/"
		r = requests.get(endpoint, proxies=self.proxies, headers=headers, verify=False)	
		print ("endpoint: " , endpoint)	
		print (r.text)
		return json.loads(r.text)

	def getIpReservs(self,  user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+directory+json"}		
		# endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/ip/reservation/"
		endpoint = "https://psm.europe.oraclecloud.com/ip/reservation/"
		r = requests.get(endpoint, proxies=self.proxies, headers=headers, verify=False)	
		print ("endpoint: " , endpoint	)
		print (r.text)
		return json.loads(r.text)