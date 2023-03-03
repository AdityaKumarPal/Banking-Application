import mysql.connector
from bank import bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.cursor(user_id)


class User:
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Aditya@997", database="abi_project")
    cursor = mydb.cursor()
    cursor.execute("select * from users")
    cursor.fetchall()

