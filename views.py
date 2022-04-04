from tokenize import Number
from app import app
from flask import render_template, request

@app.route("/")
def homepage():
    name = request.args.get('name') 
    number = 5#request.args.get('number') 
    if not name:
        name = "inconnu"
    test_var = {'name':name,'number':number}
    return render_template('homepage.html', test_var=test_var)