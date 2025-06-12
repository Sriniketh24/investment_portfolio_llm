
import google.generativeai as genai
import mysql.connector
import json

genai.configure(api_key="AIzaSyAjF_vFrlLOtIdjIf89b2jgjFcGUbJBKvI")

with open("investment_portfolio_documentation.json", "r") as f:
    schema = json.load(f)

with open("portfolio_sql_training.jsonl", "r") as f:
    examples = [json.loads(line) for line in f]

prompt = "You are a SQL query generator for the investment_portfolio database.\n"
prompt += f"Database schema:\n{schema}\n\n"

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
        password="Saikrish123$",
        database="investment_portfolio"
    )
    cursor = conn.cursor()

    print("\nExecuting SQL on MySQL...")
    cursor.execute(generated_sql)
    rows = cursor.fetchall()

    print("\nQuery Result:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print("\nError executing SQL:", err)
