# importing Flask and other modules
import mysql.connector

from flask import Flask, request, render_template 
  
# Flask constructor
app = Flask(__name__)   
  
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def signin():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       usern = request.form.get("user")
       #print(usern)
       # getting input with name = lname in HTML form 
       #mail_id = request.form.get("email")
       password = request.form.get("password")
       #phoneno = request.form.get("phone")
       #print("Your regst is "+usern + password)
       mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="sql@123#",
       database="stocks"
       )
       #mycursor = mydb.cursor()
       #mycursor.execute("CREATE TABLE Userregst (Username VARCHAR(255), mail_id VARCHAR(255), pswrd VARCHAR(255), phoneno INT(100),PRIMARY KEY (`mail_id`))")
       mycursor = mydb.cursor()
       mycursor.execute("SELECT * from Userregst")
       myresult = mycursor.fetchall()
    #   for x in myresult:
          # print(x)
           

       userstatement = f"SELECT Username FROM Userregst WHERE Username = '{usern}';"
       mycursor.execute(userstatement)
       userfound = mycursor.fetchall() 
       x = userfound[0]

       if(x[0] == usern): 
           print(usern)
           passwordstatement = f"SELECT pswrd FROM Userregst WHERE Username = '{x[0]}';" 
           mycursor.execute(passwordstatement)
           passwordfound = mycursor.fetchall()
           y=passwordfound[0]
           print(y[0])  
           password=password.replace("'","")
           print(password)
           if(y[0] == password):
               print("logged")
       
         

      
       return "Your regst is "+usern+password
    
    
    return render_template("Loginpage.html")
  
if __name__=='__main__':
   app.run()