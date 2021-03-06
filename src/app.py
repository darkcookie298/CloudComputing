from flask import Flask, render_template, json, redirect, url_for, request
from pymongo import MongoClient
from time import gmtime, strftime
import os
import sys
from word_counter import Wordcounter

# init app and database
app = Flask(__name__)

client = MongoClient('mongodb://dbccproject:eb6cOAlo7yChycVEr9CXjBp143GAyOaYYEPblrsoEUCbmo26dBWPGc7sKzEjcc2H1Z7yN2PACcvYxh1aemHaaQ==@dbccproject.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')
db = client.filedb

# provide the websites
@app.route('/')
def index():

    _items = db.filedb.find()
    items = [item for item in _items]
    return render_template('index.html', items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/table')
def table():
    return render_template('table.html')

# for the db access
@app.route('/new', methods=['POST'])
def new():
    upload_file = request.files['file']
    output = str(upload_file.read())
    
    wc = Wordcounter()
    count = wc.count_words(output) #request.form['description']
    current_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    if len(count) > 0:
        if len(count) > 1:
            top = ""
            for w in count:
                top = top + "[" + str(w) + "] "
        else:
            top = count[0]
    else:
        top = "No Keywords"
    item_doc = {
        'id':0,
        'name': request.form['name'],
        'createdAt': str(current_time),
        'description': output,
        'keywords': top
    }

    db.filedb.insert_one(item_doc)

    return redirect(url_for('upload'))

@app.route('/upload')
def upload():
    _items = db.filedb.find()
    items = [item for item in _items]

    return render_template('upload.html', items=items)

# main method for easy use within the  commandline
if __name__ == "__main__":
    # enable debug mode only for developement
    app.run(host='0.0.0.0', debug=True)