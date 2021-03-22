# MyRenaultZoeDomoticz
Connecteur entre Domoticz et la Renault Zoé ZE50

Fonctionnalités :

-Activation/désactivation des plannings de charges
-Etat de la charge
-Etat du branchement
-Lancement du pré-conditionnement
-Lancement de la charge
-Localisation
-Kilométrage
-Autonomie renvoyée par l'api (MAJ seulement au débranchement ou fin de charge)
-Autonomie calculée
-Conso moyenne après la charge
-Suivi dépassement kilométrage location.
-Démarrage "Intelligent" de la charge

Il y a plusieurs fichiers.
D'abord, le coeur de l'accès à l'api :
/home/pi/domoticz/scripts/python/MyRenault.py


Pour fonctionner, il a besoin d'un fichier contenant les identifiants :
/home/pi/domoticz/scripts/python/credentials.json
{
  "RenaultServiceLocation": "fr_FR",
  "RenaultServicesUsername": "adresse@gmail.com",
  "RenaultServicesPassword": "MotDePasseMyRenault",
  "VIN": "VF1NUMERODESERIE"
}

Maintenant, les script DzVents:

N'oubliez pas de créer les capteurs virtuels et renseigner le fichier 
/home/pi/domoticz/scripts/dzVents/scripts/zoe.lua

La version asynchrone est disponible pour Domoticz v2020.2 or later (dzVents version 3.1 or later)
/home/pi/domoticz/scripts/dzVents/scripts/zoe_async.lua

Le fichier avec un planning de charge à adapter selon vos besoins.
Vous pouvez adapter l'heure de début et la durée en minutes

/home/pi/domoticz/scripts/python/chargeSchedule.json

Le fichier avec le planning désactivé.
/home/pi/domoticz/python/chargeScheduleFalse.json

Le script suivant permet de connaître votre situation niveau LOA (trop ou pas assez de km)
/home/pi/domoticz/scripts/dzVents/scripts/zoeLOA.lua

La localisation. Les coordonnées locales sont récupérées directement dans les paramètres.
Il est possible d'adapter le script pour d'autres lieux.
/home/pi/domoticz/scripts/dzVents/scripts/zoeLocalisation.lua


Au final, j'ai mis des notifications pour l'état de la charge et de batterie ou autonomie faible.

Bugs connus :
- L'api Renault met du temps à s'activer après la livraison. Il m'a fallu 3 semaines pour avoir tous les services d'activés.
- Le lancement de charge ne fonctionne que si le planning de charge est désactivé.
- Parfois, l'api ne fonctionne pas. C'est de plus en plus rare, mais ça arrive.
- L'actualisation peut prendre du temps suivant la couverture réseau de la voiture.
