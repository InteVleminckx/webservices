# Webservices

Dit document bevat de design keuzes voor mijn API.

---

Als eerst zien we de structuur van de API, voor de opdracht zelf heb ik voor de gevraagde onderdelen al zoveel mogelijk proberen rekening te houden met RESTfulness.  
De structuur ziet eruit als volgt:  
```py
/					# 1
/movies					# 2
/movies/{movieid}			# 3
/movies/{movieid}/same-genres		# 4
/movies/{movieid}/similar-runtime	# 5
/movies/{movieid}/overlapping-actors	# 6
/movies/popular				# 7
/movies/compare				# 8
```

#### 1, 2

Deze 2 geven standaard 20 films terug van de website.  
Deze routes heb ik moeten toevoegen voor er voor te zorgen dat de route 'hackable' is.

--- 

#### 3

Deze route geeft de enkel de informatie voor een gevraagde film terug wanneer we een GET request uitvoeren.  
Deze route was vooral bedoeld voor wanneer we een film willen liken/unliken of deleten. Deze 2 acties worden dan uitgevoerd door een PUT en DELETE.

---

#### 4, 5, 6

Deze routes worden zo opgesteld dat we een actie kunnen uitvoeren op een film. We filteren dus eerst op een movie id in movies en dan vragen we bijvoorbeeld films op met dezelfde genres. Op deze manier leek het me het duidelijkste, om de route te begrijpen.

---

#### 7

Deze route geeft de populaire films terug. Dit kan gedaan worden door het argument 'amount' te gebruiken. Als dit argument niet is meegeven dan wordt er standaard de eerste 20 populaire films gegeven. We gebruiken hier een argument in plaats van een parameter omdat we hier meer een query operatie uitvoeren, we krijgen niet meer over minder te zien dan wat popular standaard toont qua informatie, maar een bepaalde scope van die informatie.  

---

#### 8

De compare route geeft alle informatie terug die gebruikt kan worden om die chart API op te roepen. Ik heb hiervoor gekozen om enkel de data terug te geven dat als argument moet worden gebruikt in plaats van de volledige url. Zodat wanneer de gebruiker toch een andere API hiervoor zou gebruiken, hij enkel de nodige data kan gebruiken uit mijn gegeven data. Anders zit het standaard verbonden aan de url en dat vond ik in het algemeen minder handig.  
Hier wordt verder ook een argument 'movies' meegeven waarbij meerdere films hun id kunnen worden meegeven gescheiden met een komma. Als er geen argument wordt meegeven zal er gewoon lege data terug worden gegeven.

---

---

## Running the project

Er is een run.sh file voorzien. Deze zal een environment aanmaken en alle nodige python package installeren. Nadien zal deze ook automatisch de website openen. 

