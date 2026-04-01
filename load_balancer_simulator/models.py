class Request:
    def __init__(self, id, weight=1):
        self.id = id
        self.weight = weight

class Server:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.current_load = 0
        self.requests_handled = 0

    def add_load(self, request_weight):
        self.current_load += request_weight
        self.requests_handled += 1
        
    def release_load(self, request_weight):
        self.current_load = max(0, self.current_load - request_weight)

    def is_overloaded(self):
        return self.current_load > self.capacity

    def get_utilization(self):
        return (self.current_load / self.capacity) * 100
