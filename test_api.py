import requests

def test():
    # token ID for Russia-Ukraine ceasefire market
    token_id = "8501497159083948713316135768103773293754490207922884688769443031624417212426"
    
    for interval in ["1m", "5m", "15m", "1h", "1d"]:
        url = f"https://clob.polymarket.com/prices-history?market={token_id}&interval={interval}&fidelity=60"
        r = requests.get(url)
        if r.status_code == 200:
            h = r.json().get("history", [])
            print(f"Interval {interval}: {len(h)} points")
        else:
            print(f"Interval {interval}: error {r.status_code}")

if __name__ == "__main__":
    test()
