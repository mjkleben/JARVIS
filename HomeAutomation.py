from Controller import *

#Setup controller

#AUTHENTICATE FIREBASE AND LOGIN
config = {
  "apiKey": "AIzaSyCkpaEJfQBZh1aBufckYMPjI1hiktwsKlA",
  "authDomain": "database-8a74e.firebaseapp.com",
  "databaseURL": "https://database-8a74e.firebaseio.com",
  "storageBucket": "database-8a74e.appspot.com"
}
email = "databasehost69@gmail.com"
password = "123456database"
firebase = initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
# Log the user in
user = auth.sign_in_with_email_and_password(email, password)
# Get a reference to the database service
google_firebase = firebase.database()


#_------------------------------------------------------------------------
def turnOff(device, state):
    google_firebase.child(device).set(state)

def turnOn(device, state):
    google_firebase.child(device).set(state)

