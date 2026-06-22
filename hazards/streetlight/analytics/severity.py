def calculate_severity(brightness_score, flicker_score, config):
    brightness_weight = config.get("weights", {}).get("brightness", 0.7)
    flicker_weight = config.get("weights", {}).get("flicker", 0.3)

    severity = ((1 - brightness_score) * brightness_weight) + \
               (flicker_score * flicker_weight)

    return min(severity, 1.0)
