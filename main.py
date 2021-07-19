from flask import Flask, jsonify, request
from flask.wrappers import Response
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
    username = request.form["username"]
    password = request.form["password"]
    name = request.form["name"]
    email = request.form["email"]

    find_user = (
        session.query(UserModel).filter(UserModel.username == username).one_or_none()
    )

    if find_user is not None:
        return "You can't create account. There is a same username."

    user = UserModel(username, password, name, email)
    session.add(user)
    session.commit()

    return Response("Sign Up Successfully", status=201)


@app.route("/signin", methods=["POST"])
def signIn():
    username = request.form["username"]
    password = request.form["password"]
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
    username = request.form["username"]
    password = request.form["password"]
    new_password = request.form["new_password"]
    user = (
        session.query(UserModel)
        .filter(UserModel.username == username, UserModel.password == password)
        .one_or_none()
    )
    if user is None:
        return "Password is wrong"

    user.password = new_password
    session.add(user)
    session.commit()

    return "Change password Successfully"


@app.route("/user/delete", methods=["DELETE"])
def delete_account():
    email = request.form["email"]
    password = request.form["password"]
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
