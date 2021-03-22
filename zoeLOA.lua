--date d'acquisition/début de la LOA-LLD
local jour = 4
local mois = 1
local annee = 2020

local kilometrageAnnuel = 12500		--forfait kilométrique annuel
local alertSensor = "Moyenne Zoé"	--capteur de type Alerte

local compteurKm = "Zoé"			--kilométrage

return {
	active = true, 
	logging = {
		--level = domoticz.LOG_DEBUG, -- Uncomment to override the dzVents global logging setting
		marker = 'Moyenne Zoé'..' '..'1.0'
	},
	on = {devices = 
		{compteurKm},  				-- mise à jour en temps réel
		timer = {'at 20:47'},		-- mise à jour journalière (quand la voiture ne roule pas)
	},

	execute = function(domoticz,compteur)
		compteur = domoticz.devices(compteurKm)
		domoticz.log("Kilometrage : "..compteur.counter,domoticz.LOG_INFO)
		kilometrage = compteur.counter
		
		reference = os.time{day=jour, year=annee, month=mois, hour=0, min=0, sec=0}
		daysfrom = (os.difftime(os.time(), reference)-(1*60*60)) / (24 * 60 * 60) -- seconds in a day
		wholedays = math.floor(daysfrom)
		distanceMoyenneSouhaitee = kilometrageAnnuel/365
		distanceMoyenneReelle = kilometrage/wholedays
		depassement = domoticz.utils.round(kilometrage-(wholedays*distanceMoyenneSouhaitee),0)
		prix = depassement/10
		domoticz.log("Ancienneté : "..wholedays,domoticz.LOG_INFO)
		domoticz.log("Distance moyenne journalière souhaitée : "..distanceMoyenneSouhaitee,domoticz.LOG_INFO)
		domoticz.log("Distance moyenne journalière réelle : "..distanceMoyenneReelle,domoticz.LOG_INFO)
		
		if (distanceMoyenneReelle > distanceMoyenneSouhaitee*1.01)then
			domoticz.log("Moyenne trop importante !",domoticz.LOG_INFO)
			domoticz.devices(alertSensor).updateAlertSensor(domoticz.ALERTLEVEL_ORANGE, 'Delta : '..depassement..' - '..prix..'€')
		else
			domoticz.devices(alertSensor).updateAlertSensor(domoticz.ALERTLEVEL_GREEN, 'Delta : '..depassement)			
		end
	end
}
