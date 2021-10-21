from flask import Flask, request,Blueprint, render_template 
  
# Flask constructor 

test = Blueprint("test", __name__, template_folder="templates")

@test.route("/")
def test():
  return render_template("loginPage.html")