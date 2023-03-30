let SHOW_POPULAR = false;

const INPUT_POPULAR = document.getElementById("input-popular");
const BARCHART = document.getElementById("barchart");

const POPULAR_MOVIES = document.getElementById("popular-movies");

const RETURN_BUTTON = document.getElementById("return-button");
const INTERACT_BUTTONS = document.getElementById("interact-buttons");

const SIMILAR_TABLES = document.getElementById("similar");

const SAME_GENRES = document.getElementById("same-genres");
const SIMILAR_RUNTIME = document.getElementById("similar-runtime");
const OVERLAPPING_ACTORS = document.getElementById("overlapping-actors");

let MOVIES = {};

let CHART_MOVIES = [];

change_view();

function change_view() {
    SHOW_POPULAR = !SHOW_POPULAR;
    if (SHOW_POPULAR) {
        document.getElementById('title').innerHTML = "Webservices";
        INPUT_POPULAR.style.display = "block";
        BARCHART.style.display = "block";
        POPULAR_MOVIES.style.display = "block";
        RETURN_BUTTON.style.display = "none";
        INTERACT_BUTTONS.style.display = "none";
        SIMILAR_TABLES.style.display = "none";
    } else {
        INPUT_POPULAR.style.display = "none";
        BARCHART.style.display = "none";
        POPULAR_MOVIES.style.display = "none";
        RETURN_BUTTON.style.display = "block";
        INTERACT_BUTTONS.style.display = "block";
        SIMILAR_TABLES.style.display = "flex";
    }
}


function get_x_popular_movies(x) {

    return fetch('/movies/popular?amount=' + x.toString(), {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error:', error));
}

function get_movies_with_same_genre(movie_id) {
    return fetch('/movies/' + movie_id + '/same-genres', {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error:', error));
}

function get_movies_with_similar_runtime(movie_id) {
    return fetch('/movies/' + movie_id + '/similar-runtime', {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error:', error));
}

function get_movies_with_overlapping_actors(movie_id) {
    return fetch('/movies/' + movie_id + '/overlapping-actors', {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error:', error));
}


function get_bar_plot_information(movies) {
    return fetch('/movies/compare?movies=' + movies, {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error:', error));
}

function delete_movie(movie_id) {
    return fetch('/movies/' + movie_id, {
        method: 'DELETE',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // Re-render popular table
            render_popular_table();

            // Change view
            change_view();

            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error:', error));
}

function like_unlike_movie(movie_id) {
    return fetch('/movies/' + movie_id, {
        method: 'PUT',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            MOVIES[movie_id]['liked'] = !MOVIES[movie_id]['liked'];
            refresh_interactive_buttons(movie_id);

            return response.json();
        })
        .catch(error => console.error('Error:', error));
}

function render_popular_table() {
    const amountInput = document.getElementById('amountInput');
    const amount = amountInput.value;

    CHART_MOVIES = [];

    get_x_popular_movies(amount).then(data => {
        const movies = data['movies'];

        // Create table based on popular movies
        let table = "<table> <thead> <tr> <th></th> <th>Movie</th> </tr> </thead> <tbody>";

        for (const key of Object.keys(movies)) {
            const movie = movies[key];
            const title = movie['title'];
            const id = movie['id'];

            if (CHART_MOVIES.length < 10) {
                CHART_MOVIES.push(id);
            }

            MOVIES[id] = {'liked': (movie['liked'] === 'true' || movie['liked'] === true)}

            table += "<tr> <td>" + (parseInt(key) + 1).toString() + "</td> <td> <p onclick='render_movie_information(" + "\"" + id + "\"" + ", " + "\"" + title + "\"" + "); change_view()' style='cursor: pointer'>" + title + "</p> </td> </tr>";

        }

        table += "</tbody> </table>";
        document.getElementById('popular-movies').innerHTML = table;
    });
}

function render_movie_information(movie_id, title) {

    // Verander title naar film naam
    document.getElementById('title').innerHTML = title;
    SAME_GENRES.innerHTML = "";
    OVERLAPPING_ACTORS.innerHTML = "";
    SIMILAR_RUNTIME.innerHTML = "";


    render_same_genres_table(movie_id);
    render_similar_runtime_table(movie_id);
    render_overlapping_actors_table(movie_id);

    refresh_interactive_buttons(movie_id);

}

function refresh_interactive_buttons(movie_id) {

    const rate = MOVIES[movie_id]['liked'] ? "UN-LIKE" : "LIKE";

    INTERACT_BUTTONS.innerHTML =
        "<button id=\"rate\" onclick='like_unlike_movie(" + "\"" + movie_id + "\"" + ")'>" + rate + "</button>" +
        "<button id=\"delete\" onclick='delete_movie(" + "\"" + movie_id + "\"" + ")'>Delete movie</button>";


}

function render_same_genres_table(movie_id) {
    SAME_GENRES.innerHTML = "";

    get_movies_with_same_genre(movie_id).then(data => {
        const movies = data['movies'];

        // Create table based on popular movies
        let table = "<h2>Same genres</h2><table> <thead> <tr> <th></th> <th>Movie</th> </tr> </thead> <tbody>";

        for (const key of Object.keys(movies)) {
            const movie = movies[key];
            const title = movie['title'];
            const id = movie['id'];

            MOVIES[id] = {'liked': (movie['liked'] === 'true' || movie['liked'] === true)}

            table += "<tr> <td>" + (parseInt(key) + 1).toString() + "</td> <td> <p onclick='render_movie_information(" + "\"" + id + "\"" + ", " + "\"" + title + "\"" + ");' style='cursor: pointer'>" + title + "</p> </td> </tr>";
        }

        table += "</tbody> </table>";
        SAME_GENRES.innerHTML = table;
    });
}

function render_similar_runtime_table(movie) {
    SIMILAR_RUNTIME.innerHTML = "";

    get_movies_with_similar_runtime(movie).then(data => {
        const movies = data['movies'];

        // Create table based on popular movies
        let table = "<h2>Similar runtime</h2><table> <thead> <tr> <th></th> <th>Movie</th> </tr> </thead> <tbody>";

        for (const key of Object.keys(movies)) {
            const movie = movies[key];
            const title = movie['title'];
            const id = movie['id'];

            MOVIES[id] = {'liked': (movie['liked'] === 'true' || movie['liked'] === true)}

            table += "<tr> <td>" + (parseInt(key) + 1).toString() + "</td> <td> <p onclick='render_movie_information(" + "\"" + id + "\"" + ", " + "\"" + title + "\"" + ");' style='cursor: pointer'>" + title + "</p> </td> </tr>";
        }

        table += "</tbody> </table>";
        SIMILAR_RUNTIME.innerHTML = table;
    });
}

function render_overlapping_actors_table(movie) {
    OVERLAPPING_ACTORS.innerHTML = "";

    get_movies_with_overlapping_actors(movie).then(data => {
        const movies = data['movies'];

        // Create table based on popular movies
        let table = "<h2>Overlapping actors</h2><table> <thead> <tr> <th></th> <th>Movie</th> </tr> </thead> <tbody>";

        for (const key of Object.keys(movies)) {
            const movie = movies[key];
            const title = movie['title'];
            const id = movie['id'];

            MOVIES[id] = {'liked': (movie['liked'] === 'true' || movie['liked'] === true)}

            table += "<tr> <td>" + (parseInt(key) + 1).toString() + "</td> <td> <p onclick='render_movie_information(" + "\"" + id + "\"" + ", " + "\"" + title + "\"" + ");' style='cursor: pointer'>" + title + "</p> </td> </tr>";
        }

        table += "</tbody> </table>";
        OVERLAPPING_ACTORS.innerHTML = table;
    });
}

function render_barchart() {

    let ids = "";

    for (let id in CHART_MOVIES) {
        ids += CHART_MOVIES[id];

        if (CHART_MOVIES[id] !== CHART_MOVIES[CHART_MOVIES.length - 1]) {
            ids += ",";
        }
    }

    if (ids !== "") {
        get_bar_plot_information(ids).then(data => {
            const baseQuickChartUrl = 'https://quickchart.io/chart?c=';
            const chartData = encodeURIComponent(JSON.stringify(data));
            const quickChartUrl = baseQuickChartUrl + chartData;
            window.open(quickChartUrl, '_blank');
        });
    }

}