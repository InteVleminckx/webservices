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

--- 



