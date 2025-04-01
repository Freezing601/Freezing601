from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Sample initial book data
books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "description": "Teaches writing clean code...",
        "price": 35.99,
        "publisher": "Prentice Hall"
    }
]

@app.route('/api/books', methods=['GET'])
def get_books():
    """Return all books in JSON format"""
    return jsonify(books)

@app.route('/api/books', methods=['POST'])
def add_book():
    """Add a new book to the collection"""
    new_book = request.json
    
    # Validate required fields
    required = ['title', 'author', 'price']
    if not all(field in new_book for field in required):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Add new book with auto-increment ID
    new_book['id'] = len(books) + 1
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/')
def home():
    """Display API information"""
    return "Freezing's Computer Bookstore API is running!"

if __name__ == '__main__':
    app.run(debug=True)