from flask import Flask
import requests
import os
import psycopg2

app = Flask(__name__)

@app.route('/')
def read_file():
    reader_url = os.getenv('FILE_READER_URL')

    print(f'getting content from f{reader_url}')
    text = requests.get(reader_url).text

    save_to_pg(text)
    return text

def save_to_pg(text):
    con = psycopg2.connect(os.getenv('POSTGRES_URI'))

    cur = con.cursor()
    cur.execute('INSERT INTO file_content(content) VALUES (%s)', (text,))
    
    con.commit()
    

if __name__ == '__main__':
    app.run('0.0.0.0')