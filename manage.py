from flask import Flask, render_template, url_for

#create a Flask Instance
app = Flask(__name__)

#Create a route directory
@app.route('/')
def home():
    title = "Router Man"
    return render_template('index.html', title=title)

@app.route('/login')
def login():
    return render_template('login.html')



if __name__== '__main__':
    app.run(debug=True)