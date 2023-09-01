# Data Engineering Challenge 👨🏻‍💻



# Bussines Context
> We received the data from a company called “ACME Investments” and we have to process it into ORCA.
> The following steps are required to complete this exercise:

# Assignment
The following steps are required to complete this exercise:
1. Create a process to read, validate, and clean the data.
2. Create the loan schedules.
3. Transform and structure the data to our own format.
4. Query our database to get insights.

# Solution
## Architecture

To address this scenario, my approach aims to leverage industry-leading architectural best practices for the entire data extraction, loading, and transformation workflow, all while utilizing a Modern Data Stack.

A streamlined architecture is suggested, comprising Snowflake, AWS Lambda (Python), Fivetran, and PowerBI.

Why opt for Snowflake? From my experience, it stands out as the most efficient, easy-to-implement solution that enables us to direct our focus on the crucial aspect—data analysis.
> Snowflake serves as a Software-as-a-Service (SaaS) analytics data warehouse. Unlike traditional data warehouses that depend on existing databases or "big data" platforms such as Hadoop, Snowflake operates on a unique, cloud-native SQL database engine.

For additional details, visit: https://www.snowflake.com/workloads/data-warehouse-modernization/

## Project Structure
The project structure is as follows:

- [airflow](airflow) In this folder, you will find the Dags and Tasks that orchestrate the components of the proposed architecture.

- [custom_elt](custom_elt) This folder contains custom code for data extraction. In the current use case, you will be able to find the extraction and loading process from SFTP to AWS S3.

- [dbt_analytics](dbt_analytics) The transformation part was carried out using DBT, one of the most widely-used frameworks for data transformation.