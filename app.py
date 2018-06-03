from flask import Flask, render_template, redirect, request
from models import init_db, Entry, BaseModel, EntryForm
from peewee import IntegrityError
import wtforms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', entries=Entry.select())

@app.route('/new', methods=['GET', 'POST'])
def new():
    form = EntryForm(request.form)
    if request.method == 'POST' and form.validate():
        Entry.create(**form.data)
        return redirect('/')
    return render_template('new.html', form=form)

@app.route('/detail/<id>')
def detail(id):
    return render_template('detail.html', entry=Entry.get(Entry.id == id))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    entry = Entry.get(Entry.id == id)
    form = EntryForm(request.form, entry)
    if request.method == 'POTS' and form.validate():
        Entry.update(**form.data).where(Entry.id == id)
        return redirect('/')
    return render_template('edit.html', entry=entry, form=form)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)