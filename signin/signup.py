# importing Flask and other modules
import mysql.connector
from flask import Flask, request, render_template 
  
# Flask constructor
app = Flask(__name__)   
  
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def vald():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       usern = request.form.get("user")
       print(usern)
       # getting input with name = lname in HTML form 
       mail_id = request.form.get("email")
       password = request.form.get("pswrd")
       phoneno = request.form.get("phone")
       print("Your regst is "+usern + mail_id + password + phoneno)
       

       mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="sql@123#",
       database="stocks"
       )
       mycursor = mydb.cursor()
       #mycursor.execute("CREATE TABLE Userregst (Username VARCHAR(255), mail_id VARCHAR(255), pswrd VARCHAR(255), phoneno VARCHAR(100),PRIMARY KEY (`mail_id`))")
       sql = "INSERT INTO Userregst (Username,mail_id,pswrd,phoneno ) VALUES (%s, %s, %s, %s)"
       val = (usern, mail_id, password,phoneno)
       mycursor.execute(sql, val)
       mydb.commit()
       if all([usern, mail_id, password,phoneno]):
           print(mycursor.rowcount, "record inserted.")
       else:
           print("u missed data")
            
       print(mycursor.rowcount, "record inserted.")

       return "Your regst is "+usern + mail_id + password + phoneno
    return render_template("validation.html")
  
if __name__=='__main__':
   app.run()