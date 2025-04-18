from flask import Flask
from flask import render_template
from flask import request, make_response

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/login")
def cookie_test():
    return render_template('login.html')

@app.route("/recipes")
def recipes():
    print('yeah here will be recipes but now they r dont exsict')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')