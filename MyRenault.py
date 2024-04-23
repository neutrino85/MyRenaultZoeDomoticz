#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#sudo apt install python3-pip
#sudo pip install aiohttp
#
import asyncio
import aiohttp
import json
import urllib
import sys
import ast


async def get_gigyasession(session, gigyarooturl, gigyaapikey, loginID, password):
	payload = {'loginID': loginID, 'password': password, 'apiKey': gigyaapikey}
	url = gigyarooturl + '/accounts.login?' + urllib.parse.urlencode(payload)
	#print(url)
	async with session.get(url) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_gigyaaccount(session, gigyarooturl, gigyaapikey, gigyacookievalue):
	#payload = {'oauth_token': gigyacookievalue}
	payload = {'login_token': gigyacookievalue, 'ApiKey':gigyaapikey}
	url = gigyarooturl + '/accounts.getAccountInfo?' + urllib.parse.urlencode(payload)
	#print(url)
	async with session.get(url) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_gigyajwt(session, gigyarooturl, gigyaapikey, gigyacookievalue):
	#payload = {'oauth_token': gigyacookievalue, 'fields': 'data.personId,data.gigyaDataCenter', 'expiration': 900}
	payload = {'login_token': gigyacookievalue, 'ApiKey':gigyaapikey, 'fields': 'data.personId,data.gigyaDataCenter', 'expiration': 900}
	url = gigyarooturl + '/accounts.getJWT?' + urllib.parse.urlencode(payload)
	#print(url)
	async with session.get(url) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_kamereonperson(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, personId):
	payload = {'country': 'FR'}
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/persons/' + personId + '?' + urllib.parse.urlencode(payload)
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_kamereontoken(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, accountId):
	payload = {'country': 'FR'}
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + accountId + '/kamereon/token?' + urllib.parse.urlencode(payload)
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_batterystatus(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	#headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey, 'x-kamereon-authorization' : 'Bearer ' + kamereonaccesstoken}
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	#url = kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v1/cars/' + vin + '/battery-status'
	#url = kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v2/cars/' + vin + '/battery-status?country=FR'
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v2/cars/' + vin + '/battery-status?country=FR'
	
	
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_car(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	#url = kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v1/cars/' + vin + '/battery-status'
	#url = kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v2/cars/' + vin + '/battery-status?country=FR'
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v2/cars/' + vin + '/?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_vehicles(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	#url = kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v1/cars/' + vin + '/battery-status'
	#url = kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v2/cars/' + vin + '/battery-status?country=FR'
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/vehicles?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_cockpit(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	#url = kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v2/cars/' + vin + '/cockpit'
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/cockpit?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def set_chargemode(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin, mode):
	if mode == 'always':
		data = {'data' : {
			'type': 'ChargeMode',
			'attributes': {
				'action': 'always_charging'
				#'action': 'schedule_mode'
			}
		}}
	else:
		data = {'data' : {
				'type': 'ChargeMode',
				'attributes': {
					#'action': 'always_charging'
					'action': 'schedule_mode'
				}
			}}
	headers = {'Content-type': 'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/actions/charge-mode?country=FR'
	#print(url)
	async with session.post(url, headers=headers,json=data) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		print(jsonresponse)
		return jsonresponse

async def set_chargingStart(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	data = {'data' : {
		'type': 'ChargingStart',
		'attributes': {
			'action': 'start'
			#'action': 'schedule_mode'
		}
	}}
	headers = {'Content-type': 'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/actions/charging-start?country=FR'
	#print(url)
	async with session.post(url, headers=headers,json=data) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def set_chargeSchedule(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin, file):
	in_file = open(file, 'r')
	data = json.load(in_file)
	in_file.close()
	headers = {'Content-type': 'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v2/cars/' + vin + '/actions/charge-schedule?country=FR'
	#print(url)
	async with session.post(url, headers=headers,json=data) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		print(jsonresponse)
		return jsonresponse

async def set_hvacStart(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	data = {'data' : {
		'type': 'HvacStart',
		'attributes': {
			'action': 'start',
			'targetTemperature': 20
		}
	}}
	headers = {'Content-type': 'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/actions/hvac-start?country=FR'
	#print(url)
	async with session.post(url, headers=headers,json=data) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def set_hvacStop(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	data = {'data' : {
		'type': 'HvacStart',
		'attributes': {
			'action': 'cancel'
		}
	}}
	headers = {'Content-type': 'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/actions/hvac-start?country=FR'
	#print(url)
	async with session.post(url, headers=headers,json=data) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse
		
async def get_chargemode(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/charge-mode?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse
		
async def get_location(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/location?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_chargeSchedule(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/charge-schedule?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse
		
async def get_chargingSettings(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/charging-settings?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def get_test(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, vin):
	headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
	url = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/res-state?country=FR'
	#print(url)
	async with session.get(url, headers=headers) as response:
		responsetext = await response.text()
		if responsetext == '':
			responsetext = '{}'
		jsonresponse = json.loads(responsetext)
		if 'message' in jsonresponse:
			self.tokenData = None
			raise MyRenaultServiceException(jsonresponse['message'])
		return jsonresponse

async def main():
	async with aiohttp.ClientSession(
			) as session:
		await mainwithsession(session)

async def mainwithsession(session):
	# Load credentials.
	#in_file = open('/home/pi/domoticz/scripts/python/credentials.json', 'r')
	in_file = open(sys.argv[1], 'r')
	credentials = json.load(in_file)
	in_file.close()
	

	gigyarooturl = "https://accounts.eu1.gigya.com"
	gigyaapikey = "3_4LKbCcMMcvjDm3X89LU4z4mNKYKdl_W0oD9w-Jvih21WqgJKtFZAnb9YdUgWT9_a"
	kamereonrooturl = "https://api-wired-prod-1-euw1.wrd-aws.com"
	kamereonapikey = 'YjkKtHmGfaceeuExUDKGxrLZGGvtVS0J'
	
	gigya_session = await get_gigyasession(session, gigyarooturl, gigyaapikey, credentials['RenaultServicesUsername'], credentials['RenaultServicesPassword'])
	with open('gigya_session.json', 'w') as outfile:
		json.dump(gigya_session, outfile)

	
	gigyacookievalue = gigya_session['sessionInfo']['cookieValue']

	gigya_account = await get_gigyaaccount(session, gigyarooturl, gigyaapikey, gigyacookievalue)
	with open('gigya_account.json', 'w') as outfile:
		json.dump(gigya_account, outfile)


	gigya_jwt = await get_gigyajwt(session, gigyarooturl, gigyaapikey, gigyacookievalue)
	with open('gigya_jwt.json', 'w') as outfile:
		json.dump(gigya_jwt, outfile)

	
	gigya_jwttoken= gigya_jwt['id_token']
	#gigya_jwttoken= ""
	
	kamereonpersonid = gigya_account['data']['personId']
	
	kamereon_person = await get_kamereonperson(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonpersonid)
	with open('kamereon_person.json', 'w') as outfile:
		json.dump(kamereon_person, outfile)


	if kamereon_person['accounts'][0]['accountType']== 'MYRENAULT':
		kamereonaccountid = kamereon_person['accounts'][0]['accountId']
	else:
		kamereonaccountid = kamereon_person['accounts'][1]['accountId']
	#print(kamereonaccountid)

	#kamereon_token = await get_kamereontoken(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid)
	#with open('kamereon_token.json', 'w') as outfile:
	#	json.dump(kamereon_token, outfile)
	#print('kamereon_token')
	
	#kamereonaccesstoken = kamereon_token['accessToken']
	
	if len(sys.argv)>2:
		if sys.argv[2] == "always":
			kamereon_chargemode = str( await set_chargemode(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN'],"always"))
		elif sys.argv[2] == "scheduled":
			kamereon_chargemode = str( await set_chargemode(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN'],"scheduled"))
		elif sys.argv[2] == "start":
			kamereon_chargemode = str( await set_chargingStart(session, kamereonrooturl, kamereonapikey, gigya_jwttoken,  kamereonaccountid, credentials['VIN']))
		elif sys.argv[2] == "ACstart":
			kamereon_chargemode = str( await set_hvacStart(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
		elif sys.argv[2] == "ACstop":
			kamereon_chargemode = str( await set_hvacStop(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
		elif sys.argv[2] == "chargeSchedule":
			kamereon_chargemode = str( await set_chargeSchedule(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN'],sys.argv[3]))
		else:
			kamereon_battery = str( await get_batterystatus(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
			#print(kamereon_battery)
			kamereon_cockpit = str( await get_cockpit(session, kamereonrooturl, kamereonapikey, gigya_jwttoken,  kamereonaccountid, credentials['VIN']))
			#print(kamereon_cockpit)
			kamereon_chargemode = str( await get_chargingSettings(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
			#print(kamereon_chargemode)
			kamereon_location = str( await get_location(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
			#print(kamereon_location)
			#kamereon_test = str( await get_test(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
			kamereon_test = "' '"
			
			jsonresponse = "{ 'battery' : " + kamereon_battery + "," + "'cockpit' : " + kamereon_cockpit + "," + "'chargemode' : " + kamereon_chargemode + "," + "'location' : " + kamereon_location + "," + "'test' : " + kamereon_test + "}" 
			print(jsonresponse)
			if len(sys.argv) > 2: 
				with open(sys.argv[2], 'w') as outfile:
					json.dump(jsonresponse, outfile)
	elif len(sys.argv)== 2:
		kamereon_battery = str( await get_batterystatus(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
		#print(kamereon_battery)
		kamereon_cockpit = str( await get_cockpit(session, kamereonrooturl, kamereonapikey, gigya_jwttoken,  kamereonaccountid, credentials['VIN']))
		#print(kamereon_cockpit)
		kamereon_chargemode = str( await get_chargingSettings(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
		#print(kamereon_chargemode)
		kamereon_location = str( await get_location(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
		#print(kamereon_location)
		#kamereon_test = str( await get_test(session, kamereonrooturl, kamereonapikey, gigya_jwttoken, kamereonaccountid, credentials['VIN']))
		kamereon_test = "' '"
		
		jsonresponse = "{ 'battery' : " + kamereon_battery + "," + "'cockpit' : " + kamereon_cockpit + "," + "'chargemode' : " + kamereon_chargemode + "," + "'location' : " + kamereon_location + "," + "'test' : " + kamereon_test + "}" 
		print(jsonresponse.replace("'",'"').replace("False","false").replace("True","true").replace("None",'"None"'))
	
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
