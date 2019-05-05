from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<name>')
def name_dynamic(name):
    return f'this is {name[100]} page'


if __name__ == '__main__':
    app.run(debug=True)
