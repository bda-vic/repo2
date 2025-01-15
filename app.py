
# %pip install psycopg2-binary
from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import psycopg2

app = Flask(__name__)

# Define connection parameters
host = 'dpg-cu02528gph6c73chsek0-a.oregon-postgres.render.com'
port = '5432'
dbname = 'bda_issv'
user = 'bda_issv_user'
password = 'ykINLweIiqpb9dyToKSiF902aX0UcAYn'
    
def get_db_connection():
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/data")
def get_data():
    return jsonify({"message": "Hello, Flask!"})

@app.route("/insights")
def insights():
    # Connect to the PostgreSQL database
    conn = get_db_connection()
    
    # Query the data from the PostgreSQL table
    query = 'SELECT "SALES_AMOUNT" FROM AdventureWorks LIMIT 1000'
    data = pd.read_sql_query(query, conn)
    
    # Close the database connection
    conn.close()

    # Check if the column exists in the data
    # if 'age' not in data.columns:
    #     return "Column 'age' does not exist in the table", 400

    # Generate insights
    # Example: Distribution of 'age'
    plt.figure(figsize=(10, 6))
    data.plot()
    # sns.countplot(data['age'])
    # plt.title('Distribution of Age')
    # plt.xlabel('Age')
    # plt.ylabel('Count')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("insights.html", plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
