import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_binance_candles(symbol="BTCUSDT", interval="1h", limit=2):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    candles = []
    for candle in data:
    if not isinstance(candle, list) or len(candle) < 5:
        continue  # skip jika data tidak lengkap
    try:
        candles.append({
            "time": int(candle[0]),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
        })
    except ValueError:
        continue  # skip jika data tidak valid
    return candles

def detect_engulfing(candles):
    prev = candles[0]
    last = candles[1]

    if (prev['close'] < prev['open']) and \
       (last['close'] > last['open']) and \
       (last['open'] < prev['close']) and \
       (last['close'] > prev['open']):
        return "📈 Bullish Engulfing terdeteksi di BTCUSDT (1H)"

    elif (prev['close'] > prev['open']) and \
         (last['close'] < last['open']) and \
         (last['open'] > prev['close']) and \
         (last['close'] < prev['open']):
        return "📉 Bearish Engulfing terdeteksi di BTCUSDT (1H)"

    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def main():
    candles = get_binance_candles()
    signal = detect_engulfing(candles)
    if signal:
        send_telegram_message(signal)

if __name__ == "__main__":
    main()
