from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base
from model.user_model import UserModel

engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


@app.route("/signup", methods=["POST"])
def signUp():
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    email = request.form.get("email")

    user = UserModel(username, password, name, email)
    session.add(user)
    session.commit()

    return "Sign Up Successfully"


@app.route("/signin", methods=["POST"])
def signIn():
    username = request.form.get("username")
    password = request.form.get("password")
    user = (
        session.query(UserModel)
        .filter(
            UserModel.username == username, UserModel.password == password
        )  # SQL WHERE문
        .one_or_none()
    )
    if user is None:
        return "No User"

    return "Sign In Successfully"


@app.route("/user/password", methods=["PATCH"])
def change_password():
    username = request.form.get("username")
    password = request.form.get("password")
    new_password = request.form.get("new_password")
    user = (
        session.query(UserModel)
        .filter(UserModel.username == username, UserModel.password == password)
        .one_or_none()
    )
    if user is None:
        return "Password is wrong"

    find_user = (
        session.query(UserModel).filter(UserModel.username == username).one_or_none()
    )
    find_user.password = new_password
    session.add(find_user)
    session.commit()

    return "Change password Successfully"

@app.route("/user/delete", methods=["DELETE"])
def delete_account():
    email = request.form.get("email")
    password = request.form.get("password")
    user = (
        session.query(UserModel)
        .filter(UserModel.email == email, UserModel.password == password)
        .one_or_none()
    )
    if user is None:
        return "Password is wrong"
    session.delete(user)
    session.commit()

    return "Bye"

app.run(debug=True)
