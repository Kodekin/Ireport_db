from app.db_config import init_db
import time, datetime
from ..base_model import BaseClassModel




class UsersModel(BaseClassModel):

    def __init__(self):

        self.db = init_db()

    def save(self, firstname, lastname, email, username, password):
        user = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "username": username,
            "password": password,
            
        }
        _record = self.user_exists(user['username'])
        if _record:
            return "Username '{}' already exists".format(username)
        else:
            query = """INSERT INTO users (firstname, lastname, email, username, password) VALUES
                        (%(firstname)s, %(lastname)s, %(email)s, %(username)s, %(password)s ) RETURNING username """
            curr = self.db.cursor()
            curr.execute(query, user)
            username = curr.fetchone()[0]
            self.db.commit()
            return username

    def user_exists(self, username):
        curr = self.db.cursor()
        query = "SELECT username, password FROM users WHERE username='{}';".format(username)
        curr.execute(query)
        return curr.fetchone()


    def logout_user(self, token):
        """This function logs out a user by adding thei token to the blacklist table"""
        conn = self.db
        curr = conn.cursor()
        query = """
                INSERT INTO blacklist 
                VALUES (%(tokens)s) RETURNING tokens;
                """
        inputs = {"tokens": token}
        curr.execute(query, inputs)
        blacklisted_token = curr.fetchone()[0]
        conn.commit()
        curr.close()
        return blacklisted_token
