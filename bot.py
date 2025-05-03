import requests
import os
from datetime import datetime

# Ambil token dan chat ID dari secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Parameter pair dan timeframe
PAIR = "BTCUSDT"
INTERVAL = "1h"
LIMIT = 3  # Ambil 3 candle terakhir

def get_binance_candles():
    url = f"https://api.binance.com/api/v3/klines?symbol={PAIR}&interval={INTERVAL}&limit={LIMIT}"
    response = requests.get(url)
    data = response.json()
    candles = []
    for candle in data:
        candles.append({
            "time": int(candle[0]),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
        })
    return candles

def is_bullish_engulfing(prev, curr):
    return prev["close"] < prev["open"] and curr["close"] > curr["open"] and curr["close"] > prev["open"] and curr["open"] < prev["close"]

def is_bearish_engulfing(prev, curr):
    return prev["close"] > prev["open"] and curr["close"] < curr["open"] and curr["open"] > prev["close"] and curr["close"] < prev["open"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def main():
    candles = get_binance_candles()
    if len(candles) < 2:
        return

    prev = candles[-2]
    curr = candles[-1]

    time_str = datetime.utcfromtimestamp(curr["time"] / 1000).strftime('%Y-%m-%d %H:%M')

    if is_bullish_engulfing(prev, curr):
        send_telegram_message(f"[{PAIR} - 1H] ✅ Bullish Engulfing terdeteksi pada candle jam {time_str}")
    elif is_bearish_engulfing(prev, curr):
        send_telegram_message(f"[{PAIR} - 1H] 🔻 Bearish Engulfing terdeteksi pada candle jam {time_str}")
    else:
        print("Tidak ada sinyal pada candle terakhir")

if __name__ == "__main__":
    main()
