import xmlrpc.client

def get_products(db, uid, password):
    """Gets all products from the Odoo database."""
    url = "http://localhost:8069/xmlrpc/2/object"
    rpc = xmlrpc.client.ServerProxy(url)
    result = rpc.execute_kw(db, uid, password,
                            "product.product", "search_read", [],
                            {"fields": ["name", "price"]})
    return result

if __name__ == "__main__":
    db = "odoo16"
    uid = "openpg"
    password = "openpgpwd"
    products = get_products(db, uid, password)
    for product in products:
        print(product["name"], product["price"])