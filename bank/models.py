import mysql.connector
from bank import bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.cursor(user_id)


class User(UserMixin):
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Your_MYSQL_Password", database="Database_Name")
    cursor = mydb.cursor()
    cursor.execute("select * from users")
    cursor.fetchall()

    @property
    def prettier_budget(self):
        if len(str(self.password)) >= 4:
            return f"{str(self.password)[:-3]},{str(self.password)[-3:]}$"
        else:
            return f"{self.password}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password = bcrypt.generate_password(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password(self.password, attempted_password)
