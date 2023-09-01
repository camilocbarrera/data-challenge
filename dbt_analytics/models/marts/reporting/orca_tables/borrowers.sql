WITH borrowers AS (SELECT customer_id    AS borrowerid
                        , customer_since AS customersince
                        , avg(income)    AS income
                        , state          AS state

--                    FROM analytics.dev_staging.stg_sftp__loan_tape
                   FROM {{ ref('stg_sftp__loan_tape') }}
                   WHERE TRUE
                   GROUP BY borrowerid, customersince, state)

SELECT row_number() OVER (ORDER BY customersince) AS id
     , borrowerid                                 AS borrowerid
     , customersince                              AS customersince
     , income                                     AS income
     , state                                      AS state
FROM borrowers