import opc, subprocess, sys, os, occs
identity_domain = sys.argv[1]
recipe_path = sys.argv[2]
upload_file_name = recipe_path + '/nosqldemo-occs-mgr-1_20170713012937.bin'
#identity_domain = "gse00003345"
opcc = opc.Compute( identity_domain, "z11", False )
occs_user = "admin"
occs_password = "Welcome321"
cloud_username = "cloud.admin"
cloud_password = opcc.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]	
container_username = "cloud_admin"

#del os.environ['http_proxy']
#del os.environ['https_proxy']
containers = []
image_found = False

#find image in datacenters to retrieve IP address
print ( "Getting datacenter...", opcc.domain_data )
for domain in opcc.domain_data:
	if image_found: break
	domain_data = opcc.domain_data[domain]	
	opcc.setDataCenter(domain_data["datacenter"].lower().replace('0', ''))
	opcc.setZone(domain_data["zone"].lower())
	opcc.authenticate(False, False, "cloud.admin")
	images = opcc.getInstances("cloud.admin") 
	for instance in images["result"]:		
		i = 0
		parts = instance["name"].split("/")
		print(parts)
		for name_parts in parts:	
			if name_parts == "CONTAINER" and parts[i+2] == "MANAGER":
				print (instance["vcable_id"])
				ip_info = { 
					"container_instance" : parts[i+1], 
					"container_ip" : opcc.getReservedIP(cloud_username, instance["vcable_id"])
				}
				print ( ip_info["container_ip"]["ip"]	 )
				containers.append(ip_info)
			i = i + 1

for container in containers:
	url = "https://" + container["container_ip"]["ip"]	
	api = occs.OCCS(url, identity_domain, occs_user, occs_password)
	print ( "Uploading snapshot" )
	print ( api.uploadSnapshot(upload_file_name) )
