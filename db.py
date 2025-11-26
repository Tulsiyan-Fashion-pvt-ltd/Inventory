from flask_mysqldb import MySQL
from helpers import*

mysql = MySQL()

# server initialization
def init_db(app):
    mysql.init_app(app) 

def add_product(skuid, vendorid, title, product_kwords, original_price, discounted_price, product_weight, product_stock, product_desc,
                    slen, blen, material, color, care, date, main_image=None, img02 =None, img03=None, img04=None):
    cursor = mysql.connection.cursor()

    # compressed files
    if (main_image != None and img02 != None and img03 != None and img04 != None):
        comp1 = compress_image(main_image)
        comp2 = compress_image(img02)
        comp3 = compress_image(img03)
        comp4 = compress_image(img04)

        main_image = compress_main_image(main_image)
        img02 = compress_main_image(img02)
        img03 = compress_main_image(img03)
        img04 = compress_main_image(img04)
    else:
        comp1 = comp2 = comp3 = comp4 = None

    cursor.execute('''insert into inventory(skuID, vendor_id, product_desc, original_price, disc_price, product_weight_gm, 
                   product_stock, product_details, saree_len, blouse_len, product_material, product_color, product_care, product_image, 
                   product_img01, product_img02, product_img03, creation_date) values(
                   %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                   (skuid, vendorid, title, original_price, discounted_price, product_weight, product_stock, product_desc,
                    slen, blen, material, color, care, comp1, comp2, comp3, comp4, date))
    
    
    cursor.execute('''insert into images(skuID, img1, img2, img3, img4)
                   values(%s, %s, %s, %s, %s)
                   ''', (skuid, main_image, img02, img03, img04))
    
    for _ in product_kwords:
        keyword = _.strip()
        # print(skuid, keyword)
        cursor.execute('''insert into searching_keywords(skuID, search_result) values(%s, %s)''',
                       (skuid, keyword))
        
    for _ in range(int(product_stock)):
        productid = product_handler.create_productid()
        cursor.execute('''insert into products(skuID, productID) values(%s, %s)''', (skuid, productid))
    mysql.connection.commit()
    cursor.close()
    return
