from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from API.models import ImageModel
from .models import BiometricSystemModel, RecordModel, User, BioSystemForm
import requests
import os
import signal
import json
import subprocess
import socket
import sys   
import logging
from django.contrib.auth.decorators import user_passes_test


test = False

logging.basicConfig(filename='logs/subsystem.log',format='%(asctime)s %(message)s',level=logging.DEBUG)
logging.info("start")

# superadmin only
@user_passes_test(lambda u: u.is_superuser)
def initSystem(request, bioId):
	bioModel = BiometricSystemModel.objects.get(id=bioId)
	portNum = bioModel.portNum
	if portNum == None:
		# set a default value
		portNum = 12346
	# first kill process in the port
	killProByPort(portNum)
	mlmodelPath = ''
	if bioModel.machineLModel.name != '':
		mlmodelPath = bioModel.machineLModel.path
	# command2 = 'python ' + bioModel.script.path + ' ' + str(portNum) + ' ' + bioModel.machineLModel.path
	command = ['python',"-u", bioModel.script.path, bioId, str(portNum), mlmodelPath]
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1, shell=False)
	
	for nextline in iter(p.stdout.readline, ""):
		print("nl:"+nextline)
		if (nextline == ''):
			break
		# logging.info(str(nextline).rstrip())
		if 'socket is listening' in nextline:
			break
	#the real code does filtering here
	
	bioModel.isStarted = True
	bioModel.save()
	message = 'Initialized {} in pid {} with port {} ......'.format(bioModel.name, p.pid, portNum)
	q = QueryDict('message=' + message)
	return HttpResponseRedirect('/subsystem?' + q.urlencode())
	# return HttpResponse('initializing {} in pid {} with port {} ......'.format(bioModel.name, p.pid, portNum))

# superadmin only
@user_passes_test(lambda u: u.is_superuser)
def stopSystem(request, bioId):
	bioModel = BiometricSystemModel.objects.get(id=bioId)
	portNum = bioModel.portNum
	if portNum == None:
		# set a default value
		portNum = 12346
	killProByPort(portNum)
	bioModel.isStarted = False
	bioModel.save()
	message = 'Stopping {} with port {} ......'.format(bioModel.name, portNum)
	q = QueryDict('message=' + message)
	return HttpResponseRedirect('/subsystem?' + q.urlencode())
	# return HttpResponse('Stopping {} with port {} ......'.format(bioModel.name, portNum)) 

# kill the process listening to the port
def killProByPort(portNum):
	pid = getPidByPort(portNum)
	if pid > 0:
		os.kill(pid, signal.SIGTERM)
		print('stop pid: {}'.format(pid))

# get the id of process listening to the port
def getPidByPort(port):
	retVal = -1
	try:
		command = "lsof -i :%s | awk '{print $2}'" % port
		if sys.platform == 'win32':
			command = 'netstat -ano | findstr "%s"' % (str(port) + " listening")
		pidStr = subprocess.check_output(command, shell=True)
		pidStr = pidStr.strip().decode('utf-8')
		if sys.platform == 'win32':
			pidStr = pidStr.replace(" ", "|")
			pidArr = pidStr.split('|')
			retVal = int(pidArr[len(pidArr)-1])
		else:
			retVal = int(pidStr.split('\n')[1])
	except:
		pass
	return retVal
   
@csrf_exempt 
def connectSystem(request, bioId, userId):
	response_data = {}	
	subsys_data = {
      'userId': userId
   	}
	userModel = User.objects.get(id=userId)
	if not test:
		imageModel = ImageModel(title=request.POST.get('title'),image=request.FILES.get('image'))
		imageModel.save()
	bioModel = BiometricSystemModel.objects.get(id=bioId)
	if bioModel.needName:
		subsys_data['name'] = request.POST.get('name')
	s = socket.socket() 
	#port number for the corresponding bioModel 
	port = bioModel.portNum
	if port == None:
		# set a default value
		port = 12346              
	s.connect(('127.0.0.1', port))
	# send image path
	if test:
		subsys_data['imagePath'] = "file://image.jpg"
		json_data = json.dumps(subsys_data, sort_keys=False, indent=2)
		s.send(json_data.encode("utf-8"))
		# s.send(b"image path....")
	else:
		subsys_data['imagePath'] = imageModel.image.path
		json_data = json.dumps(subsys_data, sort_keys=False, indent=2)
		s.send(json_data.encode("utf-8"))
		# s.send(imageModel.image.path.encode("utf-8")) 
	# receive prediction result from the server 
	result = s.recv(4096).decode("utf-8")
	json_result = json.loads(result)
	processTime = json_result["processTime"]
	isAccepted = json_result["isAccepted"]
	if processTime == None:
		processTime = 0
	# close the connection 
	s.close() 
	if not test:
		recordModel = RecordModel(user=userModel, image=imageModel, biometricSystem=bioModel, result=result, processTime=processTime, isAccepted=isAccepted)
		recordModel.save()
	response_data['result'] = json_result
	return  JsonResponse(response_data)

# superadmin only
@user_passes_test(lambda u: u.is_superuser)
def openSubsystemAdmin(request):
	message = ''
	message = request.GET.get('message', None)
	all_subsystems = BiometricSystemModel.objects.all()
	return render(request, 'subsystem.html', {'subsystems': all_subsystems, 'message': message})

# superadmin only
@user_passes_test(lambda u: u.is_superuser)
def openSubsystemLog(request, bioId):
	fileName = 'subsystem-' + bioId + '.log'
	file_ = open(os.path.join(settings.LOG_ROOT, fileName), 'r')
	content = file_.read()
	return render(request, 'log.html', {'content': content})

# superadmin only
@user_passes_test(lambda u: u.is_superuser)
def bioSystemAddEdit(request, bioId):
	message = ''
	if request.method == "POST":
		# create or update
		# get object: update
		# get DoesNotExist: create
		try:
			instance = BiometricSystemModel.objects.get(id=bioId)
		except BiometricSystemModel.DoesNotExist:
			instance = None
		form = BioSystemForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			bioSystem = form.save()
			message = 'The Biometric System is saved successfully!'
			q = QueryDict('message=' + message)
			return HttpResponseRedirect('/subsystem?' + q.urlencode())
	else:
		try:
			bioSystem = BiometricSystemModel.objects.get(id=bioId)
		except BiometricSystemModel.DoesNotExist:
			bioSystem = BiometricSystemModel(id=bioId)
		form = BioSystemForm(initial=model_to_dict(bioSystem))
    
	return render(request, 'subsystemAddEdit.html', {'form': form, 'message': message})

# superadmin only
@user_passes_test(lambda u: u.is_superuser)
def bioSystemDelete(request, bioId):
    bioSystem = BiometricSystemModel.objects.get(id=bioId)
    bioSystemName=bioSystem.name
    bioSystem.delete()
    message = bioSystemName + ' ' + 'Deleted'
    q = QueryDict('message=' + message)
    return HttpResponseRedirect('/subsystem?' + q.urlencode())

# superadmin only
@user_passes_test(lambda u: u.is_superuser)
def downloadTemplate(request):
	path = 'Subsystem/subsystemTemplate.py'
	file_path = os.path.join(settings.BASE_DIR, path)
	print(file_path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	raise Http404



