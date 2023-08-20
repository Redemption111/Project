import pymongo
from flask import Flask, render_template, request, redirect
from datetime import datetime
from bson.objectid import ObjectId
import random

app= Flask("jumbled_words")

client = pymongo.MongoClient("mongodb+srv://Redemption:87654321@cluster0.niiqppo.mongodb.net/?retryWrites=true&w=majority")
db = client.words

holder=[]


@app.route('/', methods=['GET','POST'])
def index():
    global holder
    if request.method == 'GET':
        return render_template('index.html')
    else:
        document={}
        document['word']=request.form['word']
        db.word.insert_one(document)
        # flash("Successful")
        return redirect("/")



@app.route('/play', methods=['GET','POST'])
def play():
    global holder
    if request.method == 'GET':
        entries = [i for i in db.word.find()]

        holder = random.sample(entries,k=5)
        
        for i in range(0,len(holder)):
            temp = list(holder[i]['word'])
            random.shuffle(temp)
            holder[i]['scrambled'] = ''.join(temp)
        
        return render_template('play.html', words=holder)
    else:
        print(holder)
        print(request.form)
        for i in range(0,len(holder)):
            holder[i]['user_answer'] = request.form[str(holder[i]['_id'])]
        
        return redirect("/result")



@app.route('/result',methods=['GET'])
def result():
    global holder
    print(holder)
    counter = 0
    for i in holder:
        if i['user_answer'] == i['word']:
            counter+=1

    return render_template('result.html',words=holder,counter=counter)

app.run(debug=True)