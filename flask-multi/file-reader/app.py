from flask import Flask

app = Flask(__name__)


@app.route('/')
def read_file():
    with open('/vol/content.txt') as f:
        return '\n'.join(f.readlines())

if __name__ == '__main__':
    app.run('0.0.0.0')