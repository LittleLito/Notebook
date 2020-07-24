import os
import click
from flask import Flask, flash, redirect, url_for, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from forms import NewNoteForm, EditNoteForm, DeleteNoteForm, DoneNoteForm

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' +
                                                  os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.secret_key = 'secret string'


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Note {self.body} {self.done}>'


@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database, Done.')


@app.route('/')
def index():
    form1 = DoneNoteForm()
    form2 = DeleteNoteForm()
    notes = Note.query.all()
    return render_template('index.html', notes=notes, form1=form1, form2=form2)


@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved')
        return redirect(url_for('index'))
    return render_template('edit_note.html', form=form, title='New note')


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('Your note is updated')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html', form=form, title='Edit note')


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted')
    else:
        abort(400)
    return redirect(url_for('index'))


@app.route('/done/<int:note_id>', methods=['POST'])
def done_note(note_id):
    note = Note.query.get(note_id)
    form = DoneNoteForm()
    if form.validate_on_submit():
        note.done = not note.done
        db.session.commit()
        flash('This task is done, Good job')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
