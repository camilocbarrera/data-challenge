SELECT split_part(customer_id, ':', 2)::INTEGER AS customer_id
   , trim(split_part( loan_id, ':', 2 ))              AS loan_id
   , trim(split_part( loan_number, ':', 2 ))          AS loan_number
   ,  customer_since::date                      AS customer_since
   , credit_score                               AS credit_score
   , debt_ratio                                 AS debt_ratio
   , income                                     AS income
   , paygrade                                   AS paygrade
   , TRY_TO_DATE( ets_date )                    AS ets_date
   , TRY_TO_DATE( anticipated_sep_date )        AS anticipated_sep_date
   , branch_code                                AS branch_code
   , state                                      AS state
   , try_to_date( booked_date )                 AS booked_date
   , try_to_date( interest_start_date )         AS interest_start_date
   , try_to_date( contract_date )               AS contract_date
   , balance                                    AS balance
   , amount_financed                            AS amount_financed
   , totalofpayments                            AS totalofpayments
   , cash_advance                               AS cash_advance
   , term                                       AS term
   , finance_charge                             AS finance_charge
   , origination_fees                           AS origination_fees
   , late_fees                                  AS late_fees
   , maintenance_fees                           AS maintenance_fees
   , fl_stamp_tax                               AS fl_stamp_tax
   , apr                                        AS apr
   , interest_rate                              AS interest_rate
   , life_insurance                             AS life_insurance
   , disability_insurance                       AS disability_insurance
   , refinance_amount                           AS refinance_amount
   , mnthly_pymt_amnt                           AS mnthly_pymt_amnt
   , orig_pmnt                                  AS orig_pmnt
   , last_pymnt                                 AS last_pymnt
   , payments_received                          AS payments_received
   , amount_paid                                AS amount_paid
   , TRY_TO_DATE( maturity_date )               AS maturity_date
   , chargeoff_date                             AS chargeoff_date
   , chargeoff_amt                              AS chargeoff_amt
   , TRY_TO_DATE( close_date )                  AS close_date
   , loan_status                                AS loan_status

--FROM analytics.src_raw_s3.loan_tape
FROM {{ source('src_raw_s3','loan_tape') }}
