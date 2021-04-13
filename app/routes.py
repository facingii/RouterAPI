# -*- coding: utf-8 -*-

from flask import request, jsonify
from app import rapi
from app import device

# index
#@rapi.route ('/', methods=['GET'])
#def index ():
#	return "Cisco Routers API Rest"

# get all routers bw
#@rapi.route ('/getall', methods=['GET'])
#def get_all ():
#	pass

# get individual router bw 
@rapi.route ('/getinfo', methods=['GET'])
def get_info ():
	query = request.args
	if not query.get ('ip'): 
		return jsonify (
			{
				"status": "fail",
				"error": "Se debe especificar una dirección IP."
			}
		)

	devices = rapi.config ['DEVICES']
	ip = query.get ('ip')
	if not devices.__contains__(ip):
		return jsonify (
			{
				"status": "fail",
				"error": "La ip especificada no existe."
			}
		)

	foo =  device.get_router_info (ip)
	foo.split ()

	return jsonify (
		{
			"bw": foo[3:]
		}
	)

# set router bandwith
@rapi.route ('/setbw', methods=['POST', 'PUT'])
def set_bw ():
	query = request.args
	if not query.get ('ip'): 
		return jsonify (
			{
				"status": "fail",
				"error": "Se debe especificar una dirección IP."
			}
		)

	devices = rapi.config ['DEVICES']
	ip = query.get ('ip')
	if not devices.__contains__(ip):
		return jsonify (
			{
				"status": "fail",
				"error": "La ip especificada no existe."
			}
		)

	print (request.json)
	if not request.json:
		return jsonify (
			{
				"status": "fail",
				"error": "El cuerpo del mensaje no pudo ser encontrado."
			}	
		)

	json = request.json
	if not json.get ('bw'):
		return jsonify (
			{
				"status": "fail",
				"error": "El ancho de banda debe ser especificado."
			}	
		)

	try:
		print (json.get ('bw'))
		bw = int (json.get ('bw'))
	except:
		return jsonify (
			{
				"status": "fail",
				"error": "El valor especificado no es válido."
			}
		)

	if device.set_bw (ip, bw):
		return jsonify (
			{
				"status": "ok",
				"error": ""
			}
		)
	else: 
		return jsonify (
			{
				"status": "fail",
				"error": "La operación no pudo ser completada."
			}
		)


#handle HTTP 404 error 
@rapi.errorhandler (404)
def page_not_found (e):
	return "<h1>404</404><p>The resource could not be found.</p>", 404