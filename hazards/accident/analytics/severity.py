def calculate_acri(accident_area, pedestrian_count, accident_count,
                   persistence_duration, vehicle_count, config):
    """
    ACRI — Accident & Collision Risk Index.
    Mirrors PSRI from the fire module but tuned for road accident hazards.

    Inputs:
        accident_area       : sum of bbox areas for 'accident' detections (0.0 - 1.0)
        pedestrian_count    : number of pedestrians estimated in frame
        accident_count      : number of 'accident' bounding boxes in frame
        persistence_duration: consecutive frames the hazard has been present
        vehicle_count       : number of vehicles in frame
        config              : thresholds.yaml dict

    Returns:
        acri (float) in range [0.0, 1.0]
    """
    weights = config.get("acri_weights", {})

    w_aa = weights.get("accident_area", 0.35)
    w_pc = weights.get("pedestrian_count", 0.25)
    w_ac = weights.get("accident_count", 0.20)
    w_pd = weights.get("persistence_duration", 0.10)
    w_vd = weights.get("vehicle_density", 0.10)

    # Normalize each input to 0.0 – 1.0
    norm_aa = min(1.0, accident_area)                   # already a fraction of frame
    norm_pc = min(1.0, pedestrian_count / 20.0)         # max 20 pedestrians expected
    norm_ac = min(1.0, accident_count / 5.0)            # max 5 simultaneous accident boxes
    norm_pd = min(1.0, persistence_duration / 100.0)    # max 100 persistence frames
    norm_vd = min(1.0, vehicle_count / 20.0)            # max 20 vehicles expected

    acri = (
        norm_aa * w_aa +
        norm_pc * w_pc +
        norm_ac * w_ac +
        norm_pd * w_pd +
        norm_vd * w_vd
    )

    return min(1.0, acri)
