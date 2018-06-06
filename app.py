from flask import Flask, render_template, redirect, request
from models import init_db, Entry, BaseModel, EntryForm
from peewee import IntegrityError
import wtforms

app = Flask(__name__)

@app.route('/')
@app.route('/entries')
def index():
    # Just render the index template with all entries we have
    return render_template('index.html', entries=Entry.select())

@app.route('/entry', methods=['GET', 'POST'])
def new():
    # Create the form
    form = EntryForm(request.form)
    # If we're posting and the form is filled out correctly
    # Create the new entry
    # Otherwise return the empty form
    if request.method == 'POST' and form.validate():
        Entry.create(**form.data)
        return redirect('/')
    return render_template('new.html', form=form)

@app.route('/entries/<id>')
def detail(id):
    # Render the detail template with the selected entry
    return render_template('detail.html', entry=Entry.get(Entry.id == id))

@app.route('/entries/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    # Get selected entry and create the form
    entry = Entry.get(Entry.id == id)
    form = EntryForm(request.form, entry)
    # If we're posting and the form is filled out correctly
    # Update the entry
    # Otherwise render the empty form
    if request.method == 'POST' and form.validate():
        print(form.data)
        Entry.update(**form.data).where(Entry.id == id).execute()
        return redirect('/')
    return render_template('edit.html', entry=entry, form=form)

@app.route('/entries/delete/<id>')
def delete(id):
    # Delete the selected entry
    Entry.delete().where(Entry.id == id).execute()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)