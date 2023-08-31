from app.elt import Extraction
from utils import logger
import traceback
import time
from utils.clients.sftpclient import SFTPClient


def lambda_handler(event, context=None):

    elt = Extraction(

        event.get('file_name'),
        event.get('remote_path')
    )

    response = elt.extract_and_load()

    print(response)


if __name__ == "__main__":
    # file_name = 'loan_tape.csv'
    # remote_path = '/acme-investments/Loan Tape.xlsx'
    # remote_path = "/acme-investments/Repayments.xlsx"
    event = {
        "file_name": "repayments.csv",
        "remote_path": "/acme-investments/Repayments.xlsx"
    }
    lambda_handler(event)
