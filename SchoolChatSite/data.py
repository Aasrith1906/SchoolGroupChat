import pyodbc
from flask_login import UserMixin



class User(UserMixin):

    connection = pyodbc.connect(driver='{SQL Server}', server='.', database='ChatServer',               
                trusted_connection='yes')
    cursor = connection.cursor()

    def __init__(self , username):

        User.cursor.execute("SELECT * FROM ChatLogin WHERE Username = ?"  , username)

        user_data = User.cursor.fetchone()

        if user_data:

            self.user_id = user_data[0]
            self.first_name = user_data[1]
            self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def set_id(self, user_id):
        self.user_id = user_id
            
    def get_id(self):

        return str(self.user_id)




class Login():


    connection = pyodbc.connect(driver='{SQL Server}', server='.', database='ChatServer',               
                trusted_connection='yes')

    cursor = connection.cursor()

    @staticmethod
    def TryLogin(username , password):

        parameters = (username , password)

        try:

            Login.cursor.execute("{CALL TRY_LOGIN (? , ?)}" , parameters)

            rows = Login.cursor.fetchone()

            if rows[0] == 1:

                return True

            else:

                return False

        except Exception as e:

            print(str(e))

    @staticmethod
    def GetFirstName(username):

        try:

            Login.cursor.execute("SELECT FirstName FROM ChatLogin WHERE USERNAME = ?" , username)

            

            rows = Login.cursor.fetchone()

            if rows:

                return rows[0]

            else:

                return None

        except Exception as e:

            return False

if __name__ == '__main__':

    Login.GetFirstName('Aasrith1906')
