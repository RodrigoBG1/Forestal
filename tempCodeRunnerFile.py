from flask import Flask, render_template, request, jsonify
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
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100))

# Route for home page
@app.route('/')
def index():  # or def home():
    return render_template('index.html')

# Route for products page
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)
 
def add_sample_products():
    products = [
        Product(name="Tablas", description="Madera de pino de alta calidad", price=100.00, image="tabla.jpg"),
        Product(name="Barrotes", description="Madera ", price=150.00, image="barrote.jpg"),
        Product(name="Polines", description="Madera de cedro aromática", price=200.00, image="polin.jpg"),
        Product(name="Triplay", description="Madera de cedro aromática", price=200.00, image="triplay.jpg")
    ]
    
    for product in products:
        existing_product = Product.query.filter_by(name=product.name).first()
        if not existing_product:
            db.session.add(product)
    
    db.session.commit()
    
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
        'price': product.price
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_products()
    app.run(debug=True)