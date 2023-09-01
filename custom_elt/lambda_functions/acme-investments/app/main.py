from app.elt import Extraction
from app.queries import COPY_REPAYMENTS_STG, COPY_LOAN_TAPE_STG


def lambda_handler(event, context=None):
    copy_event = event.get('copy_to_table')

    elt = Extraction(

        event.get('file_name'),
        event.get('remote_path')
    )

    response_extract = elt.extract_and_load()

    if copy_event == "COPY_REPAYMENTS_STG":
        print(copy_event,"repaymente")
        response_copy = elt.copy_data_snowflake(COPY_REPAYMENTS_STG)
    if copy_event == "COPY_LOAN_TAPE_STG":
        print(copy_event,"loan_tape")
        response_copy = elt.copy_data_snowflake(COPY_LOAN_TAPE_STG)

    log = {
        "response_extract": response_extract,
        "response_copy": response_copy
    }

    print(log)


if __name__ == "__main__":

    event = {
        "file_name": "repayments.csv",
        "remote_path": "/acme-investments/Repayments.xlsx",
        "copy_to_table": "COPY_REPAYMENTS_STG"
    }

    # event = {
    #     "file_name": "loan_tape.csv",
    #     "remote_path": "/acme-investments/Loan Tape.xlsx",
    #     "copy_to_table": "COPY_LOAN_TAPE_STG"
    # }
    lambda_handler(event)
