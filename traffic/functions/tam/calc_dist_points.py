def calc_dist(df):

    import pandas as pd
    import math
    dist = []

    # Get dist from https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    def deg2rad(deg):
        return deg * (math.pi/180)

    def get_dist(lat1,lon1,lat2,lon2,feeder):
        R = 6371
        dLat = deg2rad(lat2-lat1)
        dLon = deg2rad(lon2-lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
            math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c * 0.62137119 # km to miles

        # if its a feeder node, very small number
        if feeder == 'zone':
            d = 1/(10**9)
        return d

    for x in range(df.shape[0]):
        dist.append(get_dist(df['from_lat'][x], df['from_lon'][x], df['to_lat'][x], df['to_lon'][x], df['link_type'][x]))
    df['dist'] = dist

    return df
