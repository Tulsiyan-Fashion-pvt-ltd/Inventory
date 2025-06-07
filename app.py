from flask import Flask, render_template, session, url_for, redirect, request, jsonify
from flask_mysqldb import MySQL
import uuid
from datetime import datetime, timedelta
import base64
creds = {'Tulsiyan-inventory__@rootUser': '033f48f54a0b6a3bd062'}


app = Flask(__name__)
app.secret_key = "6129097fee5199dfa20d2ac8d06ba06ec3ad49c2c3a725ed18ab605e122f4d27028df18652e043e855e08f73119797e7c196b9a4141c9cb4da25d28e70f1b59c"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)


# app.config['MYSQL_HOST'] = "skyler.cj44qsu6gnc1.eu-north-1.rds.amazonaws.com"
# app.config['MYSQL_PORT'] = 3306
# app.config["MYSQL_USER"] = "admin"       
# app.config["MYSQL_PASSWORD"] = "68e30d55846e57ec3ac9be24a9a74bd823933782"
# app.config["MYSQL_DB"] = "maria"


app.config['MYSQL_HOST'] = "localhost"
app.config["MYSQL_USER"] = "root"       
app.config["MYSQL_PASSWORD"] = "Tulsiyan@farhan962412"
app.config["MYSQL_DB"] = "tulsiyandb"

mysql = MySQL(app)


@app.route("/")
def index():
    if session.get('user') == None:
        return redirect('/login')

    return render_template('index.html', page_name="homepage")

class product_handler:
    def create_sku():
        return 'sku-'+str(uuid.uuid4())[:13]

    def create_productid():
        return str(uuid.uuid4())[:13]+"-"+str(int(uuid.uuid4()))[:6]


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
        skuid = product_handler.create_sku()
        title = data.get('title').strip()
        vendorid = data.get('vid', 'NULL').strip()
        product_desc = data.get('desc').strip()
        product_kwords = data.get('keywords').split(',')
        product_weight = data.get('weight').strip().strip()
        original_price = data.get('price').replace(',', '').strip()
        discounted_price = data.get('dsc-price').replace(',', '').strip()
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
        cursor.execute('''insert into inventory(skuID, vendor_id, product_desc, original_price, disc_price, product_weight_gm, 
                       product_stock, product_details, saree_len, blouse_len, product_material, product_care, product_image, 
                       product_img01, product_img02, product_img03, creation_date) values(
                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                       (skuid, vendorid, title, original_price, discounted_price, product_weight, product_stock, product_desc,
                        slen, blen, material, care, main_image, img02, img03, img04, date))
        
        for _ in product_kwords:
            keyword = _.strip()
            cursor.execute('''insert into searching_keywords(skuID, search_result) values(%s, %s)''',
                           (skuid, keyword))
            
        for _ in range(int(product_stock)):
            productid = product_handler.create_productid()
            cursor.execute('''insert into products(skuID, productID) values(%s, %s)''', (skuid, productid))

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
        return render_template('edit.html', page_name="edit products", material=saree_materials)
    else:
        skuid = session.get('skuid')
        if request.content_type == 'application/json':
            query = request.get_json().get('query')
            session['skuid'] = query
            
            # write a function to fetch the provided query and fetch the product data and return
            cursor = mysql.connection.cursor()
            data = cursor.execute('''
                            select vendor_id, product_desc, original_price, disc_price, product_weight_gm, 
                       product_stock, product_details, saree_len, blouse_len, product_material, product_care, product_image, 
                       product_img01, product_img02, product_img03
                       from inventory where skuID=%s
                       ''', (query, ))

            data = cursor.fetchone()
            cursor.close()
            # print(data)
            product_details = {
                'img01': base64.b64encode(data[11]).decode('utf-8'),
                'img02': base64.b64encode(data[12]).decode('utf-8'),
                'img03': base64.b64encode(data[13]).decode('utf-8'),
                'img04': base64.b64encode(data[14]).decode('utf-8'),
                'title': data[1],
                'vid': data[0],
                'desc': data[6],
                'weight': data[4],
                'og_price': data[2],
                'disc_price': data[3],
                'stock': data[5],
                'slen': data[7],
                'blen': data[8],
                'material': data[9],
                'care': data[10]
            }

            cursor = mysql.connection.cursor()
            cursor.execute('''
                           select search_result from searching_keywords where skuId = %s
                           ''', (query, ))

            keywords = cursor.fetchall()
            cursor.close()

            keywords = [ item[0]
                for item in keywords
            ]
            # print(keywords)
            response_data = {'data': product_details, 'keywords': (', ').join(keywords)}
            # print(response_data)
            return jsonify(response_data)

        # when the update buttons is clicked update the data
        data = request.form
        title = data.get('title').strip()
        vendorid = data.get('vid', 'NULL').strip()
        product_desc = data.get('desc').strip()
        product_kwords = data.get('keywords').split(',')
        product_weight = data.get('weight').strip().strip()
        original_price = data.get('price').replace(',', '').strip()
        discounted_price = data.get('dsc-price').replace(',', '').strip()
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
        cursor.execute('''
                       update inventory set
                       product_desc = %s,
                       vendor_id = %s,
                       product_details = %s, 
                       product_weight_gm = %s,
                       original_price = %s, 
                       disc_price = %s, 
                       product_stock = %s, 
                       saree_len = %s, 
                       blouse_len = %s,
                       product_material = %s,
                       product_care = %s,
                       updation_date = %s
                       where skuID = %s
        ''', (title, vendorid, product_desc, product_weight, original_price, discounted_price, product_stock, slen, blen, material, care, date, skuid))
        
        if file01 and file02 and file03 and file04:
            cursor.execute('''update inventory
                            set product_image = %s,
                            product_img01 = %s,
                            product_img02 = %s,
                            product_img03 = %s
                            ''', (main_image, img02, img03, img04))

        # clearing all the prev searching keywords
        cursor.execute('''
                            delete from searching_keywords where skuID = %s''', (skuid, ))

        # assigning new skuids for the new stock
        cursor.execute('''
                            delete from products where skuID = %s''', (skuid, ))
        for _ in product_kwords:
            keyword = _.strip()

            cursor.execute('''insert into searching_keywords(skuID, search_result) values(%s, %s)''',
                           (skuid, keyword))
            
        for _ in range(int(product_stock)):
            productid = product_handler.create_productid()
            cursor.execute('''insert into products(skuID, productID) values(%s, %s)''', (skuid, productid))

        mysql.connection.commit()
        cursor.close()
        print('product updated successfully *_*')
        return redirect('/edit')
    

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
