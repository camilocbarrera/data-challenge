SELECT
     ROW_NUMBER( ) OVER (ORDER BY loan_id)                                                                                   AS id
   , stg_sftp__loan_tape.loan_id                                                                                             AS loanid
   , row_number( ) OVER (PARTITION BY stg_sftp__repayments.loan_number, stg_sftp__repayments.customer_id ORDER BY tran_date) AS installmentnumber
   , stg_sftp__repayments.amount_to_principal                                                                                AS expectedprincipal
   , stg_sftp__repayments.amount_to_interest                                                                                 AS expectedinterest
FROM {{ ref('stg_sftp__repayments') }}
LEFT JOIN {{ ref('stg_sftp__loan_tape') }} USING ( loan_number, customer_id )
WHERE TRUE