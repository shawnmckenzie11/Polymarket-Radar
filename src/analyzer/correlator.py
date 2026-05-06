"""
Blip-to-outcome correlation.

Analyzes whether pre-resolution blip signals correlate with YES/NO outcomes.
"""



def compute_correlation(blip_features: list) -> dict:
    """
    Compute correlation between blip signals and outcomes.

    Args:
        blip_features: List of feature dicts from extract_blip_features().

    Returns:
        Correlation analysis dict.
    """
    results = {
        "total_markets_analyzed": len(blip_features),
        "correct_predictions": 0,
        "accuracy": 0.0,
        "by_category": {},
        "time_window_accuracy": {
            "0-4h": {"total": 0, "correct": 0},
            "4-24h": {"total": 0, "correct": 0},
            "24h+": {"total": 0, "correct": 0}
        }
    }
    
    if not blip_features:
        return results
        
    for feature in blip_features:
        predicted = "Yes" if feature["price_direction"] == "UP" else "No"
        actual = feature["winning_outcome"]
        
        is_correct = predicted == actual
        if is_correct:
            results["correct_predictions"] += 1
            
        # Category breakdown
        cat = feature["category"]
        if cat not in results["by_category"]:
            results["by_category"][cat] = {"total": 0, "correct": 0}
        
        results["by_category"][cat]["total"] += 1
        if is_correct:
            results["by_category"][cat]["correct"] += 1
            
        # Time window breakdown
        h2c = feature["hours_to_close"]
        if h2c <= 4:
            window = "0-4h"
        elif h2c <= 24:
            window = "4-24h"
        else:
            window = "24h+"
            
        results["time_window_accuracy"][window]["total"] += 1
        if is_correct:
            results["time_window_accuracy"][window]["correct"] += 1

    results["accuracy"] = results["correct_predictions"] / len(blip_features)
    
    for cat, data in results["by_category"].items():
        data["accuracy"] = data["correct"] / data["total"] if data["total"] > 0 else 0
        
    for window, data in results["time_window_accuracy"].items():
        data["accuracy"] = data["correct"] / data["total"] if data["total"] > 0 else 0
        
    return results
