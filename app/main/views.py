from flask import Flask, render_template, Blueprint, redirect, request, url_for, flash
from main.model import Favorite, db
import requests

main_bp = Blueprint('main', __name__, url_prefix = '/main')

@main_bp.route("/")
def get_articles():

    response = requests.get("https://qiita.com/api/v2/items?query=python&per_page=5")
    qiita_data = response.json()

    clean_articles = []

    for item in qiita_data:
        clean_articles.append({"title": item["title"],
                               "url": item["url"]})
        
    return render_template("index.html", articles = clean_articles)


@main_bp.route("/favorite/add", methods=["POST"])
def add_favorite():

    if request.method == "POST":
        title = request.form['title']
        url = request.form['url']

        if (Favorite.query.filter_by(url = url).first() != None):
            flash("既に登録しています")
            return redirect(url_for("main.get_articles"))
        
        favorite = Favorite(title = title, url = url)

        db.session.add(favorite)
        db.session.commit()

        return redirect(url_for("main.get_articles"))
    

@main_bp.route("/favorite/list")
def list_favorite():

    favorite_list = Favorite.query.all()

    return render_template("favorite_list.html", favorite_list = favorite_list)

@main_bp.route("/favorite/delete/<int:favorite_id>", methods = ["POST"])
def delete_favorite(favorite_id):

    if request.method == "POST":
        target_article = Favorite.query.get_or_404(favorite_id)

        db.session.delete(target_article)
        db.session.commit()

    return redirect( url_for("main.list_favorite") )
