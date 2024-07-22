from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('index.html')

# Route for products page
@app.route('/products')
def products():
    main_products = Product.query.filter_by(category="main").all()
    return render_template('products.html', products=main_products)

# Route for category products
@app.route('/category/<string:category>')
def category_products(category):
    products = Product.query.filter_by(category=category).all()
    return render_template('category_products.html', category=category, products=products)

# Route for individual product pages
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

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

# Route for contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Process form data (e.g., save to database or send email)
        return "Thank you for your message. We'll get back to you soon!"
    return render_template('contact.html')

def add_sample_products():
    products = [
        # Main categories
        Product(name="Tablas", description="Madera de pino de alta calidad", image="tabla.jpg", category="main"),
        Product(name="Tablones y barrotes", description="Madera resistente", image="barrote.jpg", category="main"),
        Product(name="Polines", description="Madera de cedro aromática", image="polin.jpg", category="main"),
        Product(name="Triplay", description="Madera de cedro aromática", image="triplay.jpg", category="main"),
        
        # Specific products for each category
        # Tablas
        Product(name="Tabla de 8 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 10 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 12 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 14 de largo ", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 16 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 18 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 20 de largo", description="Tabla de pino en todas clase de 4 a 12 de ancho", image="tabla.jpg", category="Tablas"),
        

        
        # Barrotes y Tablones
        Product(name="Barrote de Cedro", description="Barrote de cedro de 4x4 pulgadas", image="barrote_cedro.jpg", category="Barrotes"),
        Product(name="Barrote de Pino", description="Barrote de pino tratado de 6x6 pulgadas", image="barrote_pino.jpg", category="Barrotes"),
        # Polines
        Product(name="Polín de Madera", description="Polín de madera tratada de 8 pies", image="polin_madera.jpg", category="Polines"),
        Product(name="Polín de Plástico", description="Polín de plástico reciclado de 6 pies",  image="polin_plastico.jpg", category="Polines"),
        #Triplay
        Product(name="Triplay de Pino", description="Triplay de pino de 18mm",  image="triplay_pino.jpg", category="Triplay"),
        Product(name="Triplay de Okume", description="Triplay de okume de 12mm",  image="triplay_okume.jpg", category="Triplay")
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
    
    
    """Product(name="Tabla de 4 x 8", description="Tabla de pino en todas clase de 4 x 8 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 6 x 8", description="Tabla de pino en todas clase de 6 x 8 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 8 x 8", description="Tabla de pino en todas clase de 8 x 8 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 10 x 8", description="Tabla de pino en todas clase de 10 x 8 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 12 x 8", description="Tabla de pino en todas clase de 12 x 10 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 4 x 10", description="Tabla de pino en todas clase de 4 x 10 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 6 x 10", description="Tabla de pino en todas clase de 6 x 10 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 8 x 10", description="Tabla de pino en todas clase de 8 x 10 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 10 x 10", description="Tabla de pino en todas clase de 10 x 10 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 12 x 10", description="Tabla de pino en todas clase de 12 x 10 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 4 x 12", description="Tabla de pino en todas clase de 4 x 12 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 6 x 12", description="Tabla de pino en todas clase de 6 x 12 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 8 x 12", description="Tabla de pino en todas clase de 8 x 12 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 10 x 12", description="Tabla de pino en todas clase de 10 x 12 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 12 x 12", description="Tabla de pino en todas clase de 12 x 12 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 4 x 14", description="Tabla de pino en todas clase de 4 x 14 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 6 x 14", description="Tabla de pino en todas clase de 6 x 14 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 8 x 14", description="Tabla de pino en todas clase de 8 x 14 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 10 x 14", description="Tabla de pino en todas clase de 10 x 14 pulgadas", image="tabla.jpg", category="Tablas"),
        Product(name="Tabla de 12 x 14", description="Tabla de pino en todas clase de 12 x 14 pulgadas", image="tabla.jpg", category="Tablas"),"""