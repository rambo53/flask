from app import app, db
from flask import render_template
import models
import views

from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
    

if __name__ == "__main__":
    app.run()