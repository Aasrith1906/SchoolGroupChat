import pyodbc
from flask_login import UserMixin



class User(UserMixin):

    connection = pyodbc.connect(driver='{SQL Server}', server='.', database='ChatServer',               
                trusted_connection='yes')

    cursor = connection.cursor()

    def __init__(self , user_id):

        User.cursor.execute("SELECT * FROM ChatLogin WHERE UserID = ? ",user_id)

        user_data = User.cursor.fetchone()

        self.id = user_id
        self.username = user_data[2]
        self.password = user_data[3]

    def get_id(self):

        return self.id
        
    def __repr__(self):

        return "{}/{}/{}".format(self.user_id,self.username,self.password)




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
    def GetUserID(username):

        try:

            Login.cursor.execute("SELECT UserID FROM ChatLogin WHERE USERNAME = ?" , username) 

            rows = Login.cursor.fetchone()

            if rows:

                return int(rows[0])

            else:

                return None

        except Exception as e:

            return False



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

    Login.GetFirstName('TestUser')
