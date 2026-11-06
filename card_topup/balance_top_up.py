""" On a weekly basis, tops up my card to a specific balance
"""
from os import getenv
from pathlib import Path

from utils.monzo_api_handler import get_pots, get_balance, withdraw_pot
import datetime
from dotenv import load_dotenv

from utils.monzo_auth_handler import refresh_access


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TOP_UP_DAY = int(getenv("TOP_UP_DAY", 0))
SOURCE_POT = getenv("SOURCE_POT", "")
TARGET_BALANCE = int(getenv("TARGET_BALANCE", 100))
TARGET_ACCOUNT = getenv("TARGET_ACCOUNT", "")


def get_next_topup_date() -> str:
    """Gets the date of the next topup date, returns today's date if it is topup day"""
    current_date = datetime.datetime.now()

    days_ahead = TOP_UP_DAY - current_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    next = current_date + datetime.timedelta(days_ahead)
    return next.strftime('%Y-%m-%d')


def get_pot_balance(pot_name: str) -> int:
    """Gets the balance of a specific pot, has to search the list of pots"""
    pots = get_pots(TARGET_ACCOUNT)
    for pot in pots.get("pots", []):
        if pot.get('id') == pot_name:
            return pot.get('balance', 0)
    return 0


def decide_top_up_amount() -> int:
    balance_json = get_balance(TARGET_ACCOUNT)

    pot_balance = get_pot_balance(SOURCE_POT)

    balance = balance_json.get("balance", 0)

    # Top up to the target balance or empty the pot if the value is insufficent
    return min((TARGET_BALANCE*100)-balance, pot_balance)


def topup():
    """Tops up the pot to the specified amount, this will only run ONCE a week using cron"""
    top_up_amount = decide_top_up_amount()
    # TODO: Setup proper logging for this
    if top_up_amount > 0:
        r = withdraw_pot(SOURCE_POT, TARGET_ACCOUNT, top_up_amount,
                         f"weekly-topup-{get_next_topup_date}")
        print(r)
    else:
        print("Account is already over target amount")


if __name__ == "__main__":
    # As this script runs perodically in the background, each time it is ran,
    # refresh access to ensure that the token hasn't expired
    refresh_access()

    topup()
