# Project 1 : Book Review Hub
Book Review Hub is book review website. Users will be able to register for this website and then log in using their email and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. Project also uses a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience.

## Features
Sign In/Register:Through Registration form new users can easily create account and existing users can Sign In providing email and password.
Email must be unique for every user.
Search:Through Search button user can search books providing Book name, Isbn Number or Authors Name which are avialable in database.
To access this feature user must be Logged In.
Review Submissions:Through Review Submission user can submit his/her review about a book and it will be displayed in review section of that book.User must be logged in to submit review and read other users reviews.
Book Review Hub Api:Through this anyone can get information about a book providing book's Isbn Number.
Example: http://127.0.0.1:5000/api/isbn/
         http://127.0.0.1:5000/api/8129115301/
         Result:{"author":"Chetan Bhagat","isbn":"8129115301","review_count":3,"title":"Two States","year":2009}

### Prerequisites

What things you need to install the software and how to install them
* Python version 3.6 or higher
* pip (Package Installer)
* Flask - pip install Flask
* Flask-Session - pip install Flask-Session
* psycopg2 - pip install psycopg2-binary
* SQLAlchemy - pip install SQLAlchemy


## Built With

* [Flask 1.0.2](http://flask.pocoo.org/) - Web microframework
* [Python 3.7.2](https://www.python.org/downloads/) - It is Programming language used to write code of Webite 
* [Goodreads API](https://www.goodreads.com/api) - It is book review website used to access review data for individual books
* [Heroku](https://www.heroku.com/) - Cloud Application Platform used to host database online 
* [Adminer](https://adminer.cs50.net/) -Database Manager used to manage the database 

## Authors

* **Rajat Rajdeep**  [Book Review Hub](https://github.com/submit50/rajatrajdeep.git)
