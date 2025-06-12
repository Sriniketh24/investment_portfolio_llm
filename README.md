# Investment Portfolio SQL Query Generator

Demo project for generating SQL queries using the Gemini API based on an investment portfolio database.

## Components

- `investment_portfolio.sql` → database schema and data
- `investment_portfolio_documentation.json` → database documentation
- `portfolio_sql_training.jsonl` → few-shot training examples
- `sql_generator.py` → Python script to query Gemini and generate SQL

## How it works

- Loads schema + few-shot examples
- Sends user question to Gemini API
- Returns generated SQL

## Example Usage

User question: "Which stocks does Alice own?"

Generated SQL:
```sql
SELECT stock_symbol, quantity FROM Holdings JOIN Users ON Holdings.user_id = Users.id WHERE Users.name = 'Alice Johnson';
# investment_portfolio_llm
# investment_portfolio_llm
