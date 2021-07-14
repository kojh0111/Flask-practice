from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base
from model.user_model import UserModel

engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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
