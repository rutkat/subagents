# requirements 
# haystack-ai pandas sqlite3 typing re

import re
import sqlite3
import pandas as pd
from typing import List

from haystack import component
from haystack.dataclasses import ChatMessage

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("dermatology_patient_data.csv", encoding="utf-8-sig", delimiter=";")

# Create a connection to a new SQLite database named "patient_data.db"
db_connection = sqlite3.connect("patient_data.db")

# Write the contents of the DataFrame to a new table named "patients"
df.to_sql("patients", db_connection, if_exists="replace", index=False)

# Close the database connection
db_connection.close()


@component
class SQLConnector:
    def __init__(self, sql_database: str):
        self.connection = sqlite3.connect(sql_database, check_same_thread=False)

    @component.output_types(results=List[str])
    def run(self, llm_replies: List[ChatMessage]):
        results = []
        pattern = r"```sql\s*([\s\S]+?)```"

        for message in llm_replies:
            extracted = re.findall(pattern, message.text)
            if not extracted:
                results.append("No SQL code found.")
                continue

            sql_to_run = " ".join(extracted[0].splitlines()).strip()
            try:
                result = pd.read_sql(sql_to_run, self.connection) 
                results.append(str(result))

            except Exception as e:
                results.append(f"Error: {e}")

        return {"results": results}

from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator

query_to_sql_prompt = """
You are an expert SQL assistant. Given the following table structure:

Table name: patients

Columns:
- patient_id (TEXT)
- age (INTEGER)
- gender (TEXT)
- condition (TEXT)  // Dermatological diagnosis (e.g., Psoriasis, Acne)
- medication (TEXT)  // Treatment corresponding to the condition
- skin_type (TEXT)  // Sensitive, Normal, Dry, Combination, Oily
- last_visit_date (DATE)
- smoker (TEXT)  // Yes or No
- alcohol_use (TEXT)  // None, Light, Moderate, Heavy
- BMI (FLOAT)  // Body Mass Index (e.g., 23.1)
- occupation (TEXT)  // Profession or employment status
- allergies (TEXT)  // Known non-sensitive allergies (e.g., Pollen, Latex, None)
- comorbid_condition (TEXT)  // Other health conditions (e.g., Asthma, Hypertension, None)

Write an SQL query to for this user query: {{query}}.

Only return the SQL query, nothing else.
"""

sql_pipeline = Pipeline()
sql_pipeline.add_component("prompt_builder", ChatPromptBuilder(template=[ChatMessage.from_user(query_to_sql_prompt)], required_variables="*"))
sql_pipeline.add_component("chat_generator", OpenAIChatGenerator(model="gpt-4o-mini"))
sql_pipeline.add_component("sql_connector", SQLConnector('patient_data.db'))

sql_pipeline.connect("prompt_builder", "chat_generator")
sql_pipeline.connect("chat_generator.replies", "sql_connector.llm_replies")

pipeline_result = sql_pipeline.run({"query":"What's the most common diagnosis of patients older than 60?"}, include_outputs_from={"chat_generator"})

print(pipeline_result["sql_connector"]["results"][0])
#    0  Lichen Simplex Chronicus   5
print(pipeline_result["chat_generator"]["replies"][0].text)
```sql
SELECT condition, COUNT(*) AS diagnosis_count
FROM patients
WHERE age > 60
GROUP BY condition
ORDER BY diagnosis_count DESC
LIMIT 1;
```
