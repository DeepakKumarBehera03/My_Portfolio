from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from forms import ContactForm
import smtplib

response = smtplib.SMTP("smtp.gmail.com", 587)
response.starttls()

app = Flask(__name__)
app.config['SECRET_KEY'] = "deepakkumar"
bootstrap5 = Bootstrap5(app)

ckeditor = CKEditor(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class ContactUser(UserMixin, db.Model):
    __tablename__ = "ContactUser"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup")
def signup():
    return render_template("project.html")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data
        new_user = ContactUser(
            email=form.email.data,
            name=form.name.data,
            phone_number=form.phone.data,
            message=form.message.data,
        )
        db.session.add(new_user)
        db.session.commit()
        response.login("deepakjgrt99@gmail.com", "eljlasisljrvlxkx")
        message = f"We will get in touch with you very soon. And we resolve your queries as soon as possible"
        response.sendmail("deepakjgrt99@gmail.com", f"{form.email.data}", message)
        flash("Your Queries is Successfully Submitted, We will resolve it as soon as possible")
        return redirect(url_for('contacts'))
    return render_template("contacts.html", contact_form=form)


@app.route("/posts")
def posts():
    return render_template("posts.html")


if __name__ == "__main__":
    app.run(debug=True)
