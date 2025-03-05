from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    important = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('index_lab_9.html')

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    notes_list = [{'id': note.id, 'text': note.text, 'important': note.important} for note in notes]
    return jsonify(notes_list)

@app.route('/add', methods=['POST'])
def add_note():
    data = request.get_json()
    text = data['text']
    important = data['important']
    note = Note(text=text, important=important)
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note added successfully!'}), 201

@app.route('/clear', methods=['POST'])
def clear_notes():
    db.session.query(Note).delete()
    db.session.commit()
    return jsonify({'message': 'All notes cleared!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

