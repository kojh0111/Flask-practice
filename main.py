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


app.run(debug=True)
"""
# Insert user
user = UserModel("username", "1234", "JH", "jh@bo.b")
session.add(user)

# select user by name
selected_users = session.query(UserModel).filter(UserModel.name == "bob").all()
bob = session.query(UserModel).filter(UserModel.name == "bob").one_or_none()

# Update password
bob.password = "2345"
session.add(bob)
session.commit()

# delete user by name
jh = session.query(UserModel).filter(UserModel.name == "JH").one_or_none()
session.delete(jh)

session.commit()
*/
"""
