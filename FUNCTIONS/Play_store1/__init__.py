import datetime
import logging

import azure.functions as func

from . import devRanks 

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    devRanks.run()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
