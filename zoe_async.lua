--Prérequis : 
--Domoticz v2020.2 or later (dzVents version 3.1 or later)

-- sources :	https://github.com/jamesremuscat/pyze
--				https://github.com/epenet/Renault-Zoe-API
local Time = require('Time')

local scriptName = 'Zoé_async'
local scriptVersion = '2.0'
--	1.0	version initiale
--	1.1 ajout custom events 
--	1.2 Authentification v2

--                                      					Dummy à créer :
local batterieZoe = "Batterie Zoé" 							-- Pourcentage
local charge = "Charge Zoé"									-- Interrupteur Custom avec les niveaux :
																-- 0	Non Branchée
																-- 10	Attente Charge Planifiée
																-- 20	Charge Terminée
																-- 30	Attente Charge Actuelle
																-- 40	Trappe Ouverte
																-- 50	En Charge
																-- 60	Erreur De Charge
																-- 70	Indisponible
local LancementCharge = "Lancer la Charge"					-- Interrupteur Push On
local lanceAC = "Zoé Pré Chambrage"							-- Interrupteur Push On
local plugStatus = "Zoé Branchée"							-- Interrupteur
local chargeMode = "Charge Programmée"						-- Interrupteur
local chargeDisable = "Charge Désactivée"					-- Interrupteur
local kilometrage = "Zoé"									-- Compteur 
local autonomie = "Autonomie Zoé"							-- Custom
local autonomieReelleEstimee = "Autonomie Zoé Réelle"		-- Custom
local consommationMoyenne = "Conso Zoé"						-- Custom
local puissanceInstantanee = "Puissance Instantanée"	-- Custom
local capaciteBatterie = 50									-- en kWh
--local tempBatt = "Temp Batterie Zoé"						-- Température

local fichierTemp = "/var/tmp/zoe.txt"						-- fichier de retour des requêtes
local credentials = "/home/pi/domoticz/scripts/python/credentials.json" -- Identifiants
local scriptPython = "/home/pi/domoticz/scripts/python/MyRenault.py"
local planningActive = "/home/pi/domoticz/scripts/python/chargeSchedule.json"
local planningDesactive = "/home/pi/domoticz/scripts/python/chargeScheduleFalse.json"
local planningChargeDesactive = "/home/pi/domoticz/scripts/python/chargeDisable.json"

return {
	active = true,
	logging = {
		level = domoticz.LOG_DEBUG, -- Uncomment to override the dzVents global logging setting
		marker = scriptName..' '..scriptVersion
	},	
	on = {
		timer = {'every 4 minutes'},
		devices = {
            LancementCharge,
			chargeMode,
			chargeDisable,
			lanceAC            
		},

		shellCommandResponses = { 'zoe_async' }
	},
	data = {
        notifZoe = {initial=false},
        notifZoeKm = {initial=false},
		kmFinDeCharge = {initial=345},
		batterieFinDeCharge = {initial=100},
		batterieTimestamp = {initial="2020-11-26 22:38:30"},
		
    },

	execute = function(domoticz, item) 
		
		if (item.isShellCommandResponse ) then
		--résultat de l'appel de l'api
			if item.statusCode == 0  then --retour ok
				domoticz.log(item.data, domoticz.LOG_DEBUG)
				zoe = item.json
				if(zoe)then
					if (zoe.battery.data) then
						domoticz.log("Autonomie fin de charge : "..zoe.battery.data.attributes.batteryAutonomy,domoticz.LOG_DEBUG)
						domoticz.log("Batterie fin de charge : "..domoticz.data.batterieFinDeCharge,domoticz.LOG_DEBUG)
						
						if (zoe.battery.data.attributes.chargingInstantaneousPower)then
							--Puissance instantanée de charge retournée par l'api
							domoticz.devices(puissanceInstantanee).updateCustomSensor(zoe.battery.data.attributes.chargingInstantaneousPower)
						end						
						
						if (tonumber(zoe.battery.data.attributes.batteryAutonomy) ~= tonumber(domoticz.devices(autonomie).rawData[1])
						or tonumber(zoe.battery.data.attributes.batteryAutonomy) ~= domoticz.data.kmFinDeCharge )then
							--calcul de l'autonomie restante et de la consommation
							domoticz.devices(autonomie).updateCustomSensor(zoe.battery.data.attributes.batteryAutonomy)
							domoticz.devices(autonomieReelleEstimee).updateCustomSensor(zoe.battery.data.attributes.batteryAutonomy)
							domoticz.data.kmFinDeCharge = zoe.battery.data.attributes.batteryAutonomy
							domoticz.data.batterieFinDeCharge = zoe.battery.data.attributes.batteryLevel
							domoticz.log("Batterie Fin de Charge : "..domoticz.data.batterieFinDeCharge,domoticz.LOG_DEBUG)
							domoticz.log("Autonomie Fin de Charge : "..domoticz.data.kmFinDeCharge,domoticz.LOG_DEBUG)
							consommation = math.floor(100*capaciteBatterie*domoticz.data.batterieFinDeCharge/domoticz.data.kmFinDeCharge)/100
							domoticz.log( "Consommation : "..consommation, domoticz.LOG_DEBUG)
							domoticz.devices(consommationMoyenne).updateCustomSensor(consommation)
						end
						
						if zoe.battery.data.attributes.batteryLevel > domoticz.devices(batterieZoe).percentage
						and domoticz.devices(charge).state == "En Charge" then
						-- calcul de la puissance de charge 
							local now = Time(domoticz.time.rawDateTime) -- current time
							local compar= now.compare(Time(domoticz.data.batterieTimestamp))

							domoticz.log("Time rawDateTime "..domoticz.time.rawDateTime,domoticz.LOG_DEBUG)
							domoticz.log("Time batterieTimestamp "..domoticz.data.batterieTimestamp,domoticz.LOG_DEBUG)
							domoticz.log("Time compare "..compar.minutes,domoticz.LOG_DEBUG)
							domoticz.data.batterieTimestamp = domoticz.time.rawDateTime
							local deltaPourcentage = zoe.battery.data.attributes.batteryLevel - domoticz.devices(batterieZoe).percentage
							local KWh = capaciteBatterie*deltaPourcentage/100
							local puissanceCharge = KWh / compar.minutes * 60 * 1000
							domoticz.log("Puissance charge "..puissanceCharge.."W",domoticz.LOG_DEBUG)
							domoticz.devices("Puissance Charge").updateEnergy(puissanceCharge)
						end
						
						if (zoe.battery.data.attributes.batteryLevel ~= domoticz.devices(batterieZoe).percentage
						or domoticz.devices(batterieZoe).lastUpdate.minutesAgo >9)then
						--mise à jour du niveau de batterie (forcée toutes les 10 minutes)
							domoticz.log("Batterie : "..zoe.battery.data.attributes.batteryLevel,domoticz.LOG_DEBUG)
							domoticz.devices(batterieZoe).updatePercentage(zoe.battery.data.attributes.batteryLevel)
							if (zoe.battery.data.attributes.batteryLevel <= 40 
							and domoticz.data.notifZoe == false 
							and domoticz.devices(plugStatus).active == false )then
							--envoi d'un message d'alerte batterie < 40%
								domoticz.data.notifZoe = true
								domoticz.log( "Batterie Zoé inférieure à 40 %.", domoticz.LOG_DEBUG)
								domoticz.notify("Domobox","Il faudra recharger Zoé. Batterie Zoé inférieure à 40 %.",domoticz.PRIORITY_NORMAL)
							end
							kmAutonomieReelleEstimee = math.floor(domoticz.data.kmFinDeCharge / domoticz.data.batterieFinDeCharge * zoe.battery.data.attributes.batteryLevel)
							domoticz.log( "Autonomie estimée : "..kmAutonomieReelleEstimee, domoticz.LOG_DEBUG)
							domoticz.devices(autonomieReelleEstimee).updateCustomSensor(kmAutonomieReelleEstimee)
							
							if (kmAutonomieReelleEstimee <= 40 and domoticz.data.notifZoeKm == false and domoticz.devices(plugStatus).active == false)then
								domoticz.data.notifZoeKm = true
								domoticz.log( "Autonomie Zoé inférieure à 40 Km.", domoticz.LOG_DEBUG)
								domoticz.notify("Domobox","Il faudra recharger Zoé. Autonomie Zoé inférieure à 40 Km.",domoticz.PRIORITY_NORMAL)
							end
							
							
						end
						
										
						-- Température non remontée par l'API pour l'instant pour la ZE50
						-- domoticz.log("Temp Batterie : "..zoe.battery.data.attributes.batteryTemperature,domoticz.LOG_DEBUG)
						-- if (tonumber(zoe.battery.data.attributes.batteryTemperature) ~= tonumber(domoticz.devices(tempBatt).temperature))then
							-- domoticz.devices(tempBatt).updateTemperature(zoe.battery.data.attributes.batteryTemperature)
						-- end
						
						domoticz.log("Charge : "..zoe.battery.data.attributes.chargingStatus,domoticz.LOG_DEBUG)
						if (tonumber(zoe.battery.data.attributes.chargingStatus) == 0 and domoticz.devices(charge).state ~= "Non Branchée")then
							domoticz.devices(charge).switchSelector("Non Branchée")
							domoticz.devices("Puissance Charge").updateEnergy(0)
						elseif (tonumber(zoe.battery.data.attributes.chargingStatus) == 0.1 and domoticz.devices(charge).state ~= "Attente Charge Planifiée")then
							domoticz.devices(charge).switchSelector("Attente Charge Planifiée")
							domoticz.devices("Puissance Charge").updateEnergy(0)
						elseif (tonumber(zoe.battery.data.attributes.chargingStatus) == 0.2 and domoticz.devices(charge).state ~= "Charge Terminée")then
							domoticz.devices(charge).switchSelector("Charge Terminée")
							domoticz.devices("Puissance Charge").updateEnergy(0)
						elseif (tonumber(zoe.battery.data.attributes.chargingStatus) == 0.3 and domoticz.devices(charge).state ~= "Attente Charge Actuelle")then
							domoticz.devices(charge).switchSelector("Attente Charge Actuelle")
							domoticz.devices("Puissance Charge").updateEnergy(0)
						elseif (tonumber(zoe.battery.data.attributes.chargingStatus) == 0.4 and domoticz.devices(charge).state ~= "Trappe Ouverte")then
							domoticz.devices(charge).switchSelector("Trappe Ouverte")
						elseif (tonumber(zoe.battery.data.attributes.chargingStatus) == 1 and domoticz.devices(charge).state ~= "En Charge")then
							domoticz.devices(charge).switchSelector("En Charge")
							domoticz.data.notifZoe = false
							domoticz.data.notifZoeKm = false
							domoticz.data.batterieTimestamp = domoticz.time.rawDateTime
						elseif (tonumber(zoe.battery.data.attributes.chargingStatus) == -1 and domoticz.devices(charge).state ~= "Erreur De Charge")then
							domoticz.devices(charge).switchSelector("Erreur De Charge")
							domoticz.devices("Puissance Charge").updateEnergy(0)
						elseif (tonumber(zoe.battery.data.attributes.chargingStatus) == -1.1 and domoticz.devices(charge).state ~= "Indisponible")then
							domoticz.devices(charge).switchSelector("Indisponible")
						end
						
						domoticz.log("Plug Status : "..zoe.battery.data.attributes.plugStatus,domoticz.LOG_DEBUG)
						if (tonumber(zoe.battery.data.attributes.plugStatus) == 0 )then
							domoticz.devices(plugStatus).switchOff().checkFirst()
						else
							domoticz.devices(plugStatus).switchOn().checkFirst()
						end
						
						
					end
					if (zoe.cockpit.data and zoe.chargemode.data and zoe.chargemode.data.attributes.schedules)then
						domoticz.log("km : "..zoe.cockpit.data.attributes.totalMileage,domoticz.LOG_DEBUG)
						if (domoticz.utils.round(tonumber(zoe.cockpit.data.attributes.totalMileage),1) ~= tonumber(domoticz.devices(kilometrage).counter))then
							domoticz.log(domoticz.utils.round(tonumber(zoe.cockpit.data.attributes.totalMileage),1),LOG_DEBUG)
							domoticz.log(tonumber(domoticz.devices(kilometrage).counter),LOG_DEBUG)
							
							domoticz.devices(kilometrage).updateCounter(zoe.cockpit.data.attributes.totalMileage)
						end
						
						if (zoe.chargemode.data.attributes.schedules[1].activated and domoticz.devices(chargeMode).bState == false )then
							domoticz.log("mode planning : "..tostring(zoe.chargemode.data.attributes.schedules[1].activated),domoticz.LOG_DEBUG)
							domoticz.devices(chargeMode).switchOn().silent()
						elseif (zoe.chargemode.data.attributes.schedules[1].activated == false and domoticz.devices(chargeMode).bState == true )then
							domoticz.devices(chargeMode).switchOff().silent()
						end
					end
								
				else
					domoticz.log("API injoignable",domoticz.LOG_ERROR)
				end
			end
		
		-----------------Actions boutons---------------------------
		elseif(item.name == LancementCharge and item.bState == true)then
			domoticz.log("Lancement de la charge",domoticz.LOG_DEBUG)
			os.execute("python3 '"..scriptPython.."' '"..credentials.."' 'start' &")
		elseif(item.name == lanceAC and item.bState == true)then
			domoticz.log("Lancement de la clim",domoticz.LOG_DEBUG)
			os.execute("python3 '"..scriptPython.."' '"..credentials.."' 'ACstart' &")
		elseif(item.name == lanceAC and item.bState == false)then
			domoticz.log("Arrêt de la clim",domoticz.LOG_DEBUG)
			os.execute("python3 '"..scriptPython.."' '"..credentials.."' 'ACstop' &")
		elseif(item.name == chargeMode and item.bState == true)then
			domoticz.log("Planning de charge activé",domoticz.LOG_DEBUG)
			os.execute(scriptPython..' '..credentials..' "chargeSchedule" "'..planningActive..'" &')
		elseif(item.name == chargeMode and item.bState == false)then
			domoticz.log("Planning de charge désactivé",domoticz.LOG_DEBUG)
			os.execute(scriptPython..' '..credentials..' "chargeSchedule" "'..planningDesactive..'" &')
		elseif(item.name == chargeDisable and item.bState == true)then
			domoticz.log("Charge désactivée",domoticz.LOG_DEBUG)
			os.execute(scriptPython..' '..credentials..' "chargeSchedule" "'..planningChargeDesactive..'" &')
		elseif(item.name == chargeDisable and item.bState == false)then
			domoticz.log("Planning de charge activé",domoticz.LOG_DEBUG)
			os.execute(scriptPython..' '..credentials..' "chargeSchedule" "'..planningActive..'" &')
		
		elseif(item.isTimer) then
			if domoticz.data.batterieTimestamp == nil then
				domoticz.data.batterieTimestamp = domoticz.time.rawDateTime
			end
			-- Execution de la requête
			domoticz.executeShellCommand({
                command = "python3 '"..scriptPython.."' '"..credentials.."'",
                callback = 'zoe_async',
                timeout = 30,
            })

		end
		
		
	end
}
