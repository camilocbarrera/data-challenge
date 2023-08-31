# Data Engineering Challenge 👨🏻‍💻




# Project Structure
The project structure is as follows:

- [airflow](airflow) Airflow is our orchestrator. Here you will find all our dags, this is managed by Astronomer.


- [custom_elt](custom_elt) custom_elt By default, we use EL tools like Fivetran for data extraction. However, when data
  cannot be extracted using these tools, we must develop custom processes (mostly in Python) to execute this process.


- [dbt_analytics](dbt_analytics) dbt_analytics Here, we treat analytics as code. All transformation processes are
  carried out using DBT, the most widely used framework for performing Analytics Engineering.
