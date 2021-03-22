
local scriptName = 'ZoéLocalisation'
local scriptVersion = '1.2'

local fichierTemp = "/var/tmp/zoe.txt"
local presence = "Zoé Domicile"								-- Interrupteur

return {
	active = true,
	logging = {
		level = domoticz.LOG_DEBUG, -- Uncomment to override the dzVents global logging setting
		marker = scriptName..' '..scriptVersion
	},	
	on = {
		shellCommandResponses = { 'zoe_async' }		
	},


	execute = function(domoticz, item) 
		local latitudeCible = domoticz.settings.location.latitude
		local longitudeCible = domoticz.settings.location.longitude
		
		-- Fonction de calcul de distance
		-- Renvoi la distance en kilometre a une decimale entre deux coordonées GPS
		local function distancekm(latitude1, longitude1, latitude2, longitude2)
			rayonTerre = 6378137;   -- Rayon équatorial de la terre en metre
			radlatx = math.rad(latitude1);
			radlonx = math.rad(longitude1);
			radlaty = math.rad(latitude2);
			radlony = math.rad(longitude2);
			calculLatitude = (radlaty - radlatx) / 2;
			calculLongitude = (radlony - radlonx) / 2;
			detail = (math.sin(calculLatitude))^2 + math.cos(radlatx) * math.cos(radlaty) * (math.sin(calculLongitude))^2;
			calcul = 2 * math.atan(math.sqrt(detail), math.sqrt(1 - detail));
			output = math.floor((rayonTerre * calcul)/10)/100
			return output
		end		
		if item.statusCode == 0  then --retour ok
			zoe = item.json
			if(zoe)then
				if (zoe.location.data) then
					latitude = zoe.location.data.attributes.gpsLatitude
					domoticz.log("Latitude "..latitude, domoticz.LOG_DEBUG)
					longitude = zoe.location.data.attributes.gpsLongitude
					domoticz.log("Longitude "..longitude, domoticz.LOG_DEBUG)
					
					distance = distancekm(latitude,longitude,latitudeCible,longitudeCible)
					domoticz.log("distance "..distance, domoticz.LOG_DEBUG)
					if(distance<1)then
						domoticz.devices(presence).switchOn().checkFirst()
					else
						domoticz.devices(presence).switchOff().checkFirst()
					end
				end
			else
				domoticz.log("API injoignable",domoticz.LOG_ERROR)
			end
		end		
	end
}
