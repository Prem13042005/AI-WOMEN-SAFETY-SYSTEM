def get_location_type(lat, lon):
    # For demo: dummy classifier
    if 18.5 < lat < 18.6 and 73.8 < lon < 73.9:
        return 2  # High risk slum area
    elif 18.6 < lat < 18.65:
        return 0  # Urban safe
    else:
        return 1  # Unknown/medium risk
