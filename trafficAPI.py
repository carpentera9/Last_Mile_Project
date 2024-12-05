import http.client
import json

# API Key for TomTom
api_key = 'vIWAkgxeRxGm3GsoHEdyv95p4Tf1qkc5'

# List of major highways with coordinates (latitude, longitude) in Cincinnati, Newport, and Northern Kentucky
# Each highway has two points: one for northbound and one for southbound
highways = {
    'I-71': {'north': '39.1072,-84.5045', 'south': '39.1000,-84.5100'},
    'I-74': {'north': '39.1310,-84.5477', 'south': '39.1200,-84.5500'},
    'I-75': {'north': '39.0736,-84.5323', 'south': '39.0600,-84.5400'},
    'I-275': {'north': '39.0663,-84.3748', 'south': '39.0600,-84.3800'},
    'US-50': {'north': '39.0920,-84.5200', 'south': '39.0800,-84.5300'},
    'OH-126': {'north': '39.2290,-84.3950', 'south': '39.2200,-84.4000'},
    'I-471': {'north': '39.0911,-84.4960', 'south': '39.0800,-84.5000'},
    'KY-8': {'north': '39.0920,-84.4950', 'south': '39.0800,-84.5000'},
    'KY-18': {'north': '39.0462,-84.6632', 'south': '39.0400,-84.6700'},
    'KY-237': {'north': '39.0481,-84.6700', 'south': '39.0400,-84.6750'}
}

# Function to get traffic flow information
def get_traffic_flow(point):
    conn = http.client.HTTPSConnection("api.tomtom.com")
    url = f"/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point={point}"
    conn.request("GET", url)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        return json.loads(data)
    else:
        return None

# Check traffic flow for each highway in both directions
print("Traffic Predictions for Major Highways in Cincinnati, Newport, and Northern Kentucky:")
for highway, directions in highways.items():
    for direction, point in directions.items():
        traffic_flow = get_traffic_flow(point)
        
        if traffic_flow:
            flow_data = traffic_flow.get("flowSegmentData", {})
            current_speed = flow_data.get("currentSpeed", 0)
            free_flow_speed = flow_data.get("freeFlowSpeed", 0)
            delay = current_speed < free_flow_speed
            
            if delay:
                prediction = f"Traffic delay detected. Current speed is {current_speed} mph, which is below the free-flow speed of {free_flow_speed} mph."
            else:
                prediction = f"No delay, traffic is flowing normally. Current speed is {current_speed} mph."
            
            print(f"{highway} ({direction.capitalize()}bound): {prediction}")
        else:
            print(f"{highway} ({direction.capitalize()}bound): Failed to retrieve traffic flow information.")
