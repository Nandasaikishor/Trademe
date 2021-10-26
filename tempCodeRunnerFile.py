

inputdata = {} 



@app.route("/")
def default():
   return render_template("index.html")

 #LOGIN

@app.route("/login/user",methods = ["GET", "POST"])