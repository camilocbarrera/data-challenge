COPY_REPAYMENTS_STG = """
COPY INTO analytics.src_raw_s3.repayments FROM (

     SELECT
          $1::varchar  AS customerid
        , $2::varchar  AS loan_number
        , $3::varchar  AS interesttype
        , $4::varchar  AS loan_status
        , $5::varchar  AS company
        , $6::varchar  AS branch
        , $7::date     AS bookeddate
        , $8::date     AS interest_start_date
        , $9::date     AS cohort
        , $10::varchar AS chargeoff_date
        , $11::number  AS trancode
        , $12::varchar AS trantype
        , $13::varchar AS reject
        , $14::double  AS tranamount
        , $15::double  AS amounttoprincipal
        , $16::double  AS amounttointerest
        , $17::double  AS amounttofees
        , $18::double  AS precomputeamount
        , $19::double  AS cancelfeeamount
        , $20::date    AS tran_date
        , $21::number  AS tran_from_origination
        , $22::number  AS accounting_period
        , $23::double  AS amountfinanced
        , $24::double  AS amountchargedoff

     FROM @analytics.src_raw_s3.SFT_FILES_STG (FILE_FORMAT => analytics.src_raw_s3.csv_format , PATTERN => '^(repayments\.csv)$')

)

"""

COPY_LOAN_TAPE_STG = """
COPY INTO analytics.src_raw_s3.loan_tape FROM (
     SELECT
          $1::varchar  AS customer_id
        , $2::varchar  AS loan_id
        , $3::varchar  AS loan_number
        , $4::DATETIME AS customer_since
        , $5::DOUBLE   AS credit_score
        , $6::DOUBLE   AS debt_ratio
        , $7::DOUBLE   AS income
        , $8::VARCHAR  AS paygrade
        , $9::VARCHAR  AS ets_date
        , $10::VARCHAR AS anticipated_sep_date
        , $11::NUMBER  AS branch_code
        , $12::VARCHAR AS state
        , $13::varchar AS booked_date
        , $14::varchar AS interest_start_date
        , $15::varchar AS contract_date
        , $16::DOUBLE  AS balance
        , $17::DOUBLE  AS amount_financed
        , $18::DOUBLE  AS totalofpayments
        , $19::DOUBLE  AS cash_advance
        , $20::NUMBER  AS term
        , $21::DOUBLE  AS finance_charge
        , $22::DOUBLE  AS origination_fees
        , $23::DOUBLE  AS late_fees
        , $24::DOUBLE  AS maintenance_fees
        , $25::VARCHAR AS fl_stamp_tax
        , $26::DOUBLE  AS apr
        , $27::DOUBLE  AS interest_rate
        , $28::DOUBLE  AS life_insurance
        , $29::DOUBLE  AS disability_insurance
        , $30::DOUBLE  AS refinance_amount
        , $31::DOUBLE  AS mnthly_pymt_amnt
        , $32::VARCHAR AS orig_pmnt
        , $33::VARCHAR AS last_pymnt
        , $34::NUMBER  AS payments_received
        , $35::DOUBLE  AS amount_paid
        , $36::VARCHAR AS maturity_date
        , $37::VARCHAR AS chargeoff_date
        , $38::DOUBLE  AS chargeoff_amt
        , $39::VARCHAR AS close_date
        , $40::VARCHAR AS loan_status

     FROM @analytics.src_raw_s3.SFT_FILES_STG (FILE_FORMAT => analytics.src_raw_s3.csv_format , PATTERN => '^(loan_tape\.csv)$')
)
"""
