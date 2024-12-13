import argparse
from load_balancer.load_balancer import LoadBalancer

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments to configure the load balancer.

    Returns:
        argparse.Namespace: Parsed arguments containing host, port, and health check interval.
    """
    parser = argparse.ArgumentParser(description="Run a Load Balancer.")
    parser.add_argument("--host", type=str, default="localhost", help="The hostname or IP address to bind to (default: localhost).")
    parser.add_argument("--port", type=int, default=5432, help="The port number to listen on (default: 5432).")
    parser.add_argument("--health-check-interval", type=int, default=15, help="Interval for health checks in seconds (default: 15).")
    return parser.parse_args()


if __name__ == "__main__":
    args: argparse.Namespace = parse_arguments()
    load_balancer: LoadBalancer = LoadBalancer(host=args.host, port=args.port, health_check_interval=args.health_check_interval)
    load_balancer.start()
