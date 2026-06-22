
def calculate_psri(fire_area, smoke_area, fire_count, smoke_count, persistence_duration, people_exposure, vehicle_exposure, config):
    weights = config.get("psri_weights", {})
    w_fa = weights.get("fire_area", 0.3)
    w_sa = weights.get("smoke_area", 0.1)
    w_fc = weights.get("fire_count", 0.2)
    w_sc = weights.get("smoke_count", 0.1)
    w_pd = weights.get("persistence_duration", 0.1)
    w_pe = weights.get("people_exposure", 0.1)
    w_ve = weights.get("vehicle_exposure", 0.1)
    
    # Normalize inputs (Assuming typical max values for 1.0 normalization)
    norm_fa = min(1.0, fire_area)  # Area as fraction of frame (0.0 to 1.0)
    norm_sa = min(1.0, smoke_area)
    norm_fc = min(1.0, fire_count / 10.0)
    norm_sc = min(1.0, smoke_count / 10.0)
    norm_pd = min(1.0, persistence_duration / 100.0) # max 100 frames
    norm_pe = min(1.0, people_exposure / 50.0)
    norm_ve = min(1.0, vehicle_exposure / 20.0)
    
    psri = (norm_fa * w_fa) + (norm_sa * w_sa) + (norm_fc * w_fc) + (norm_sc * w_sc) + (norm_pd * w_pd) + (norm_pe * w_pe) + (norm_ve * w_ve)
    return min(1.0, psri)
