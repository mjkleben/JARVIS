from Controller import *


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
db = firebase.database()
#-------------------------------------------------------------------------------------------------
print("Sender On.. ")
Message = ""

while True:

    #Send message
    Message = input("->").strip()
    if(Message == "cls"):
        os.system("cls")
    elif (Message == "quit"):
        db.child("My_SentMsg").set(Message)
        sys.exit(0)
    else:
        data = Message
        db.child("My_SentMsg").set(Message)

        time.sleep(1.5)
        ConsoleLog = db.child("ConsoleLog").get().val().strip()
        print(ConsoleLog)


input()