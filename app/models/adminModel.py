from flask_login import UserMixin

class AdminUser(UserMixin):
    def __init__(self, user_id, email, role):
        self.id = user_id
        self.email = email
        self.role = role