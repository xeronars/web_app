# app.py file content

# Import the Flask class
from flask import Flask

# Create an instance of the Flask class. 
# __name__ helps Flask find template and static files.
app = Flask(__name__)


# Define a route with the @app.route decorator.
# This tells Flask what URL should trigger our function.
@app.route('/')
def home():  
    "default route"
    return '<h1>Hello, World! From my first Flask app!</h1>'


@app.route('/about')
def about():
    return 'This is the About page.'


# This ensures the server only runs if the script is executed directly.
if __name__ == '__main__':
    app.run(debug=True)