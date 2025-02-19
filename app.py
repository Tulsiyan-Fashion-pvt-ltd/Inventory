from flask import Flask, render_template, session, url_for, redirect, request
from flask_mysqldb import MySQL
import uuid
from datetime import datetime
creds = {'Tulsiyan-inventory__@rootUser': '033f48f54a0b6a3bd062'}


app = Flask(__name__)
app.secret_key = "6129097fee5199dfa20d2ac8d06ba06ec3ad49c2c3a725ed18ab605e122f4d27028df18652e043e855e08f73119797e7c196b9a4141c9cb4da25d28e70f1b59c"


app.config['MYSQL_HOST'] = "skyler.cj44qsu6gnc1.eu-north-1.rds.amazonaws.com"
app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_USER"] = "admin"       
app.config["MYSQL_PASSWORD"] = "68e30d55846e57ec3ac9be24a9a74bd823933782"
app.config["MYSQL_DB"] = "maria"


# app.config['MYSQL_HOST'] = "localhost"
# app.config["MYSQL_USER"] = "root"       
# app.config["MYSQL_PASSWORD"] = "9624"
# app.config["MYSQL_DB"] = "tulsiyandb"

mysql = MySQL(app)


@app.route("/")
def index():
    if session.get('user') == None:
        return redirect('/login')

    return render_template('index.html', page_name="homepage")

# to generate unique value
def generate_unique_id():  
    return str(uuid.uuid4())



saree_materials = [
    "Banarasi Silk", "Kanchipuram Silk", "Tussar Silk", "Mysore Silk",
    "Handloom Cotton", "Chanderi Cotton", "Tant Cotton",
    "Georgette", "Chiffon", "Crepe", "Net", 
    "Linen", "Satin", "Organza", "Velvet"
]

@app.route("/add", methods = ['POST', 'GET'])
def add():
    if session.get('user') == None:
        return redirect('/login')

    if request.method == "GET":
        return render_template('add.html', page_name="add products", material=saree_materials)
    else:
        data = request.form
        productid = str(uuid.uuid4()).strip().strip()
        title = data.get('title').strip()
        vendorid = data.get('vid', 'NULL').strip()
        product_desc = data.get('desc').strip()
        product_kwords = data.get('keywords').split(',')
        product_weight = data.get('weight').strip().strip()
        product_price = data.get('price').replace(',', '').strip()
        product_stock = data.get('stock').strip().strip()
        slen = data.get('slen').strip().strip()
        blen = data.get('blen').strip().strip()
        material = data.get('material').strip().strip()
        care = data.get('product-care').strip().strip()

        file01 = request.files['img01']
        main_image = file01.read()

        file02 = request.files['img02']
        img02 = file02.read()
        
        file03 = request.files['img03']
        img03 = file03.read()
        
        file04 = request.files['img04']
        img04 = file04.read()

        date = datetime.now()
        date = date.strftime("%Y-%m-%d")
        cursor = mysql.connection.cursor()
        cursor.execute('''insert into inventory(productID, vendor_id, product_desc, product_price, product_weight_gm, 
                       product_stock, product_details, saree_len, blouse_len, product_material, product_care, product_image, 
                       product_img01, product_img02, product_img03, creation_date) values(
                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                       (productid, vendorid, title, product_price, product_weight, product_stock, product_desc,
                        slen, blen, material, care, main_image, img02, img03, img04, date))
        
        for _ in product_kwords:
            keyword = _.strip()
            cursor.execute('''insert into searching_keywords(productId, search_result) values(%s, %s)''',
                           (productid, keyword))
        mysql.connection.commit()
        cursor.close()
        return redirect('/add')
    


@app.route("/draft", methods=['POST', 'GET'])
def draft():
    if session.get('user') == None:
        return redirect('/login')
    
    if request.method == "GET":
        return render_template('draft.html', page_name="draft products")



@app.route("/edit", methods=['POST', 'GET'])
def edit():
    if session.get('user') == None:
        return redirect('/login')
    
    if request.method == "GET":
        return render_template('edit.html', page_name="edit products")
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        empl_code = data.get('empl-code')
        psswrd = data.get('password')

        if empl_code and psswrd:
            if creds[empl_code] != psswrd:
                return redirect('/login')
            else:
                session['user'] = empl_code
                return redirect('/')
        else:
            return redirect('/login')
        
    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)