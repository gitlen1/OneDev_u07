import requests
from prometheus_client import start_http_server, Gauge
import time

# OneDev API endpoint for build data
ONEDV_API_URL = "http://172.232.159.177:6610/~api/builds"

# Prometheus metric definition
build_status_metric = Gauge('onedev_build_status', 'OneDev Build Status', ['project', 'branch'])

def fetch_and_export_build_data():
    try:
        response = requests.get(ONEDV_API_URL)
        response.raise_for_status()
        build_data = response.json()

        for build in build_data:
            project = build['project']
            branch = build['branch']
            status = build['status']

            # Export build status as a Prometheus metric
            build_status_metric.labels(project=project, branch=branch).set(status)

    except Exception as e:
        print(f"Error fetching build data from OneDev: {str(e)}")

if __name__ == '__main__':
    # Start a Prometheus HTTP server on port 9101
    start_http_server(9101)

    while True:
        # Fetch and export build data periodically
        fetch_and_export_build_data()
        time.sleep(30) 
