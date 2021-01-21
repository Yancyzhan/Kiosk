# first of all import the socket library 
import socket                
import time
import sys
import json
import logging

subsys_id = sys.argv[1]
log_name = "logs/subsystem-" + subsys_id + ".log"

#logging setup 
logging.basicConfig(filename=log_name,format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

error_status = -1
success_status = 1

# reserve a port on your computer
# port is got from argument, if not, set it to be 12346
portArg = sys.argv[2]
try:
	port = int(portArg)
except:
	port = 12346

# next create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
print ("Socket successfully created")
logging.info('Socket successfully created')

start_time = time.time()
# import other libraries needed for this subsystem
#--------------------------------------------------

#--------------------------------------------------

mlModelPath = sys.argv[3]
#load machine learning model here...
#--------------------------------------------------

#--------------------------------------------------

print("--- it takes %s seconds to initialize the system ---" % (time.time() - start_time))  
logging.info("it takes %s seconds to initialize the system" % (time.time() - start_time))
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
# If we would have passed 127.0.0.1 
# then it would have listened to 
# only those calls made within the local computer.
s.bind(('127.0.0.1', port))          
print ("socket binded to %s" %(port)) 
logging.info("socket binded to %s" %(port))
# put the socket into listening mode
# 50 here means that 50 connections are kept waiting if the server is busy
# and if a 51st socket trys to connect then the connection is refused. 
s.listen(50)      
print ("socket is listening")            
logging.info("socket is listening")
# a forever loop until we interrupt it or  
# an error occurs 
while True:
	# do not put any print('') in this while loop!!!!
	# It may break the subsystem in some machine !!!!
	data = {
		'subsystemId':subsys_id,
		'status': success_status
	}
	isAccepted = True
	userName = "test"
	try:
		# Establish connection with client. 
		c, addr = s.accept() 
		connect_time = time.time()     
		logging.info('Got connection from %s', addr)

		request_data = c.recv(4096).decode("utf-8")
		json_request = json.loads(request_data)
		image_path = json_request["imagePath"]

		logging.info("predicting.....")

		#prediction part...
		#need to update isAccepted and userName here based on the prediction result...
		#--------------------------------------------------

		#isAccepted = True or False
		#userName = ...
		#--------------------------------------------------

		data['isAccepted'] = isAccepted
		data['name'] = userName
		
	except Exception as e:
		data["status"] = error_status
		data['error message'] = e
		logging.error("ERROR during prediction: %s", e)
		data['isAccepted'] = False
	else:
		logging.info("prediction succeed!")

	# calculate the prediction process time
	process_time = time.time() - connect_time
	# send result message to the client
	data['processTime'] = process_time
	json_data = json.dumps(data, sort_keys=False, indent=2)
	c.send(json_data.encode("utf-8"))
	logging.info("prediction result sent: %s",json_data)  
	# Close the connection with the client 
	c.close()
	logging.info("close user socket")

