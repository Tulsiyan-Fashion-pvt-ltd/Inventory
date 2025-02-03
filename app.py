from flask import Flask, render_template, session, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "6129097fee5199dfa20d2ac8d06ba06ec3ad49c2c3a725ed18ab605e122f4d27028df18652e043e855e08f73119797e7c196b9a4141c9cb4da25d28e70f1b59c"


app.config['MYSQL_HOST'] = "skyler.cj44qsu6gnc1.eu-north-1.rds.amazonaws.com"
app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_USER"] = "admin"       
app.config["MYSQL_PASSWORD"] = "68e30d55846e57ec3ac9be24a9a74bd823933782"
app.config["MYSQL_DB"] = "maria"

mysql = MySQL(app)


@app.route("/")
def index():
    return render_template('index.html', page_name="homepage")


if __name__ == "__main__":
    app.run(debug=True)