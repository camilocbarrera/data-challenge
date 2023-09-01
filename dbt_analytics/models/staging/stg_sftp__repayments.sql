SELECT
     customerid            AS customer_id
   , loan_number           AS loan_number
   , interesttype          AS interesttype
   , loan_status           AS loan_status
   , company               AS company
   , branch                AS branch
   , bookeddate            AS booked_date
   , interest_start_date   AS interest_start_date
   , cohort                AS cohort
   , chargeoff_date        AS chargeoff_date
   , trancode              AS tran_code
   , trantype              AS tran_type
   , reject                AS is_reject
   , tranamount            AS tran_amount
   , amounttoprincipal     AS amount_to_principal
   , amounttointerest      AS amount_to_interest
   , amounttofees          AS amount_to_fees
   , precomputeamount      AS precompute_amount
   , cancelfeeamount       AS cancel_fee_amount
   , tran_date             AS tran_date
   , tran_from_origination AS tran_from_origination
   , accounting_period     AS accounting_period
   , amountfinanced        AS amount_financed
   , amountchargedoff      AS amount_chargedo_ff
-- FROM analytics.src_raw_s3.repayments
FROM {{  source('src_raw_s3','repayments') }}

