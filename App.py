from flask import Flask , render_template , redirect , url_for , session ,flash
from flask_socketio import SocketIO , emit 
from flask_wtf import FlaskForm
import data
from flask_bootstrap import Bootstrap 

from flask_login import login_user , LoginManager  , login_required , logout_user

from wtforms import StringField , SubmitField , PasswordField, TextAreaField 
from wtforms.validators import DataRequired 


active_user_list = []


class LoginForm(FlaskForm):

    username = StringField('Enter username: ',validators=[DataRequired()])
    password = PasswordField('Enter password: ',validators=[DataRequired()])
    submit = SubmitField()
    #recaptcha = RecaptchaField()

class ChatForm(FlaskForm):

    EnterMessage = TextAreaField('Enter Message:', validators=[DataRequired('Enter message')])
    submit = SubmitField()
    #logout = SubmitField()


app = Flask(__name__)

app.config['SECRET_KEY'] = 'adiao;wf0724-j1245j;12'

socketio = SocketIO(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

    return data.User(user_id)


@app.route('/' , methods = ["GET" , "POST"])
def LoginPage():

    session['Login'] = False

    form = LoginForm()

    username = ""
    password = ""

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        try:

            if "'" in username or "'" in password:

                flash("invalid username or password")

                form.username.data = ""
                form.password.data = ""

            else:


                if data.Login.TryLogin(username , password) == True:

                    session['username'] = username
                    session['firstname'] = data.Login.GetFirstName(username)
                    user_id = data.Login.GetUserID(username)

                    user = data.User(user_id)

                    login_user(user)
                    
                    return redirect(url_for('Chat'))

                else:

                    flash("invalid username or password")
                    form.username.data = ""
                    form.password.data = ""

        except Exception as e:

            print(str(e))

    return render_template('Login.html',form = form )


@app.route('/Chat',methods = ['GET' , 'POST'])
@login_required
def Chat():
    chatform = ChatForm()

    if session['username']:
        
        return render_template('Chat.html' , username = session['username'], form = chatform)

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('LoginPage'))

@socketio.on('connect', namespace='/Chat')
def connect():

    print('Client connected')
    
    if session['username'] not in active_user_list:

        active_user_list.append(session['username'])

        emit('UserConnectionResponse' , {'username':'server' , 'data':'{} has entered the chat'.format(session['firstname'])})

        

@socketio.on('UserMessage' , namespace = '/Chat')
def UserMessage(message):

    print("{}:{}".format(session['username'] , message))
    
    emit('RecieveUserMessage' , {'username':session['username'] , 'data': message})

@socketio.on('disconnect' , namespace='/Chat')
def disconnected():

    emit('UserDisconnection' , {'username':'server' , 'data':'{} has left the chat'.format(session['username'])})

    active_user_list.remove(session['username'])

    print('{} has disconnected'.format(session['username']))

if __name__ == '__main__':

    #login_manager.init_app(app)
    socketio.run(app,debug = True)
   
