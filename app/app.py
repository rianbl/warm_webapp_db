from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# PostgreSQL connection parameters
conn = psycopg2.connect(
    dbname='appdb',
    user='user',
    password='password',
    host='mypsql',  # Use the service name defined in the docker-compose.yml
    port='5432'
)
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
