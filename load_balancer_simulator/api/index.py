from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Core Logic ---
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

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
    def distribute(self, request):
        raise NotImplementedError()

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
        return min(self.servers, key=lambda s: s.current_load)

class RandomBalancer(LoadBalancer):
    def distribute(self, request):
        return random.choice(self.servers)

class Simulator:
    def __init__(self, balancer_class, num_servers, server_capacity, num_requests):
        self.servers = [Server(id=i, capacity=server_capacity) for i in range(num_servers)]
        self.balancer = balancer_class(self.servers)
        self.num_requests = num_requests
        self.history = []

    def run(self):
        for i in range(self.num_requests):
            req = Request(id=i, weight=random.randint(1, 10))
            chosen_server = self.balancer.distribute(req)
            chosen_server.add_load(req.weight)

            snapshot = {s.id: s.current_load for s in self.servers}
            self.history.append(snapshot)

            if random.random() < 0.4:
                release_server = random.choice(self.servers)
                if release_server.current_load > 0:
                    release_server.release_load(random.randint(1, min(10, release_server.current_load)))

# --- API Endpoints ---
class SimulationRequest(BaseModel):
    num_servers: int = 4
    server_capacity: int = 50
    num_requests: int = 100

@app.post("/api/simulate")
def run_simulation(req: SimulationRequest):
    balancers = {
        "Round Robin": RoundRobinBalancer,
        "Least Connections": LeastConnectionsBalancer,
        "Random": RandomBalancer
    }
    
    results = {}
    for name, b_class in balancers.items():
        sim = Simulator(b_class, req.num_servers, req.server_capacity, req.num_requests)
        sim.run()
        results[name] = {
            "history": sim.history,
            "distribution": {s.id: s.requests_handled for s in sim.servers},
            "overloaded": [s.id for s in sim.servers if s.is_overloaded()]
        }
        
    return {"results": results}


import os
from fastapi.staticfiles import StaticFiles

# --- Local Development Static Files ---
current_dir = os.path.dirname(os.path.realpath(__file__))
public_dir = os.path.join(os.path.dirname(current_dir), "public")
if os.path.exists(public_dir):
    app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
