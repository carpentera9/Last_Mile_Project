import http.client
import json
import tkinter as tk

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

class TrafficFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.results_text = tk.Text(self, width=60, height=20, wrap='word', font=("Helvetica", 10))
        self.results_text.tag_configure("highway", font=("Helvetica", 12, "bold"))
        self.results_text.tag_configure("delay", foreground="red", font=("Helvetica", 10, "bold"))
        self.results_text.tag_configure("normal", foreground="green", font=("Helvetica", 10, "bold"))
        self.results_text.tag_configure("error", foreground="orange", font=("Helvetica", 10, "italic"))
        self.results_text.pack(pady=10)
        
        # Refresh button
        refresh_button = tk.Button(self, text="Refresh Traffic Info", command=self.refresh_traffic_info)
        refresh_button.pack(pady=5)

        # Initial load of traffic information
        self.refresh_traffic_info()

    # Function to get traffic flow information
    def get_traffic_flow(self, point):
        conn = http.client.HTTPSConnection("api.tomtom.com")
        url = f"/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point={point}"
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            return json.loads(data)
        else:
            return None

    # Function to refresh traffic information for each highway
    def refresh_traffic_info(self):
        self.results_text.delete(1.0, tk.END)  # Clear previous results
        self.results_text.insert(tk.END, "Traffic Information for Major Highways:\n\n")
        
        for highway, directions in highways.items():
            self.results_text.insert(tk.END, f"Highway: {highway}\n", "highway")
            
            for direction, point in directions.items():
                traffic_flow = self.get_traffic_flow(point)
                
                if traffic_flow:
                    flow_data = traffic_flow.get("flowSegmentData", {})
                    current_speed = flow_data.get("currentSpeed", 0)
                    free_flow_speed = flow_data.get("freeFlowSpeed", 0)
                    delay = current_speed < free_flow_speed

                    # Display formatted information
                    self.results_text.insert(tk.END, f"  {direction.capitalize()}bound:\n")
                    self.results_text.insert(tk.END, f"    Current Speed: {current_speed} mph\n")
                    self.results_text.insert(tk.END, f"    Free Flow Speed: {free_flow_speed} mph\n")
                    if delay:
                        self.results_text.insert(tk.END, f"    Status: Delay Detected\n", "delay")
                    else:
                        self.results_text.insert(tk.END, f"    Status: Traffic Flowing Normally\n", "normal")
                else:
                    self.results_text.insert(tk.END, f"  {direction.capitalize()}bound:\n")
                    self.results_text.insert(tk.END, "    Status: Failed to retrieve traffic flow information\n", "error")
            self.results_text.insert(tk.END, "-" * 40 + "\n")  # Separator line

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Traffic Information")
    traffic_frame = TrafficFrame(root)
    traffic_frame.pack(pady=20, padx=20)
    root.mainloop()
