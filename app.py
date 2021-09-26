from flask import Flask
from flask import make_response, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/authorize')
def authorize():
    pass

    
if __name__ == '__main__':
    app.run(debug=True)