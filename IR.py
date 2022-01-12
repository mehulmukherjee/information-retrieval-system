from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
import os
from IR_Final import *
from werkzeug import secure_filename


app=Flask(__name__)


@app.route('/')
def e():
	
	return render_template("IR_Main.html")


@app.route('/Positional_Index',methods=['POST','GET'])
def a():

	displayTermPosition()
	if request.method == 'POST':
		try:
			x=str(request.form['query1'])
			y=str(request.form['query2'])
			z=int(str(request.form['query3']))
			if x is not None:
				
				query(x,y,z)				
				return redirect(url_for('b'))
		except Exception as e :
			print e
			return render_template("Positional_Index.html")
	return render_template("Positional_Index.html")

@app.route('/Inverted_Index',methods=['POST','GET'])
def d():
	
	displayInvIndex()
	if request.method == 'POST':
		try:
			x=str(request.form['query'])			
			if x is not None:
				
				queryInvIndex(x)
				return redirect(url_for('b'))
		except Exception as e :
			print e
			return render_template("Inverted_Index.html")
	return render_template("Inverted_Index.html")

@app.route('/Answer')
def b():
	return render_template("Answer.html")

@app.route('/Answer1')
def c():
	return render_template("Answer1.html")	


@app.route('/Add_Document',methods=['POST','GET'])
def index7():
	if request.method == 'POST':
		f=request.files['file']
		f.save(secure_filename(f.filename))
		return render_template("IR_Main.html")
	return render_template("Add_Document.html")


if __name__ == "__main__":
	app.config['AUTO_RELOAD'] = True
	app.run(debug=True)