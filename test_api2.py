import requests
import json

def test():
    condition_id = "0x9c1a953fe92c8357f1b646ba25d983aa83e90c525992db14fb726fa895cb5763"
    url = f"https://gamma-api.polymarket.com/markets?conditionId={condition_id}"
    resp = requests.get(url)
    data = resp.json()
    if data:
        for m in data:
            o = m.get("outcomes")
            print("Outcomes type:", type(o))
            if isinstance(o, str):
                o = json.loads(o)
            print("Length:", len(o))
            break

if __name__ == "__main__":
    test()
