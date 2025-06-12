import os
import google.generativeai as genai
import mysql.connector
import json
import re

genai.configure(api_key= "YOUR_GEMINI_API_KEY")
with open("investment_portfolio_documentation.json", "r") as f:
    schema_text = f.read()

with open("portfolio_sql_training.jsonl", "r") as f:
    examples = [json.loads(line) for line in f]

prompt = "You are a SQL query generator for the investment_portfolio database.\n"
prompt += f"Database schema:\n{schema_text}\n\n"

for ex in examples:
    user_message = None
    assistant_message = None
    for m in ex["messages"]:
        if m["role"] == "user":
            user_message = m["content"]
        elif m["role"] == "assistant":
            assistant_message = m["content"]
    if user_message and assistant_message:
        prompt += f"User question: {user_message}\n"
        prompt += f"SQL: {assistant_message}\n\n"

user_question = "Which stocks does Alice own?"
prompt += f"User question: {user_question}\nSQL:"

model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
response = model.generate_content(prompt)

generated_sql = response.text.strip()

print("User question:", user_question)
print("\nGenerated SQL:\n", generated_sql)

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_ROOT_PASSWORD",
        database="investment_portfolio"
    )
    cursor = conn.cursor()

    try:
        explain_sql = f"EXPLAIN {generated_sql}"
        cursor.execute(explain_sql)
        explain_result = cursor.fetchall()
        print("\nEXPLAIN successful → SQL is valid.\n")

        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'investment_portfolio'
        """)
        valid_columns = set([row[0].lower() for row in cursor.fetchall()])

        columns_in_sql = set(re.findall(r'(?<=SELECT )(.*?)(?= FROM)', generated_sql, re.IGNORECASE))
        if columns_in_sql:
            columns_string = list(columns_in_sql)[0]
            extracted_columns = set()
            for col in columns_string.split(","):
                col_name = col.strip().split(" AS ")[0].split(".")[-1].strip().lower()
                extracted_columns.add(col_name)
        else:
            extracted_columns = set()

        print("Columns used in SQL:", extracted_columns)
        print("Valid columns in DB:", valid_columns)

        if len(extracted_columns) == 0:
            accuracy = 0
        else:
            match_count = sum([1 for col in extracted_columns if col in valid_columns])
            accuracy = (match_count / len(extracted_columns)) * 100

        print(f"\nColumn match accuracy: {accuracy:.2f}%")

        threshold = 75
        if accuracy >= threshold:
            print("\nAccuracy is sufficient → Executing SQL on MySQL...")
            cursor.execute(generated_sql)
            rows = cursor.fetchall()

            print("\nQuery Result:")
            for row in rows:
                print(row)
        else:
            print("\nAccuracy below threshold → SQL execution skipped for safety.")

    except mysql.connector.Error as err:
        print("\nEXPLAIN failed → Invalid SQL → Execution skipped.")
        print("Error:", err)

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print("\nError connecting to MySQL:", err)
