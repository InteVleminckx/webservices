# Webservices API

API documentation for the webservice assignment

## Movies : operations on movies

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

```json
>>> GET http://127.0.0.1:5000/movies/popular?amount=x 
{
    0: {
	"id": 10597,
	"title": "Kevin & Perry Go Large",
	"liked": false
    },
    ...
    x: {
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

```json
>>> GET http://127.0.0.1:5000/movies/10597/same-genres
{
    0: {
	"id": 76600,
	"title": "Avatar: The Way of Water",
	"liked": false
    },
    ...
    19: {
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

```json
>>> GET http://127.0.0.1:5000/movies/10597/same-genres
{
    0: {
	"id": 76600,
	"title": "Avatar: The Way of Water",
	"liked": false
    },
    ...
    19: {
	"id": 67006 
	"title": "Star Wars: Episode IV: A New Hope,",
	"liked": false
    }
}

```

#### <ins>404<ins>

An error message for indicating there went something wrong.

---

