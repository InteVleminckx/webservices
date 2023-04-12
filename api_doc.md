# Webservices API

API documentation for the webservice assignment

## Movies : operations on movies

---

### Movies

#### <ins>Request - GET<ins>

**GET** /movies/{movieid}
> ***movieid***: integer  
The id of the movie.

#### <ins>Response - GET<ins>

##### <ins>200<ins>

Returns information about the movie by its id.  
The movie information is represented with following key:
- ***id***: integer - The ID of the movie.
- ***title***: string - The original title of the movie.
- ***liked***: boolean - Whether the movie is liked by the user or not.

###### Example
```py
>>> GET http://127.0.0.1:5000/movies/10597 
```
```json
    {
	"id": 10597,
	"title": "Kevin & Perry Go Large",
	"liked": false
    } 
```

##### <ins>404<ins>

An error message for indicating there went something wrong.

#### <ins>Request - PUT<ins>

**PUT** /movies/{movieid}
> ***movieid***: integer  
The id of the movie.

#### <ins>Response - PUT<ins>

##### <ins>200<ins>

Like's or unlike's a movie based on the current like status of the movie.  
Returns a little message when its succeed.

###### Example
```py
>>> PUT http://127.0.0.1:5000/movies/10597
```
```py 
"The movie with movie id 10597, is successfully liked/unliked."
```

##### <ins>404<ins>

An error message for indicating there went something wrong.

#### <ins>Request - DELETE<ins>

**DELETE** /movies/{movieid}
> ***movieid***: integer  
The id of the movie.

#### <ins>Response - DELETE<ins>

##### <ins>200<ins>

Deletes a mvoie by its id.
Returns a little message when its succeed.

###### Example
```py
>>> DELETE http://127.0.0.1:5000/movies/10597
```
```py 
"The movie with movie id 10597, is successfully deleted."
```

##### <ins>404<ins>

An error message for indicating there went something wrong.

---

### Popular

#### <ins>Request<ins>

**GET** /movies/popular
> ***amount***: integer  
The number of popular movies to retrieve.  
Example value: 10  
Default value: 20

#### <ins>Response<ins>

##### <ins>200<ins>

Returns a dictionary containing the popular movies.  
Each movie's information is represented with following key:
- ***id***: integer - The ID of the movie.
- ***title***: string - The original title of the movie.
- ***liked***: boolean - Whether the movie is liked by the user or not.

###### Example
```py
>>> GET http://127.0.0.1:5000/movies/popular?amount=x 
```
```json
{
    "0":{
	"id": 10597,
	"title": "Kevin & Perry Go Large",
	"liked": false
    },

    "...": {},

    "x":{
	"id": 76600,
	"title": "Avatar: The Way of Water",
	"liked": false
    }
}
```

##### <ins>404<ins>

An error message for indicating there went something wrong.

---

### Same genres

#### <ins>Request<ins>

**GET** /movies/{movieid}/same-genres
> ***movieid***: integer  
The id of the movie.

#### <ins>Response<ins>

##### <ins>200<ins>

Returns a dictionary containing movies with the same genre as the provided movie.  
Each movie's information is represented with following key:
- ***id***: integer - The ID of the movie.
- ***title***: string - The original title of the movie.
- ***liked***: boolean - Whether the movie is liked by the user or not.

###### Example

```py
>>> GET http://127.0.0.1:5000/movies/10597/same-genres
```
```json
{
    "0":{
	"id": 76600,
	"title": "Avatar: The Way of Water",
	"liked": false
    },

    "...": {},

    "19":{
	"id": 12345,
	"title": "Avatar",
	"liked": false
    }
}

```

#### <ins>404<ins>

An error message for indicating there went something wrong.

---

### Similar runtime

#### <ins>Request<ins>

**GET** /movies/{movieid}/similar-runtime  
> ***movieid***: integer  
The id of the movie.

#### <ins>Response<ins>

##### <ins>200<ins>

Returns a dictionary containing movies with the similar runtime as the provided movie.  
Each movie's information is represented with following key:
- ***id***: integer - The ID of the movie.
- ***title***: string - The original title of the movie.
- ***liked***: boolean - Whether the movie is liked by the user or not.

###### Example

```py
>>> GET http://127.0.0.1:5000/movies/76600/similar-runtime
```
```json
{
    "0":{
	"id": 76600,
	"title": "Avatar: The Way of Water",
	"liked": false
    },

    "...": {},

    "19":{
	"id": 67006,
	"title": "Star Wars: Episode IV: A New Hope,",
	"liked": false
    }
}

```

#### <ins>404<ins>

An error message for indicating there went something wrong.

---

### Two overlapping actors

#### <ins>Request<ins>

**GET** /movies/{movieid}/overlapping-actors  
> ***movieid***: integer  
The id of the movie.

#### <ins>Response<ins>

##### <ins>200<ins>

Returns a dictionary containing movies with two overlapping actors as the provided movie.  
Each movie's information is represented with following key:
- ***id***: integer - The ID of the movie.
- ***title***: string - The original title of the movie.
- ***liked***: boolean - Whether the movie is liked by the user or not.

###### Example

```py
>>> GET http://127.0.0.1:5000/movies/67006/overlapping-actors
```
```json
{
    "0":{
	"id": 67006,
	"title": "Star Wars: Episode IV: A New Hope",
	"liked": false
    },

    "...": {},

    "19":{
	"id": 67005,
	"title": "Star Wars: Episode III: Revenge of the Sith",
	"liked": tue
    }
}

```

#### <ins>404<ins>

An error message for indicating there went something wrong.

--- 

### Comparing movies

**GET** /movies/compare
> ***movies***: comma-separated string contains ID as integers  
Is a comma-separated string containging the IDs of the movies to retrieve chart data for. 

#### <ins>Response<ins>

##### <ins>200<ins>

Returns a dictionary that contains data for plotting a chart for the requested movies. 
The dictionary contains the following keys:
- ***type***: string -  The type of chart being returned. Currently 'bar'.
- ***data***: dictionary - Containing the data for the chart.
	- ***labels***: list - The movie names for the requested movies.
	- ***datasets***: list - Containing a single dictionary representing the dataset.
		- ***label***: string - The label for the dataset. Currently set to 'Voting average'.
		- ***data***: list - The average voting scores for the requested movies.



For plotting the chart in your browser you can past the retrieved dictionary behind the argument 'c' as follows:
```
https://quickchart.io/chart?c=<dictionary>
```

###### Example

```py
>>> GET http://127.0.0.1:5000/movies/compare?movies=67060,456123,74185
```
```json
{
	"type": "bar", 
	"data": {
			"labels": ["Scream I", "Scream II", "Srceam III"],
			"datasets": [{
					"label": "Voting average",
					"data": [7.5, 8.2, 6.7]
				}]
		}
}
```

#### <ins>404<ins>

An error message for indicating there went something wrong.


---



