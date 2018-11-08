import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host=os.environ['POSTGRES_HOST'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs where source='local';"""
    cur.execute(sql_all)
    all_local = cur.fetchone()[0]

    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE source='local' and status LIKE \'2__\';"""
    cur.execute(sql_success)
    success_local = cur.fetchone()[0]

    # Determine rate if there was at least one request
    rate_local = "No entries yet!"
    if all_local != 0:
        rate_local = str(success_local / all_local)

    sql_all = """SELECT COUNT(*) FROM weblogs where source='remote';"""
    cur.execute(sql_all)
    all_remote = cur.fetchone()[0]

    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE source='remote' and status LIKE \'2__\';"""
    cur.execute(sql_success)
    success_remote = cur.fetchone()[0]

    # Determine rate if there was at least one request
    rate_remote = "No entries yet!"
    if all_remote != 0:
        rate_remote = str(success_remote / all_remote)


    return render_template('index.html', rate = {'local': rate_local, 'remote': rate_remote})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
