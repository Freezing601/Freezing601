from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Data storage setup
DATA_FILE = 'books_data.json'
books = []

# Load initial data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        books = json.load(f)
else:
    books = [
        {
            "id": 1,
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "description": "This book teaches clean code principles with practical examples... (40+ words placeholder)",
            "price": 35.99,
            "publisher": "Prentice Hall"
        }
    ]

def save_data():
    """Save books data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(books, f)

# HTML Template (embedded in Python)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Bookstore API</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: auto; padding: 20px; }
        .book { background: #f8f9fa; padding: 15px; margin: 10px; border-left: 4px solid #3498db; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Bookstore API Interface</h1>
    <form id="bookForm">
        <input type="text" name="title" placeholder="Title" required>
        <input type="text" name="author" placeholder="Author" required>
        <textarea name="description" placeholder="Description (40+ words)" required></textarea>
        <input type="text" name="publisher" placeholder="Publisher" required>
        <input type="number" step="0.01" name="price" placeholder="Price" required>
        <button type="submit">Add Book</button>
    </form>
    <div id="bookList">
        {% for book in books %}
        <div class="book">
            <h3>{{ book.title }}</h3>
            <p><strong>Author:</strong> {{ book.author }}</p>
            <p><strong>Price:</strong> ${{ "%.2f"|format(book.price) }}</p>
            <p>{{ book.description }}</p>
        </div>
        {% endfor %}
    </div>
    <script>
    // Frontend logic
    document.getElementById('bookForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            title: e.target.title.value,
            author: e.target.author.value,
            description: e.target.description.value,
            publisher: e.target.publisher.value,
            price: parseFloat(e.target.price.value)
        };
        
        try {
            const response = await fetch('/api/books', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(await response.text());
            window.location.reload();
        } catch (error) {
            alert("Error: " + error.message);
        }
    });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Render main interface"""
    return render_template_string(HTML_TEMPLATE, books=books)

@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    """API endpoint for books"""
    if request.method == 'GET':
        return jsonify(books)
    else:
        # Validation
        required_fields = ['title', 'author', 'description', 'price', 'publisher']
        if not all(field in request.json for field in required_fields):
            return jsonify({"error": "Missing fields"}), 400
        
        if len(request.json['description'].split()) < 40:
            return jsonify({"error": "Description must be ≥40 words"}), 400

        # Add new book
        new_book = request.json
        new_book['id'] = len(books) + 1
        books.append(new_book)
        save_data()
        return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(debug=True)