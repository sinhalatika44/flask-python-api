from app.models.user import User

class AuthService:
    def user_exists(self, username, email):
        return User.query.filter((User.username == username) | (User.email == email)).first() is not None