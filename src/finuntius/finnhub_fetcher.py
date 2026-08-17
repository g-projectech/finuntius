import os
import re
import time
import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from finuntius.translations import t, DEFAULT_LANGUAGE

FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/company-news"
FINNHUB_PROFILE_URL = "https://finnhub.io/api/v1/stock/profile2" #endpoint usato per ottenre profilo di una società
ISIN_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$") #standrad ISO 6166
MAX_RETRIES_ON_RATE_LIMIT = 2
RETRY_BACKOFF_SECONDS = 5

#verifica se l'ISIN segue lo standard ISO 6166
def is_valid_isin(value: str) -> bool:
    return bool(ISIN_PATTERN.match(value.strip().upper()))

#pulisce il ticker da spazi vuoti e lo rende tutto in MAIUSC
def clean_symbol(symbol: str) -> str:
    return symbol.strip().upper()

#esegue richiesta GET alle API e gestisce anche limite di richieste (429) mettendosi in pausa
def _retry_on_rate_limit(url: str, params: dict) -> requests.Response:
    attempt = 0
    while True:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 429 and attempt < MAX_RETRIES_ON_RATE_LIMIT:
            retry_after = response.headers.get("Retry-After")
            wait_seconds = float(retry_after) if retry_after else RETRY_BACKOFF_SECONDS * (attempt + 1)
            time.sleep(wait_seconds)
            attempt += 1
            continue

        return response

#passa ISIN e key dell'utente alle API, gestisce eventuali errori, e restitisce dati cercando ticker
def resolve_isin_to_symbol(isin: str, token: str, lang: str = DEFAULT_LANGUAGE) -> str:
    try:
        response = _retry_on_rate_limit(FINNHUB_PROFILE_URL, {"isin": isin, "token": token})

        if response.status_code == 401:
            raise RuntimeError(t("invalid_api_key", lang))
        elif response.status_code == 403:
            raise RuntimeError(t("isin_paid_required", lang))
        elif response.status_code == 429:
            raise RuntimeError(t("rate_limit", lang))

        response.raise_for_status()
        data = response.json() or {}

        ticker = data.get("ticker")
        if not ticker:
            raise RuntimeError(t("isin_not_found", lang, isin=isin))

        return ticker

    except requests.RequestException as err:
        raise RuntimeError(t("network_error", lang, err=err))

# rimuove titoli duplicati
def _remove_duplicates(items: List[Dict]) -> List[Dict]:
    seen_titles = set()
    unique_items = []
    for item in items:
        title_hash = (item.get("headline") or "").strip().lower()
        if title_hash and title_hash in seen_titles:
            continue
        if title_hash:
            seen_titles.add(title_hash)
        unique_items.append(item)
    return unique_items

# recupera e formatta le news finanziarie da finhub per ticker o ISIN in questione
def fetch_financial_news(
    symbol: str,
    max_items: int = 5,
    api_key: str = None,
    days_back: int = 7,
    lang: str = DEFAULT_LANGUAGE
) -> List[Dict[str, str]]:
    token = api_key or os.getenv("FINNHUB_API_KEY")

    if not token:
        raise ValueError(t("missing_api_key", lang))

    raw_symbol = symbol.strip()

    if is_valid_isin(raw_symbol):
        final_clean_symbol = resolve_isin_to_symbol(raw_symbol.upper(), token, lang)
    else:
        final_clean_symbol = clean_symbol(raw_symbol)

    to_date = datetime.now(timezone.utc)
    from_date = to_date - timedelta(days=days_back)

    params = {
        "symbol": final_clean_symbol,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "token": token
    }

    try:
        response = _retry_on_rate_limit(FINNHUB_NEWS_URL, params)

        if response.status_code == 401:
            raise RuntimeError(t("invalid_api_key", lang))
        elif response.status_code == 403:
            raise RuntimeError(t("premium_ticker_required", lang))
        elif response.status_code == 429:
            raise RuntimeError(t("rate_limit", lang))

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            raise RuntimeError(t("unexpected_response", lang, data=data))

        data = _remove_duplicates(data)

        data.sort(key=lambda x: x.get("datetime", 0), reverse=True)

        formatted_articles = []
        for item in data[:max_items]:
            timestamp_raw = item.get("datetime")
            dt_str = "N/A"
            if timestamp_raw is not None:
                dt_str = datetime.fromtimestamp(timestamp_raw, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

            formatted_articles.append({
                "title": item.get("headline", "N/A"),
                "source": item.get("source", "Unknown"),
                "date": dt_str,
                "link": item.get("url", "N/A"),
                "summary": item.get("summary", "")
            })

        return formatted_articles

    except requests.RequestException as err:
        raise RuntimeError(t("network_error", lang, err=err))