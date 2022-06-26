from cgitb import text
from datetime import datetime
from turtle import title

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    anons = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        anons = request.form['anons']
        text = request.form['full_text']
        
        
        article = Article(title=title, anons=anons, text=text)
        
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/news')    
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("news/create.html")

@app.route('/news')
def news_index():
    article = Article.query.order_by(Article.data.desc()).all()
    return render_template("news/news_index.html", article=article)



@app.route('/news/<int:pk>')
def news_detail(pk):
    article = Article.query.get(pk)
    return render_template("news/news_detail.html", article=article)

@app.route('/news/<int:pk>/del')
def news_del(pk):
    articles = Article.query.get_or_404(pk)

    try:
        db.session.delete(articles)
        db.session.commit()
        return redirect('/news')
    except:
        return "При удалении произошла ошибка"

@app.route('/news/<int:pk>/update', methods=['GET', 'POST'])
def news_update(pk):
    article = Article.query.get_or_404(pk)
    if request.method == 'POST':
        article.title = request.form['title']
        article.anons = request.form['anons']
        article.text = request.form['full_text']
        
        try:
            db.session.commit()
            return redirect('/news')    
        except:
            return "При обнавлении статьи произошла ошибка"
    else:
        return render_template("news/news_update.html", article=article)


