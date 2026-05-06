import json
from src.analyzer.historical_fetcher import fetch_dataset
from src.analyzer.features import extract_blip_features
from src.analyzer.correlator import compute_correlation

def main():
    print("Fetching dataset of 50 resolved markets...")
    dataset = fetch_dataset(target_count=50)
    print(f"Successfully fetched {len(dataset)} valid markets with history.")
    
    if not dataset:
        print("Not enough data to run correlation.")
        return
        
    print("Extracting retroactive blip features...")
    blip_features = []
    
    for market_data in dataset:
        features = extract_blip_features(market_data)
        if features:
            blip_features.append(features)
            
    print(f"Extracted {len(blip_features)} blips from {len(dataset)} markets.")
    
    if not blip_features:
        print("No blips found using current thresholds.")
        return
        
    print("Computing correlation analysis...")
    results = compute_correlation(blip_features)
    
    print("\n" + "="*50)
    print("PHASE 1: BLIP CORRELATION ANALYSIS RESULTS")
    print("="*50)
    
    print(f"\nTotal Markets Analyzed: {results['total_markets_analyzed']}")
    print(f"Overall Accuracy (Price Delta -> Outcome): {results['accuracy']:.1%}")
    print(f"Correct Predictions: {results['correct_predictions']}")
    
    print("\n--- Accuracy By Category ---")
    for cat, data in results['by_category'].items():
        print(f"{cat}: {data['accuracy']:.1%} ({data['correct']}/{data['total']})")
        
    print("\n--- Accuracy By Time Window ---")
    for window, data in results['time_window_accuracy'].items():
        if data['total'] > 0:
            print(f"{window}: {data['accuracy']:.1%} ({data['correct']}/{data['total']})")
        else:
            print(f"{window}: No blips detected")
            
    print("\n" + "="*50)

    # Save to docs directory in the repository
    import os
    # Get absolute path to the repo root's docs folder
    repo_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_dir = os.path.join(repo_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    raw_data_path = os.path.join(docs_dir, "phase1_raw_data.json")
    with open(raw_data_path, "w") as f:
        json.dump(blip_features, f, indent=2)
        
    detailed_md_path = os.path.join(docs_dir, "phase1_results.md")
    with open(detailed_md_path, "w") as f:
        f.write("# Phase 1: Detailed Correlation Analysis\n\n")
        f.write("## Summary\n")
        f.write(f"- **Total Markets Analyzed:** {results['total_markets_analyzed']}\n")
        f.write(f"- **Overall Accuracy:** {results['accuracy']:.1%} ({results['correct_predictions']}/{results['total_markets_analyzed']})\n\n")
        
        f.write("## Detailed Market Blips\n")
        f.write("| Market | Time to Close | Trigger | Price Delta | Predicted Outcome | Actual Outcome | Correct |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for blip in blip_features:
            q = blip.get('question', 'Unknown')
            if len(q) > 40:
                q = q[:37] + "..."
            hrs = f"{blip['hours_to_close']:.1f}h"
            trig = blip['trigger_type']
            delta = f"{blip['price_delta']:.3f}"
            pred = "Yes" if blip["price_direction"] == "UP" else "No"
            actual = blip['winning_outcome']
            correct = "✅" if pred == actual else "❌"
            f.write(f"| {q} | {hrs} | {trig} | {delta} | {pred} | {actual} | {correct} |\n")
            
    print(f"\nDetailed results saved to {detailed_md_path}")
    print(f"Raw JSON data saved to {raw_data_path}")

if __name__ == "__main__":
    main()
