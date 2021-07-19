import unittest
from model.user_model import UserModel
from main import app, session


def sum(a, b):
    return a + b


class TestSignUp(unittest.TestCase):
    def setUp(self):
        self.test_app = app.test_client()

    def tearDown(self):
        session.query(UserModel).filter(
            UserModel.username == "fdsa",
            UserModel.password == "fdsa",
            UserModel.name == "fdsa",
            UserModel.email == "adfdd@asd.ds",
        ).delete()
        session.commit()

    def test_success_signup(self):
        response = self.test_app.post(
            "/signup",
            json={
                "username": "fdsa",
                "password": "fdsa",
                "name": "fdsa",
                "email": "adfdd@asd.ds",
            },
        )
        self.assertEqual(201, response.status_code)

        user = (
            session.query(UserModel)
            .filter(
                UserModel.username == "fdsa",
                UserModel.password == "fdsa",
                UserModel.name == "fdsa",
                UserModel.email == "adfdd@asd.ds",
            )
            .one_or_none()
        )
        self.assertIsNotNone(user)

    def test_exist_username(self):
        user = UserModel("fdsa", "fdsa", "fdsa", "adfdd@asd.ds")
        session.add(user)
        session.commit()

        response = self.test_app.post(
            "/signup",
            json={
                "username": "fdsa",
                "password": "fdsa",
                "name": "fdsa",
                "email": "adfdd@asd.ds",
            },
        )
        self.assertEqual(400, response.status_code)


unittest.main()
