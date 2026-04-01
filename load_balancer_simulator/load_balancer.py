import random

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers

    def distribute(self, request):
        raise NotImplementedError("Subclasses must implement this method")

class RoundRobinBalancer(LoadBalancer):
    def __init__(self, servers):
        super().__init__(servers)
        self.current_index = 0

    def distribute(self, request):
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server

class LeastConnectionsBalancer(LoadBalancer):
    def distribute(self, request):
        # find the sever with the least current load (acting as connections here for simplicity)
        return min(self.servers, key=lambda s: s.current_load)

class RandomBalancer(LoadBalancer):
    def distribute(self, request):
        return random.choice(self.servers)
