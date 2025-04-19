from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# This will act as an in-memory "database" for our books
books_db = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-book', methods=['POST'])
def add_book():
    book_id = request.form.get('book-id')
    title = request.form.get('book-title')
    author = request.form.get('book-author')

    if book_id in books_db:
        return jsonify({"message": "Book ID already exists!"}), 400
    if book_id and title and author:
        books_db[book_id] = {"book_id": book_id, "title": title, "author": author}
        return jsonify({"message": "Book added successfully!"}), 200
    else:
        return jsonify({"message": "Please fill in all fields!"}), 400

@app.route('/search-book', methods=['GET'])
def search_book():
    query = request.args.get('query')
    if not query:
        return jsonify({"message": "Please enter a search query"}), 400

    # First, search by book ID
    if query in books_db:
        book = books_db[query]
        return jsonify(book), 200

    # Then, search by book title
    for book in books_db.values():
        if book['title'].lower() == query.lower():
            return jsonify(book), 200

    return jsonify({"message": "Book not found!"}), 404

@app.route('/get-books', methods=['GET'])
def get_books():
    return jsonify(list(books_db.values())), 200

if __name__ == '__main__':
    app.run(debug=True)
