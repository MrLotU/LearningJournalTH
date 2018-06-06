from flask import Flask, render_template, redirect, request
from models import init_db, Entry, BaseModel, EntryForm
from peewee import IntegrityError
import wtforms

app = Flask(__name__)

@app.route('/')
@app.route('/entries')
def index():
    return render_template('index.html', entries=Entry.select())

@app.route('/entry', methods=['GET', 'POST'])
def new():
    form = EntryForm(request.form)
    if request.method == 'POST' and form.validate():
        Entry.create(**form.data)
        return redirect('/')
    return render_template('new.html', form=form)

@app.route('/entries/<id>')
def detail(id):
    return render_template('detail.html', entry=Entry.get(Entry.id == id))

@app.route('/entries/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    entry = Entry.get(Entry.id == id)
    form = EntryForm(request.form, entry)
    if request.method == 'POST' and form.validate():
        print(form.data)
        Entry.update(**form.data).where(Entry.id == id).execute()
        return redirect('/')
    return render_template('edit.html', entry=entry, form=form)

@app.route('/entries/delete/<id>')
def delete(id):
    Entry.delete().where(Entry.id == id).execute()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)