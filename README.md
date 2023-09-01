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
![image](https://github.com/camilocbarrera/data-challenge/assets/85809276/b3cc92f7-d026-4a2a-856a-56565f1fea76)
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


## Data Engineering
In this scenario, we leveraged AWS Lambda Functions written in Python to execute a batch processing workflow. The process involved utilizing Docker to create a containerized environment, and the resulting image was uploaded to the AWS Elastic Container Registry (ECR) service. As a key component of the architecture, Fivetran was incorporated to streamline the data loading process, enhancing the efficiency of data ingestion.
Review the code of this function [here](custom_elt%2Flambda_functions%2Facme-investments). 

To illustrate the architecture, the AWS Lambda Function orchestrated the batch process, interacting with the Docker image stored in the AWS ECR. The Lambda Function executed Python code to perform the desired data transformations and operations. The containerized environment ensured consistency and isolation throughout the process.

Furthermore, Fivetran played a significant role in simplifying the data loading workflow. By utilizing Fivetran, the focus shifted from traditional ETL tasks to more intricate data modeling endeavors. Fivetran's data source agnosticism, automated data pipelines, real-time synchronization, data transformation capabilities, and robust monitoring and alerting features contributed to a seamless integration process.

By utilizing Fivetran, the complexities of data integration were mitigated, allowing for the optimization of time and resources. Data accuracy and timeliness were ensured, and the data engineers were able to establish efficient and reliable data pipelines. Additional insights about Fivetran's capabilities can be found at: [https://www.fivetran.com/data-movement/saas-replication](https://www.fivetran.com/data-movement/saas-replication)

![_etl_sftp_acme](https://github.com/camilocbarrera/data-challenge/assets/85809276/1f1f6ec3-9d1f-49ad-9ad9-f5adeff56a1d)


## Data Modeling with DBT

The process of data modeling will be accomplished using [DBT](https://www.getdbt.com/product/what-is-dbt/) (Data Build Tool), a versatile open-source command line tool designed to enhance the effectiveness of data transformation within a data warehouse. Originating at RJMetrics in 2016, DBT emerged as a solution to introduce fundamental transformation capabilities to the Stitch platform.

The proposed approach for modeling entails adopting a decoupled distribution strategy. This strategic choice fosters scalability in all dimensions, promoting loose coupling and strong cohesion among the various models. The envisioned methodology is illustrated below:
![Image](https://user-images.githubusercontent.com/85809276/231127215-d8db4c69-749e-4da0-a235-10c00068d203.png)

In each stage of this process, models are meticulously constructed along with their corresponding tests, snapshots, and metrics. Each layer is segregated, ensuring a structured and organized approach to modeling. For a deeper understanding, refer to the directory labeled "models/marts."

### DBT Architectural Structure

The architecture, as depicted in the initial image, is notably modular. This modularity facilitates component reusability, upholding a balance between low cohesion and high coupling. This design philosophy ensures flexibility and maintainability throughout the modeling process.

<img width="334" alt="image" src="https://github.com/camilocbarrera/data-challenge/assets/85809276/4032de65-318b-4b72-bb97-97d51f4f223e">

####

### DAG Lineage

The data progression, illustrated in the following stages, traverses from data sources through Staging, intermediate report, and culminates in Report layer. The semantic layer will supported by Power BI.

![_etl_sftp_lineage](https://github.com/camilocbarrera/data-challenge/assets/85809276/03446f7b-c06e-4288-887c-4bc79b695ae5)


### 2. Create the loan schedules.
Despite the complexity of this section due to its recursive nature, the development was carried out using SQL 🥷 through a recursive CTE (Common Table Expression) in Snowflake. This allows for the calculation of values without the need for a heuristic process. As demonstrated in the following query:

```snowflake
WITH RECURSIVE saleswithrownumbers AS (

     SELECT
          customer_id                                                                                       AS customer_id
        , loan_number                                                                                       AS loan_number
        , disbursement_amount                                                                               AS disbursement_amount
        , expectedprincipal                                                                                 AS expectedprincipal
        , installmentnumber                                                                                 AS number_of_installment
        , instalmentdate                                                                                    AS instalmentdate
        , term                                                                                              AS term
        , monthly_interest_rate                                                                             AS monthly_interest_rate
        , ROW_NUMBER( ) OVER (PARTITION BY customer_id,loan_number ORDER BY loan_number, installmentnumber) AS rn
     FROM analytics.dev_reporting.int_loan_schedule

)
   , recursivesubtraction          AS (

     SELECT
          customer_id
        , loan_number
        , disbursement_amount
        , expectedprincipal
        , monthly_interest_rate
        , number_of_installment
        , instalmentdate
        , rn
        , disbursement_amount - expectedprincipal AS new_disbursement_amount
     FROM saleswithrownumbers
     WHERE rn = 1

     UNION ALL

     SELECT
          s.customer_id
        , s.loan_number
        , s.disbursement_amount
        , s.expectedprincipal
        , s.monthly_interest_rate
        , s.number_of_installment
        , s.instalmentdate
        , s.rn
        , r.new_disbursement_amount - s.expectedprincipal
     FROM saleswithrownumbers        AS s
     INNER JOIN recursivesubtraction AS r
                     ON s.rn = r.rn + 1 AND s.customer_id = r.customer_id AND s.loan_number = r.loan_number
     WHERE s.rn <= s.term
)
   , oustanding                    AS (

     SELECT
          customer_id
        , loan_number
        , disbursement_amount
        , expectedprincipal
        , monthly_interest_rate
        , number_of_installment
        , instalmentdate
        , rn
        , new_disbursement_amount

     FROM recursivesubtraction


     UNION ALL

     SELECT

          customer_id                               AS customer_id
        , loan_number                               AS loan_number
        , NULL                                      AS disbursement_amount
        , NULL                                      AS expectedprincipal
        , NULL                                      AS monthly_interest_rate
        , 0                                         AS number_of_installment
        , NULL                                      AS instalmentdate
        , 0                                         AS rn
        , coalesce( amount_financed, 0 )
                  + coalesce( origination_fees, 0 ) AS new_disbursement_amount


     FROM analytics.dev_staging.stg_sftp__loan_tape

     WHERE TRUE
     ORDER BY customer_id, loan_number, rn
)

SELECT
     stg_sftp__loan_tape.loan_id          AS loan_id
   , oustanding.number_of_installment     AS number_of_installment
   , oustanding.instalmentdate            AS instalmentdate
   , lag( oustanding.new_disbursement_amount, 1 )
          OVER (PARTITION BY customer_id,loan_number ORDER BY number_of_installment)
             * monthly_interest_rate      AS expectedinterest
   , expectedprincipal - expectedinterest AS expectedprincipal
   , new_disbursement_amount              AS outstanding_principal

FROM oustanding
JOIN analytics.dev_staging.stg_sftp__loan_tape USING ( customer_id, loan_number )
WHERE TRUE
  AND loan_id = 140000000001441648
;
```
- Result: 

| LOAN\_ID | NUMBER\_OF\_INSTALLMENT | INSTALMENTDATE | EXPECTEDINTEREST | EXPECTEDPRINCIPAL | OUTSTANDING\_PRINCIPAL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 140000000001441648 | 0 | null | null | null | 1121.3899999999999 |
| 140000000001441648 | 1 | 2020-04-30 | 19.285104524999998 | 103.73186001444931 | 998.3730354605506 |
| 140000000001441648 | 2 | 2020-05-31 | 17.16952027733282 | 105.84744426211648 | 875.3560709211013 |
| 140000000001441648 | 3 | 2020-06-30 | 15.053936029665639 | 107.96302850978367 | 752.339106381652 |
| 140000000001441648 | 4 | 2020-07-31 | 12.93835178199846 | 110.07861275745084 | 629.3221418422027 |
| 140000000001441648 | 5 | 2020-08-31 | 10.82276753433128 | 112.19419700511803 | 506.30517730275335 |
| 140000000001441648 | 6 | 2020-09-30 | 8.707183286664101 | 114.3097812527852 | 383.28821276330405 |
| 140000000001441648 | 7 | 2020-10-31 | 6.591599038996922 | 116.42536550045239 | 260.27124822385474 |
| 140000000001441648 | 8 | 2020-11-30 | 4.476014791329742 | 118.54094974811956 | 137.25428368440544 |
| 140000000001441648 | 9 | 2020-12-31 | 2.3604305436625626 | 120.65653399578675 | 14.237319144956132 |

### 3. Transform and structure the data to our own format.


> Export the data into 4 datasets with ORCA’s structure that will be stored in our database.

The 4 datasets can be accessed, exported, and consumed from various applications through tables, as demonstrated below.

The logic behind the modeling was executed in SQL and constructed using DBT.

```snowflake
-- actualpayments
SELECT
     id
   , loanid
   , paymentdate
   , principalpaid
   , interestpaid
FROM analytics.dev_reporting.actualpayments;

-- borrowers
SELECT
     id
   , borrowerid
   , customersince
   , income
   , state
FROM analytics.dev_reporting.borrowers;

-- expectedpayments
SELECT
     id
   , loanid
   , installmentnumber
   , expectedprincipal
   , expectedinterest
FROM analytics.dev_reporting.expectedpayments;
-- loans
SELECT
     id
   , loanid
   , borrowerid
   , disbursementdate
   , disbursementamount
   , originationfee
   , apr
   , interestrate
   , term
   , score
FROM analytics.dev_reporting.loans;
```

### 4. Query our database to get insights.

 
> 1- Aggregated by Score buckets:
>
> a. Avg. Disbursement Amount.
>
>  b. Total NUMBER OF loans.
 >
> c. Total amount disbursed.
 >
> d. Number OF UNIQUE borrowers.
 >
> Buckets: 0 – 299, 300 – 600, 601 – 660, 661 – 720, 721 – 780, +781
```snowflake
WITH agregate_metrics_by_score AS (


     SELECT
          CASE
               WHEN credit_score BETWEEN 0 AND 299   THEN '[0 - 299]'
               WHEN credit_score BETWEEN 300 AND 600 THEN '[300 - 600]'
               WHEN credit_score BETWEEN 601 AND 660 THEN '[601 - 660]'
               WHEN credit_score BETWEEN 661 AND 720 THEN '[661 - 720]'
               WHEN credit_score BETWEEN 721 AND 780 THEN '[721 - 780]'
               WHEN credit_score >= 781              THEN '[781+)'
                                                     ELSE 'Unknown'
               END                                                                AS credit_score_bucket


        , CASE
               WHEN credit_score BETWEEN 0 AND 299   THEN 1
               WHEN credit_score BETWEEN 300 AND 600 THEN 2
               WHEN credit_score BETWEEN 601 AND 660 THEN 3
               WHEN credit_score BETWEEN 661 AND 720 THEN 4
               WHEN credit_score BETWEEN 721 AND 780 THEN 5
               WHEN credit_score >= 781              THEN 6
                                                     ELSE 7
               END                                                                AS credit_score_bucket_order

        , avg( coalesce( amount_financed, 0 ) + coalesce( origination_fees, 0 ) ) AS disbursement_amount
        , count( DISTINCT loan_id )                                               AS total_number_of_loans
        , avg( coalesce( amount_financed, 0 ) )                                   AS total_amount_disbursed
        , count( DISTINCT customer_id )                                           AS number_of_unique_borrowers

     FROM analytics.dev_staging.stg_sftp__loan_tape

     GROUP BY credit_score_bucket, credit_score_bucket_order
)
SELECT
     credit_score_bucket
   , disbursement_amount
   , total_number_of_loans
   , total_amount_disbursed
   , number_of_unique_borrowers
FROM agregate_metrics_by_score
ORDER BY credit_score_bucket_order
```
- result:

| CREDIT\_SCORE\_BUCKET | DISBURSEMENT\_AMOUNT | TOTAL\_NUMBER\_OF\_LOANS | TOTAL\_AMOUNT\_DISBURSED | NUMBER\_OF\_UNIQUE\_BORROWERS |
| :--- | :--- | :--- | :--- | :--- |
| \[0 - 299\] | 2766.7120720469143 | 3581 | 2682.65825746998 | 3093 |
| \[300 - 600\] | 3820.171742838523 | 105879 | 3678.0269877879473 | 50102 |
| \[601 - 660\] | 3980.669371348772 | 42965 | 3826.74460235075 | 29605 |
| \[661 - 720\] | 3967.442629145961 | 8653 | 3807.2156708655957 | 7272 |
| \[721 - 780\] | 4097.131086956521 | 1104 | 3924.250362318841 | 987 |
| \[781+\) | 5238.8603125 | 32 | 5021.655000000001 | 30 |
| Unknown | 3611.2672486033516 | 716 | 3495.5369832402234 | 707 |



> 2. Outstanding balance PER Loan

> a. Outstanding balance IS calculated AS Total Disbursed - Principal Payments.

```snowflake
WITH payments AS (

     SELECT
          stg_sftp__loan_tape.loan_id AS loan_id
        , SUM( tran_amount )          AS tran_amount
     FROM analytics.dev_staging.stg_sftp__repayments
     LEFT JOIN analytics.dev_staging.stg_sftp__loan_tape USING ( customer_id, loan_number )
     WHERE TRUE
     GROUP BY 1
)

SELECT
     loan_id                                                          AS loan_id
   , COALESCE( amount_financed, 0 ) + COALESCE( origination_fees, 0 ) AS disbursed
   , payments.tran_amount                                             AS tran_amount

FROM analytics.dev_staging.stg_sftp__loan_tape
JOIN payments USING ( loan_id )
WHERE TRUE
```

- LIMIT 10 RESULT

| LOAN\_ID | DISBURSED | TRAN\_AMOUNT |
| :--- | :--- | :--- |
| 140000000001379417 | 2229.45 | 2229.45 |
| 140000000001382892 | 1880.6999999999998 | 1041.07 |
| 140000000001383320 | 4592.9400000000005 | 2715.5200000000004 |
| 140000000001383361 | 1101.4099999999999 | 1101.4099999999999 |
| 140000000001384548 | 3373.56 | 440.91999999999996 |
| 140000000001381245 | 2427.6200000000003 | 1650 |
| 140000000001381932 | 1640.22 | 701.8 |
| 140000000001381983 | 2347.4100000000003 | 750 |
| 140000000001382520 | 5750.31 | 6250 |
| 140000000001382542 | 3752.73 | 0 |

## Roadmap Overview 🎯

To ensure effective project organization, I've devised a concise high-level roadmap encompassing the key epics and their associated tasks for this solution. The entire roadmap has been meticulously documented in Jira, utilizing the Scrum template as the foundation.

<img width="522" alt="image" src="https://github.com/camilocbarrera/data-challenge/assets/85809276/00877ab6-4f5f-41fa-a1b7-bfcebbd12a55">


![image](https://github.com/camilocbarrera/athena-challenge/assets/85809276/82465811-b41f-4f7a-b082-23bbbd8cdaba)



# Next steps

- [ ]  Set up Git Actions For Continuous Integration
- [ ]  Set up Airflow to orchestrate dbt dags and Airbyte jobs
- [ ]  Set up Elementary for Data Observability
- [ ]  Report and visualizations