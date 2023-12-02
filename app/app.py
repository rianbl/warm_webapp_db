from flask import Flask, render_template, request
import psycopg2
from psycopg2 import OperationalError
import time

app = Flask(__name__)

# Initialize conn as a global variable
conn = None

def wait_for_postgres():
    global conn  # Reference the global variable

    max_retries = 30  # Adjust the number of retries as needed
    retry_interval = 2  # Adjust the interval between retries as needed

    for attempt in range(max_retries):
        try:
            # Attempt to establish a connection to PostgreSQL
            conn = psycopg2.connect(
                dbname='appdb',
                user='user',
                password='password',
                host='mypsql',
                port='5432'
            )
            print("Connected to PostgreSQL successfully!")
            return True
        except OperationalError as e:
            print(f"Attempt {attempt + 1}: PostgreSQL not ready - {e}")
            time.sleep(retry_interval)

    print(f"Could not connect to PostgreSQL after {max_retries} attempts. Exiting.")
    return False

# Wait for PostgreSQL to be ready before proceeding
if not wait_for_postgres():
    exit(1)

# Continue with the rest of the script
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    # Get the name from the form submission
    column_name = request.form['column_name']

    # Perform the INSERT operation
    insert_query = f"INSERT INTO apptable (name) VALUES ('{column_name}') RETURNING *;"
    cursor.execute(insert_query)
    conn.commit()

    # Display the SQL query for the INSERT operation
    result_query = f"SELECT * FROM apptable WHERE name = '{column_name}';"
    
    return render_template('result.html', result=result_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
