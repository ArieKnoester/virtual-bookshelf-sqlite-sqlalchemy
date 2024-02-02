from flask import Flask, render_template, request, redirect, url_for
from models.book import Book, db


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(
            db.select(Book)
        )
        all_books = result.scalars()
        return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(
                title=request.form["title"],
                author=request.form["author"],
                rating=request.form["rating"],
            )
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit_rating/<int:book_id>", methods=["GET", "POST"])
def edit_rating(book_id):
    if request.method == "POST":
        with app.app_context():
            book_to_update = db.session.execute(
                db.select(Book).filter_by(id=book_id)
            ).scalar()
            book_to_update.rating = request.form["new_rating"]
            db.session.commit()
            return redirect(url_for('home'))

    with app.app_context():
        result = db.session.execute(
            db.select(Book).filter_by(id=book_id)
        )
        book_to_edit = result.scalar_one()
        return render_template("edit_rating.html", book=book_to_edit)


@app.route("/delete/<int:book_id>")
def delete(book_id):
    with app.app_context():
        book_to_delete = db.session.execute(
            db.select(Book).filter_by(id=book_id)
        ).scalar_one()
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
