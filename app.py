from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = 'clothes.db'

def create_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS clothes
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, filename TEXT)''')

create_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form.get('category')
        new_category = request.form.get('new_category')
        if not category and new_category:
            category = new_category
        file = request.files['file']
        if file and file.filename:  # Check if a file is uploaded
            original_filename = secure_filename(file.filename)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{original_filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            with sqlite3.connect(app.config['DATABASE']) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO clothes (category, filename) VALUES (?, ?)", (category, filename))
                conn.commit()

    categories = []
    clothes = []
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT category FROM clothes")
        categories = [category[0] for category in c.fetchall()]  # Flatten the list of tuples
        c.execute("SELECT * FROM clothes")
        clothes = c.fetchall()

    return render_template('index.html', categories=categories, clothes=clothes)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete', methods=['POST'])
def delete():
    filename = request.form.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        with sqlite3.connect(app.config['DATABASE']) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM clothes WHERE filename=?", (filename,))
            conn.commit()
    return '', 204

@app.route('/clear_database', methods=['POST'])
def clear_database():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM clothes")
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
