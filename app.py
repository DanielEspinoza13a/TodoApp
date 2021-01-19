from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


app.config['MONGO_URI'] = "<insert mongo cluster link>"
mongo = PyMongo(app)

#Nombre de la coleccion
todos = mongo.db.todos

#Ruta index
@app.route('/')
def index():
    saved_todos = todos.find()
    return render_template('index.html', todos=saved_todos)

#Insertar objeto
@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

#Marcar que se ha completado una tarea
@app.route('/complete/<oid>')
def complete(oid):
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    todos.save(todo_item)
    return redirect(url_for('index'))

#Borrar un objeto completado
@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('index'))

#Borrar todos los objetos de la lista
@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))