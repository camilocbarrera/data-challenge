SELECT
     ROW_NUMBER( ) OVER (ORDER BY loan_id) AS id
   , stg_sftp__loan_tape.loan_id           AS loanid
   , tran_date                             AS paymentdate
   , tran_amount                           AS principalpaid
   , amount_to_interest                    AS interestpaid

FROM {{ ref('stg_sftp__repayments') }}
LEFT JOIN {{ ref('stg_sftp__loan_tape') }} USING ( loan_number, customer_id )
WHERE TRUE