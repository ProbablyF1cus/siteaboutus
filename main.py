from flask import Flask
from flask import render_template
from flask import request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/login")
def cookie_test():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
