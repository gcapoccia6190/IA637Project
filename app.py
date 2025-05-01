# --- app.py ---
from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from user import User
import yaml
from book import Book
from bookInteraction import BookInteraction
from bookConfirmation import BookConfirmation
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['FullName']
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']

        # Check if username already exists
        temp = User()
        temp.cur.execute("SELECT * FROM User WHERE Username = %s", (username,))
        if temp.cur.fetchone():
            return render_template('signup.html', msg="Username already taken.")

        # Hash password
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert as role 'user'
        temp.cur.execute("""
        INSERT INTO User (FullName, Username, PasswordHash, Email, Role)
        VALUES (%s, %s, %s, %s, 'reader')
        """, (full_name, username, hashed_pw, email))
        temp.conn.commit()

        return redirect('/login')

    return render_template('signup.html')






@app.route('/admin/review', methods=['GET', 'POST'])
def admin_add_review():
    if 'user_id' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        return render_template('ok_dialog.html', msg="Admins only.")

    book_obj = Book()
    interaction_obj = BookInteraction()

    if request.method == 'POST':
        book_id = request.form['BookID']
        content = request.form['Content']
        rating = request.form['Rating']
        user_id = session['user_id']

        now = datetime.now()
        date_str = now.date()
        time_str = now.time().strftime("%H:%M:%S")

        interaction_obj.insert([
            user_id, book_id, 'Comment', content or None,
            int(rating) if rating else None,
            None, date_str, time_str, 'Admin Panel'
        ])
        return redirect('/admin/review')

    books = book_obj.select_all()
    return render_template('admin_add_review.html', books=books)

@app.route('/confirmations', methods=['GET', 'POST'])
def confirm_book():
    if 'user_id' not in session:
        return redirect('/login')

    confirm_obj = BookConfirmation()
    book_obj = Book()

    # Insert confirmation if form is submitted
    if request.method == 'POST':
        book_id = request.form['BookID']
        user_id = session['user_id']
        notes = request.form['Notes']

        # Optional: prevent duplicate confirmation by the same user
        confirm_obj.cur.execute(
            "SELECT * FROM BookConfirmation WHERE BookID = %s AND UserID = %s",
            (book_id, user_id)
        )
        if confirm_obj.cur.fetchone():
            return render_template('confirm_book.html', msg="You've already confirmed this book!", books=book_obj.select_where("Status = 'inactive'"))

        confirm_obj.insert([book_id, user_id, None, notes])
        return redirect('/confirmations')

    books = book_obj.select_where("Status = 'inactive'")
    return render_template('confirm_book.html', books=books)



@app.route('/interactions', methods=['GET', 'POST'])
def view_interactions():
    if 'user_id' not in session:
        return redirect('/login')

    interaction_obj = BookInteraction()
    book_obj = Book()

    books = book_obj.select_all()
    interactions = []

    if request.method == 'POST':
        selected_book = request.form['BookID']
        query = """
            SELECT bi.*, b.Title, u.Username
            FROM BookInteraction bi
            JOIN Book b ON bi.BookID = b.BookID
            JOIN User u ON bi.UserID = u.UserID
            WHERE bi.BookID = %s
            ORDER BY bi.Date DESC, bi.Time DESC
        """
        interaction_obj.cur.execute(query, (selected_book,))
    else:
        query = """
            SELECT bi.*, b.Title, u.Username
            FROM BookInteraction bi
            JOIN Book b ON bi.BookID = b.BookID
            JOIN User u ON bi.UserID = u.UserID
            ORDER BY bi.Date DESC, bi.Time DESC
        """
        interaction_obj.cur.execute(query)

    interactions = interaction_obj.cur.fetchall()
    return render_template('view_interactions.html', interactions=interactions, books=books)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book_obj = Book()
    book_obj.cur.execute("SELECT * FROM Book WHERE BookID = %s", (book_id,))
    book = book_obj.cur.fetchone()

    if not book:
        return render_template('ok_dialog.html', msg="Book not found.")

    source = request.args.get('from', '')

    return render_template('book_detail.html', book=book, from_viewbooks=(source == 'viewbooks'))

@app.route('/user/review', methods=['GET', 'POST'])
def user_add_review():
    if 'user_id' not in session:
        return redirect('/login')
    if session['username'] == 'admin':
        return render_template('ok_dialog.html', msg="Admins should use the admin review page.")

    book_obj = Book()
    interaction_obj = BookInteraction()

    if request.method == 'POST':
        book_id = request.form['BookID']
        content = request.form['Content']
        rating = request.form['Rating']
        user_id = session['user_id']

        from datetime import datetime
        now = datetime.now()
        date_str = now.date()
        time_str = now.time().strftime("%H:%M:%S")

        interaction_obj.insert([
            user_id, book_id, 'Comment', content or None,
            int(rating) if rating else None,
            None, date_str, time_str, 'User Portal'
        ])
        return redirect('/user/review')

    books = book_obj.select_all()
    return render_template('user_add_review.html', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("USERNAME:", username, "PASSWORD:", password)  # debugging
        user = User.verify_login(username, password)
        print("USER FOUND:", user)  # debugging
        if user:
            session['user_id'] = user['UserID']
            session['username'] = user['Username']
            session['role'] = user['Role']  # ✅ FIXED: set role in session
            return redirect('/dashboard')
        return render_template('login.html', msg="Invalid credentials")
    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    user_obj = User()

    # Handle update submission
    if request.method == 'POST':
        full_name = request.form['FullName']
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']

        if password:  # If password entered, update hash
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            user_obj.cur.execute("""
                UPDATE User SET FullName = %s, Username = %s, Email = %s, PasswordHash = %s WHERE UserID = %s
            """, (full_name, username, email, hashed_pw, session['user_id']))
        else:
            user_obj.cur.execute("""
                UPDATE User SET FullName = %s, Username = %s, Email = %s WHERE UserID = %s
            """, (full_name, username, email, session['user_id']))

        user_obj.conn.commit()
        session['username'] = username  # ✅ Update session if username changed

    # Reload user info
    user_obj.cur.execute("SELECT * FROM User WHERE UserID = %s", (session['user_id'],))
    user = user_obj.cur.fetchone()

    # Get books the user interacted with
    interaction_obj = BookInteraction()
    interaction_obj.cur.execute("""
        SELECT DISTINCT b.Title
        FROM BookInteraction bi
        JOIN Book b ON bi.BookID = b.BookID
        WHERE bi.UserID = %s
        ORDER BY b.Title
    """, (session['user_id'],))
    books = interaction_obj.cur.fetchall()

    return render_template('profile.html', user=user, books=books)

@app.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book_admin(book_id):
    if 'user_id' not in session or session['username'] != 'admin':
        return render_template('ok_dialog.html', msg="Admins only.")

    book_obj = Book()

    if request.method == 'POST':
        title = request.form['Title']
        author = request.form['Author']
        isbn = request.form['ISBN']
        genre = request.form['Genre']
        edition = request.form['EditionNumber']
        year = request.form['PublishYear']
        status = request.form['Status']
        blurb = request.form['Blurb']

        book_obj.cur.execute("""
            UPDATE Book
            SET Title = %s, Author = %s, ISBN = %s, Genre = %s,
                EditionNumber = %s, PublishYear = %s, Status = %s, Blurb = %s
            WHERE BookID = %s
        """, (title, author, isbn, genre, edition, year, status, blurb, book_id))
        book_obj.conn.commit()
        return redirect('/admin')

    # GET request – load existing book info
    book_obj.cur.execute("SELECT * FROM Book WHERE BookID = %s", (book_id,))
    book = book_obj.cur.fetchone()

    if not book:
        return render_template('ok_dialog.html', msg="Book not found.")

    return render_template('admin_edit_book.html', book=book)





@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    book_obj = Book()
    trending_query = """
        SELECT b.*, COUNT(i.InteractionID) AS InteractionCount
        FROM Book b
        LEFT JOIN BookInteraction i ON b.BookID = i.BookID
        GROUP BY b.BookID
        ORDER BY InteractionCount DESC
        LIMIT 5
    """
    book_obj.cur.execute(trending_query)
    trending_books = book_obj.cur.fetchall()

    return render_template(
        'dashboard.html',
        username=session['username'],
        role=session['role'],
        trending_books=trending_books
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session:
        return redirect('/login')

    book_obj = Book()

    if request.method == 'POST':
        title = request.form['Title']
        author = request.form['Author']
        isbn = request.form['ISBN']
        genre = request.form['Genre']
        edition = request.form['EditionNumber']
        year = request.form['PublishYear']

        # Check for duplicate book (title + author or ISBN match)
        book_obj.cur.execute(
            "SELECT * FROM Book WHERE (Title = %s AND Author = %s) OR ISBN = %s",
            (title, author, isbn)
        )
        existing = book_obj.cur.fetchone()
        if existing:
            return render_template('add_book.html', msg="Book already exists!")

        # Set status: inactive for regular users, active for admin
        user_role = session.get('username')
        status = 'active' if user_role == 'admin' else 'inactive'

        # Insert the book
        book_obj.insert([title, author, isbn, genre, status, edition, year])
        return redirect('/books')

    return render_template('add_book.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    if session['username'] != 'admin':
        return render_template('ok_dialog.html', msg="Admins only.")

    book_obj = Book()
    confirm_obj = BookConfirmation()

    if request.method == 'POST':
        book_id = request.form['BookID']
        action = request.form['Action']

        new_status = 'active' if action == 'activate' else 'inactive'
        book_obj.cur.execute("UPDATE Book SET Status = %s WHERE BookID = %s", (new_status, book_id))
        book_obj.conn.commit()
        return redirect('/admin')


    confirm_obj.cur.execute("""
    SELECT b.BookID, b.Title, b.Author, b.Status, COUNT(c.ConfirmationID) AS ConfirmCount
    FROM Book b
    LEFT JOIN BookConfirmation c ON b.BookID = c.BookID
    GROUP BY b.BookID, b.Title, b.Author, b.Status
""")

    books = confirm_obj.cur.fetchall()

    return render_template('admin_dashboard.html', books=books)

from book import Book

@app.route('/books')
def view_books():
    if 'user_id' not in session:
        return redirect('/login')

    book_obj = Book()
    books = book_obj.select_all()
    return render_template('view_books.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)