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
     FROM {{ ref('int_loan_schedule') }}

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


     FROM {{ ref('stg_sftp__loan_tape') }}

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
JOIN {{ ref('stg_sftp__loan_tape') }} USING ( customer_id, loan_number )
WHERE TRUE
--   AND loan_id = 140000000001441648