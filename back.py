from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///woodproducts.db'
db = SQLAlchemy(app)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))
    category = db.Column(db.String(50), nullable=False)

# Route for home page
@app.route('/')
def index():
    logo = 'logo.png'
    venta= 'venta.jpg'
    canteado='canteado.jpg'
    tres='tres.jpeg'
    
    return render_template('index.html', logo=logo, venta=venta, canteado=canteado, tres=tres)

# Route for products page
@app.route('/products')
def products():
    main_products = Product.query.filter_by(category="main").all()
    return render_template('products.html', products=main_products, logo='logo.png')

# Route for category products
@app.route('/category/<string:category>')
def category_products(category):
    products = Product.query.filter_by(category=category).all()
    return render_template('category_products.html', category=category, products=products, logo='logo.png')

# Route for individual product pages
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product, logo='logo.png')

# API route for product data
@app.route('/api/products')
def api_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category': product.category
    } for product in products])
    
@app.route('/search')
def search():
    query = request.args.get('query', '')
    products = Product.query.filter(Product.name.ilike(f'%{query}%') | 
                                    Product.description.ilike(f'%{query}%')).all()
    return render_template('search_results.html', products=products, query=query, logo='logo.png')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'  # Outlook SMTP server
app.config['MAIL_PORT'] = 587  # Outlook SMTP port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'forestalweb@outlook.com'
app.config['MAIL_PASSWORD'] = 'web12345'
app.config['MAIL_DEFAULT_SENDER'] = 'forestalweb@outlook.com'

mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Send email
        msg = Message("New Contact Form Submission", 
                      recipients=["Forestalweb@outlook.com"])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        
        return "Gracias por tu mensaje. Nos pondremos en contacto contigo pronto!"
    
    return render_template('contact.html', logo='logo.png')

def add_sample_products():
    products = [
        # Main categories
        Product(name="Tablas", description="Madera de pino de alta calidad", image="tabla.jpg", category="main"),
        Product(name="Tablones y barrotes", description="Madera  de pino con espesor de 5/4 y 6/4", image="barrote.jpg", category="main"),
        Product(name="Polines", description="Madera de pino de 3x3 ", image="polin.jpg", category="main"),
        Product(name="Triplay", description="Madera de cedro aromática", image="triplay.jpg", category="main"),
        
        # Tablas
        Product(name="Tabla de 8 de largo", description="Tabla de pino en todas clase de 4 a 12 pulgadas de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 10 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 12 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 14 de largo ", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 16 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 18 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 20 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        
        # Barrotes y Tablones
        Product(name="Tablón de 8 de largo", description="Tablón de pino en todas clase de 4 a 12 pulgadas de ancho", image="barrote.jpg", category="Tablones y barrotes"),
        Product(name="Tablón de 10 de largo", description="Tablón de pino en todas clase de 4 a 12 de ancho", image="barrote.jpg", category="Tablones y barrotes"),
        Product(name="Tablón de 12 de largo", description="Tablón de pino en todas clase de 4 a 12 de ancho", image="barrote.jpg", category="Tablones y barrotes"),
        Product(name="Tablón de 14 de largo ", description="Tablón de pino en todas clase de 4 a 12 de ancho", image="barrote.jpg", category="Tablones y barrotes"),
        Product(name="Tablón de 16 de largo", description="Tablón de pino en todas clase de 4 a 12 de ancho", image="barrote.jpg", category="Tablones y barrotes"),
        Product(name="Tablón de 18 de largo", description="Tablón de pino en todas clase de 4 a 12 de ancho", image="barrote.jpg", category="Tablones y barrotes"),
        Product(name="Tablón de 20 de largo", description="Tablón de pino en todas clase de 4 a 12 de ancho", image="barrote.jpg", category="Tablones y barrotes"), 
               
        # Polines
        Product(name="Polin de 8 de largo", description="Polin de pino en todas clase de 4 a 12 pulgadas de ancho", image="polin.jpg", category="Polines"),
        Product(name="Polin de 10 de largo", description="Polin de pino en todas clase de 4 a 12 de ancho", image="polin.jpg", category="Polines"),
        Product(name="Polin de 12 de largo", description="Polin de pino en todas clase de 4 a 12 de ancho", image="polin.jpg", category="Polines"),
        Product(name="Polin de 14 de largo ", description="Polin de pino en todas clase de 4 a 12 de ancho", image="polin.jpg", category="Polines"),
        Product(name="Polin de 16 de largo", description="Polin de pino en todas clase de 4 a 12 de ancho", image="polin.jpg", category="Polines"),
        Product(name="Polin de 18 de largo", description="Polin de pino en todas clase de 4 a 12 de ancho", image="polin.jpg", category="Polines"),
        Product(name="Polin de 20 de largo", description="Polin de pino en todas clase de 4 a 12 de ancho", image="polin.jpg", category="Polines"), 

        #Triplay
        Product(name="Triplay de 5.5 mm", description="Hoja de Triplay de 5.5 mm cd ",  image="triplay.jpg", category="Triplay"),
        Product(name="Triplay de 12 mm", description="Hoja de Triplay de 12 mm para cimbra ",  image="triplay.jpg", category="Triplay"),
        Product(name="Triplay de 16 mm", description="Hoja de Triplay de 16 mm para cimbra ",  image="triplay.jpg", category="Triplay"),
        Product(name="Triplay de 19 mm", description="Hoja de Triplay de 19 mm para cimbra ",  image="triplay.jpg", category="Triplay"),
        Product(name="Triplay de 12 mm", description="Hoja de Triplay de 12 mm de segunda",  image="triplay.jpg", category="Triplay"),
        Product(name="Triplay de 16 mm", description="Hoja de Triplay de 16 mm de segunda ",  image="triplay.jpg", category="Triplay"),
        Product(name="Triplay de 19 mm", description="Hoja de Triplay de 19 mm de segunda ",  image="triplay.jpg", category="Triplay"),
    ]
    
    for product in products:
        existing_product = Product.query.filter_by(name=product.name).first()
        if not existing_product:
            db.session.add(product)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_products()
    app.run(debug=True)        
    
    