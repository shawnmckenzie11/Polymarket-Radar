import requests
import json
import time

def fetch_closed_markets(limit=50):
    """Fetch recent closed markets from Gamma API."""
    url = f"https://gamma-api.polymarket.com/markets?closed=true&limit={limit}&order=createdAt&ascending=false"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching closed markets: {e}")
        return []

def fetch_dataset(target_count=50):
    dataset = []
    print(f"Fetching {target_count} active high-volume markets for retroactive correlation...")
    
    url = f"https://gamma-api.polymarket.com/markets?active=true&limit={target_count*2}&order=volume&ascending=false"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print("Failed to fetch markets.")
            return dataset
        markets = resp.json()
        print(f"Retrieved {len(markets)} markets from Gamma. Checking for CLOB history...")
        
        for idx, market in enumerate(markets):
            outcomes = market.get("outcomes", "[]")
            if isinstance(outcomes, str):
                try: outcomes = json.loads(outcomes)
                except: outcomes = []
                
            if not outcomes or len(outcomes) != 2:
                continue
                
            clob_ids = []
            try:
                clob_ids = json.loads(market.get("clobTokenIds", "[]"))
            except:
                pass
                
            if not clob_ids:
                continue
                
            prices = market.get("outcomePrices", "[]")
            if isinstance(prices, str):
                try: prices = json.loads(prices)
                except: prices = []
                
            winning_outcome = None
            if len(prices) == 2:
                try:
                    p1 = float(prices[0])
                    p2 = float(prices[1])
                    # Simulate outcome based on current leader
                    winning_outcome = outcomes[0] if p1 > p2 else outcomes[1]
                except:
                    pass
                    
            if not winning_outcome:
                continue
                
            yes_token_id = clob_ids[0]
            
            url_clob = f"https://clob.polymarket.com/prices-history?market={yes_token_id}&interval=1m&fidelity=60"
            resp_clob = requests.get(url_clob, timeout=10)
            history = []
            if resp_clob.status_code == 200:
                history = resp_clob.json().get("history", [])
            
            if len(history) < 5:
                continue
                
            dataset.append({
                "condition_id": market.get("conditionId"),
                "question": market.get("question"),
                "category": market.get("category", "Unknown"),
                "winning_outcome": winning_outcome,
                "history": history
            })
            print(f"[{len(dataset)}/{target_count}] Parsed history for: {market.get('question')[:50]}...")
            
            if len(dataset) >= target_count:
                break
                
    except Exception as e:
        print(f"Error fetching data: {e}")
        
    return dataset
