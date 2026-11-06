from typing import Dict

import requests
from dotenv import load_dotenv
from utils.monzo_auth_handler import get_access_token

load_dotenv()


def get_accounts() -> Dict:
    url = "https://api.monzo.com/accounts"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    r = requests.get(url, headers=headers)

    r.raise_for_status()

    data = r.json()
    return data


def get_balance(account_id: str) -> Dict:
    url = "https://api.monzo.com/balance"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {"account_id": account_id}
    r = requests.get(url, headers=headers, params=params)

    r.raise_for_status()

    data = r.json()
    return data


def get_pots(account_id: str) -> Dict:
    url = "https://api.monzo.com/pots"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {"current_account_id": account_id}
    r = requests.get(url, headers=headers, params=params)

    r.raise_for_status()

    data = r.json()
    return data


def deposit_pot(pot_id: str, account_id: str, amount: int, dedupe_id: str) -> Dict:
    url = f"https://api.monzo.com/pots/{pot_id}/deposit"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {
        "source_account_id": account_id,
        "amount": amount,
        "dedupe_id": dedupe_id
    }
    r = requests.put(url, headers=headers, data=data)

    r.raise_for_status()

    data = r.json()
    return data


def withdraw_pot(pot_id: str, account_id: str, amount: int, dedupe_id: str) -> Dict:
    url = f"https://api.monzo.com/pots/{pot_id}/withdraw"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {
        "destination_account_id": account_id,
        "amount": amount,
        "dedupe_id": dedupe_id
    }
    r = requests.put(url, headers=headers, data=data)

    r.raise_for_status()

    data = r.json()
    return data


def get_transaction(transaction_id: str) -> Dict:
    url = f"https://api.monzo.com/transactions/{transaction_id}"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {"expand[]": "merchant"}
    r = requests.get(url, headers=headers, params=params)

    r.raise_for_status()

    data = r.json()
    return data


def get_transactions(account_id: str) -> Dict:
    url = "https://api.monzo.com/transactions"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {"account_id": account_id}
    r = requests.get(url, headers=headers, params=params)

    r.raise_for_status()

    data = r.json()
    return data


def update_transaction_metadata(transaction_id: str, metadata: Dict) -> Dict:
    url = f"https://api.monzo.com/transactions/{transaction_id}"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {
        f"metadata[{key}]": value
        for key, value in metadata.items()
    }
    r = requests.patch(url, headers=headers, data=data)

    r.raise_for_status()

    data = r.json()
    return data


def upload_attachment(file_name: str, file_type: str, content_length: int) -> Dict:
    url = "https://api.monzo.com/attachment/upload"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {
        "file_name": file_name,
        "file_type": file_type,
        "content_length": content_length
    }
    r = requests.post(url, headers=headers, data=data)

    r.raise_for_status()

    data = r.json()
    return data


def register_attachment(external_id: str, file_type: str, file_url: str) -> Dict:
    url = "https://api.monzo.com/attachment/register"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {
        "external_id": external_id,
        "file_type": file_type,
        "file_url": file_url
    }
    r = requests.post(url, headers=headers, data=data)

    r.raise_for_status()

    data = r.json()
    return data


def deregister_attachment(attachment_id: str) -> Dict:
    url = "https://api.monzo.com/attachment/deregister"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {"id": attachment_id}
    r = requests.post(url, headers=headers, data=data)

    r.raise_for_status()

    data = r.json()
    return data


def create_transaction_receipt(receipt_data: Dict) -> Dict:
    url = "https://api.monzo.com/transaction-receipts"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    r = requests.put(url, headers=headers, json=receipt_data)

    r.raise_for_status()

    data = r.json()
    return data


def get_transaction_receipt(external_id: str) -> Dict:
    url = "https://api.monzo.com/transaction-receipts"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {"external_id": external_id}
    r = requests.get(url, headers=headers, params=params)

    r.raise_for_status()

    data = r.json()
    return data


def delete_transaction_receipt(external_id: str) -> Dict:
    url = "https://api.monzo.com/transaction-receipts"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {"external_id": external_id}
    r = requests.delete(url, headers=headers, params=params)

    r.raise_for_status()

    data = r.json()
    return data


def create_webhook(account_id: str, url: str) -> Dict:
    api_url = "https://api.monzo.com/webhooks"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {
        "account_id": account_id,
        "url": url
    }
    r = requests.post(api_url, headers=headers, data=data)

    r.raise_for_status()

    data = r.json()
    return data


def get_webhooks(account_id: str) -> Dict:
    url = "https://api.monzo.com/webhooks"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {"account_id": account_id}
    r = requests.get(url, headers=headers, params=params)

    r.raise_for_status()

    data = r.json()
    return data


def delete_webhook(webhook_id: str) -> Dict:
    url = f"https://api.monzo.com/webhooks/{webhook_id}"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    r = requests.delete(url, headers=headers)

    r.raise_for_status()

    data = r.json()
    return data
