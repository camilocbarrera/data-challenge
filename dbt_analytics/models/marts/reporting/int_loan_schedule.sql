
     WITH payments      AS (


          SELECT
               loan_number                                                                  AS loan_number
             , customer_id                                                                  AS customer_id
             , ROW_NUMBER( ) OVER (PARTITION BY loan_number,customer_id ORDER BY tran_date) AS installmentnumber
             , LAST_DAY( dateadd( 'month', installmentnumber - 1, cohort ) )                AS instalmentdate

--           FROM dev_staging.stg_sftp__repayments
          FROM {{ ref('stg_sftp__repayments') }}
          WHERE TRUE
     )
        , loans         AS (


          SELECT
               customer_id
             , loan_id
             , term
             , loan_number
             , amount_financed
             , origination_fees
             , contract_date
             , interest_rate
             , ( interest_rate / 100 ) / 12 AS monthly_interest_rate

--           FROM analytics.dev_staging.stg_sftp__loan_tape
          FROM {{ ref('stg_sftp__loan_tape') }}


          WHERE TRUE
     )
        , loan_schedule AS (

          SELECT

               loans.customer_id                                          AS customer_id
             , loans.loan_id                                              AS loan_id
             , loans.term                                                 AS term
             , loans.loan_number                                          AS loan_number
             , loans.amount_financed                                      AS amount_financed
             , loans.origination_fees                                     AS origination_fees
             , loans.contract_date                                        AS contract_date
             , loans.interest_rate                                        AS interest_rate
             , loans.monthly_interest_rate                                AS monthly_interest_rate

             , payments.installmentnumber                                 AS installmentnumber
             , payments.instalmentdate                                    AS instalmentdate
             , coalesce( loans.amount_financed, 0 )
                       + coalesce( loans.origination_fees, 0 )            AS disbursement_amount


             , ( disbursement_amount * monthly_interest_rate ) * power( 1 + monthly_interest_rate, term )
                       / ( POWER( 1 + monthly_interest_rate, term ) - 1 ) AS expectedprincipal

             , disbursement_amount                                        AS x

          FROM loans
          LEFT JOIN payments USING ( loan_number, customer_id )
     )
     SELECT
          loan_schedule.customer_id
        , loan_schedule.loan_id
        , loan_schedule.term
        , loan_schedule.amount_financed
        , loan_schedule.origination_fees
        , loan_schedule.contract_date
        , loan_schedule.interest_rate
        , loan_schedule.monthly_interest_rate
        , loan_schedule.loan_number
        , loan_schedule.installmentnumber
        , loan_schedule.instalmentdate
        , loan_schedule.disbursement_amount
        , loan_schedule.expectedprincipal
        , loan_schedule.x

     FROM loan_schedule
