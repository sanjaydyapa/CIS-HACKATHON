import time
import random
from models import Request, Server

class Simulator:
    def __init__(self, balancer_class, num_servers, server_capacity, num_requests):
        self.servers = [Server(id=i, capacity=server_capacity) for i in range(num_servers)]
        self.balancer = balancer_class(self.servers)
        self.num_requests = num_requests
        self.history = []  # To track load over time

    def run(self):
        for i in range(self.num_requests):
            # Simulate a request arriving
            req = Request(id=i, weight=random.randint(1, 10))
            
            # Balancer chooses server
            chosen_server = self.balancer.distribute(req)
            chosen_server.add_load(req.weight)

            # Record state step by step for each server
            snapshot = {s.id: s.current_load for s in self.servers}
            self.history.append(snapshot)

            # Randomly simulate some requests completing (releasing load)
            if random.random() < 0.4:
                # Pick a random server to release some load
                release_server = random.choice(self.servers)
                if release_server.current_load > 0:
                    release_server.release_load(random.randint(1, min(10, release_server.current_load)))

    def get_overloaded_servers(self):
        return [s for s in self.servers if s.is_overloaded()]

    def get_distribution_stats(self):
        return {s.id: s.requests_handled for s in self.servers}
