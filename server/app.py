#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# An API endpoint at /clear is available to clear your session as needed.
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return make_response(jsonify(articles), 200)

# When a user makes a GET request to /articles/<int:id>, the following should happen:
@app.route('/articles/<int:id>')
def show_article(id):
    # If this is the first request this user has made, set session['page_views'] to an initial value of 0.
    session['page_views'] = session.get('page_views') or 0
    # For every request to /articles/<int:id>, increment the value of session['page_views'] by 1.
    session['page_views'] += 1

    # If the user has viewed 3 or fewer pages, render a JSON response with the article data.
    if session['page_views'] <= 3:
        return Article.query.filter(Article.id == id).first().to_dict(), 200

    # If the user has viewed more than 3 pages, render a JSON response including an error message {'message': 'Maximum pageview limit reached'}, and a status code of 401 unauthorized. 
    return {'message': 'Maximum pageview limit reached'}, 401

if __name__ == '__main__':
    app.run(port=5555)
