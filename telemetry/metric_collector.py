import time
import random
from prometheus_client import start_http_server, Gauge

# Define Prometheus Gauges for node metrics
CPU_USAGE = Gauge('node_cpu_usage_percent', 'CPU usage percentage', ['node_id'])
MEMORY_USAGE = Gauge('node_memory_usage_percent', 'Memory usage percentage', ['node_id'])

def collect_metrics():
    # Simulates streaming telemetry across distributed nodes
    nodes = ['node-alpha', 'node-beta', 'node-gamma']
    while True:
        for node in nodes:
            # Simulate occasional spike anomalies
            spike = random.choices([0, 45], weights=[0.9, 0.1])[0]
            cpu = min(100.0, max(5.0, random.gauss(40, 10) + spike))
            mem = min(100.0, max(10.0, random.gauss(60, 5) + (spike * 0.5)))
            
            CPU_USAGE.labels(node_id=node).set(cpu)
            MEMORY_USAGE.labels(node_id=node).set(mem)
        time.sleep(0.1)  # High frequency data generation

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus telemetry collector running on port 8000...")
    collect_metrics()
