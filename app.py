from flask import Flask, render_template, jsonify, request
from werkzeug.exceptions import NotFound, Unauthorized
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_authorize import Authorize
import model

db = SQLAlchemy()
app = Flask(__name__)
login = LoginManager(app)
authorize = Authorize(app)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///db.mysql'


@app.route('/articles/', methods=['POST'])
@login.logged_in
@authorize.create(model.Article)
def article():
    article = model.Article(
        name=request.json.get('name'),
        content=request.json.get('content'),
    )
    db.session.add(article)
    db.session.commit()
    return jsonify(msg='Created Article'), 200


@app.route('/articles/<int:ident>', methods=['GET', 'PUT', 'DELETE'])
@login.logged_in
def single_article(ident):
    article = db.session.query(model.Article).filter_by(id=ident).first()
    if not article:
        raise NotFound

    if request.method == 'GET':
        if not authorize.read(article):
            raise Unauthorized

        return jsonify(id=article.id, name=article.name), 200

    elif request.method == 'PUT':
        if not authorize.update(article):
            raise Unauthorized

        if 'name' in request.json:
            article.name = request.json['name']

        if 'content' in request.json:
            article.content = request.json['content']
            db.session.commit()

        return jsonify(id=article.id, name=article.name), 200

    elif request.method == 'DELETE':
        if not authorize.delete(article) or \
                not authorize.has_role('admin'):
            raise Unauthorized

        db.session.delete(article)
        db.session.commit()
        return


@app.route('articles/<int:ident>/revoke', methods=['POST'])
@login.logged_in
def revoke_article(ident):
    article = db.session.query(model.Article).filter_by(id=ident).first()
    if not article:
        raise NotFound

    if not authorize.revoke(article):
        raise Unauthorized

    article.revoke = True
    db.session.commit()

    return



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cycles/')
def cycles():
    return render_template('cycles.html')


@app.route('/brands/')
def brands():
    return render_template('brands.html')


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
