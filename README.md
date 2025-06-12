# Investment Portfolio SQL Query Generator

Demo project for generating SQL queries using the Gemini API based on an investment portfolio database.

## Components

- `investment_portfolio.sql` → database schema and data
- `investment_portfolio_documentation.json` → database documentation
- `portfolio_sql_training.jsonl` → few-shot training examples
- `sql_generator.py` → Python script to query Gemini and generate SQL + validate and execute safely

## How it works

- Loads schema + few-shot examples
- Sends user question to Gemini API
- Returns generated SQL
- **Validates generated SQL before executing**:
  - Runs `EXPLAIN` to check if the SQL is valid
  - Extracts column names used in the query
  - Compares them to actual columns in the database
  - Computes **column match accuracy %**
  - Only executes the query if accuracy ≥ 90%, otherwise skips the query for safety

## Example Usage

User question: "Which stocks does Alice own?"

Generated SQL:

```sql
SELECT stock_symbol, quantity FROM Holdings JOIN Users ON Holdings.user_id = Users.id WHERE Users.name = 'Alice Johnson';
