from flask import Flask
from flask import render_template, request
import sqlite3
import random

app = Flask(__name__)
databaseName = "todo"

def create_database():
    conn = sqlite3.connect(databaseName+'.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master")
    tableNames = c.fetchall()
    for table in tableNames:
        c.execute("DROP TABLE IF EXISTS "+table[0])
        print("dropped " + table[0])

    createMovieTable(c)
    createUserTable(c)
    createReviewTable(c)

    conn.commit()

    seed_database(conn)
    conn.close()


def createMovieTable(c):
    c.execute("CREATE TABLE IF NOT EXISTS movies(movieId INTEGER NOT NULL,movieName CHAR(100), movieReleaseDate CHAR(100), movieImageLarge CHAR(100), movieDescription CHAR(100), PRIMARY KEY (movieId))")
    print("Created Movie Table")

def createUserTable(c):
    c.execute("CREATE TABLE IF NOT EXISTS users(userId INTEGER NOT NULL, userName CHAR(100), userPassword CHAR(100), userEmail CHAR(100), PRIMARY KEY (userId))")
    print("Created User Table")

def createReviewTable(c):
    c.execute("CREATE TABLE IF NOT EXISTS reviews(postId INTEGER NOT NULL, userId int, movieId int, reviewTime CHAR(100), reviewText CHAR(100), reviewRating int(10), PRIMARY KEY (postId), FOREIGN KEY (movieId) REFERENCES movies(movieId), FOREIGN KEY (userId) REFERENCES users(userId))")
    print("Created Review Table")

def seed_database(conn, userNumberSeed = 100, reviewSeederNumber = 100):
    c = conn.cursor()
    movieSeeder = [
    ["Inception", "2010-07-16", "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg", "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."],
    ["The Shawshank Redemption", "1994-09-22", "https://m.media-amazon.com/images/I/815qtzaP9iL._AC_UF894,1000_QL80_.jpg", "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."],
    ["The Dark Knight", "2008-07-18", "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg", "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham."],
    ["The Godfather", "1972-03-24", "https://play-lh.googleusercontent.com/ZucjGxDqQ-cHIN-8YA1HgZx7dFhXkfnz73SrdRPmOOHEax08sngqZMR_jMKq0sZuv5P7-T2Z2aHJ1uGQiys", "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."],
    ["Pulp Fiction", "1994-10-14", "https://m.media-amazon.com/images/S/pv-target-images/dbb9aff6fc5fcd726e2c19c07f165d40aa7716d1dee8974aae8a0dad9128d392.jpg", "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."],
    ["The Matrix", "1999-03-31", "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg", "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."],
    ["Forrest Gump", "1994-07-06", "https://m.media-amazon.com/images/I/61eAL7QPTRL._AC_UF894,1000_QL80_.jpg", "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75."],
    ["Fight Club", "1999-10-15", "https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg", "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more."],
    ["Interstellar", "2014-11-07", "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg", "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."],
    ["The Lord of the Rings: The Fellowship of the Ring", "2001-12-19", "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_.jpg", "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."]
]

    c.executemany("INSERT INTO movies(movieName,movieReleaseDate,movieImageLarge,movieDescription) VALUES ( ?, ?, ?, ?)", (movieSeeder))
    conn.commit()

    for i in range(userNumberSeed):
        name = randomString(10)
        c.execute("INSERT INTO users(userName, userPassword, userEmail) VALUES (?, ?, ?)", (name,randomString(10),name+"@mail.com",))
        conn.commit()

    for i in range(reviewSeederNumber):
        c.execute("INSERT INTO reviews(movieId, userId, reviewTime, reviewText, reviewRating) VALUES (?, ?, ?, ?, ?)", (random.randint(0, userNumberSeed),random.randint(0, len(movieSeeder)), "timeDateChangeHere","greatMovie",random.randint(0, 10)))
        conn.commit()

    c.execute("SELECT * FROM movies")
    movieRows = c.fetchall()
    for movies in movieRows:
        print(movies) 

    c.execute("SELECT * FROM users")
    users = c.fetchall()
    for user in users:
        print(user) 

    c.execute("SELECT * FROM reviews")
    reviews = c.fetchall()
    for review in reviews:
        print(review) 

    print("Seeding complete")


def randomString(length):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    str = ''
    for i in range(0,length,2):
        str += random.choice(number)
        str += random.choice(alpha)
    return str


@app.route("/")
def home():
    conn = sqlite3.connect(databaseName+'.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies LIMIT 3")

    movieTop5 = c.fetchall()
    
    conn.commit()
    conn.close()

    return render_template('home.html',movieTop5=movieTop5)

@app.route("/log/", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return
    return render_template('loginpage.html')

@app.route("/movie/", methods=['GET','POST'])
def viewMovie():
    conn = sqlite3.connect(databaseName+'.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies")

    movies = c.fetchall()
    
    conn.commit()
    conn.close()

    if request.method == 'POST':
        print("Post")
        return render_template('movie.html',movies=movies)
    print("Get")
    return render_template('movie.html',movies=movies)

if __name__ == '__main__':
    print("start")
    create_database()
    app.run(debug=True)
