# import xmlrpclib
import xmlrpc.client as xmlrpclib

# URL of the Odoo instance
url = 'http://localhost:8069'

# Database name, username, and password
db_name = 'wsfnoticias16'
username = 'admin'
password = 'admin'

# Connect to the Odoo instance
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db_name, username, password, {})

# Create a new XML-RPC client instance
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Retrieve a list of products
product_ids = models.execute_kw(db_name, uid, password,
                                'product.product', 'search', [[]])
products = models.execute_kw(db_name, uid, password,
                             'product.product', 'read', [product_ids], {'fields': ['name', 'list_price']})

# Print the list of products
for product in products:
    print('{}: ${}'.format(product['name'], product['list_price']))

## Pruebas Junior

domain = [('importancia', '=', 'cat1'), ('estado', '=', 'on')]

medios_ids = models.execute_kw(db_name, uid, password,
                               'wsf_noticias_medios', 'search', [domain])

medios = models.execute_kw(db_name, uid, password,
                           'wsf_noticias_medios', 'read', [medios_ids])

for rec in medios:

    print("-----------")
    print("Medios:", rec)
