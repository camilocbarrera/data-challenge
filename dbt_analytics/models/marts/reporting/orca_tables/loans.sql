WITH loans AS (

     SELECT DISTINCT
          ROW_NUMBER( ) OVER (ORDER BY loan_id)                            AS id
        , loan_id                                                          AS loanid
        , customer_id                                                      AS borrowerid
        , contract_date                                                    AS disbursementdate
        , coalesce( amount_financed, 0 ) + coalesce( origination_fees, 0 ) AS disbursementamount
        , origination_fees                                                 AS originationfee
        , apr                                                              AS apr
        , interest_rate                                                    AS interestrate
        , term                                                             AS term
        , credit_score                                                     AS score

--      FROM analytics.dev_staging.stg_sftp__loan_tape
     FROM {{ ref('stg_sftp__loan_tape') }}
     WHERE TRUE
)
SELECT *
FROM loans