import matplotlib.pyplot as plt
from simulator import Simulator
from load_balancer import RoundRobinBalancer, LeastConnectionsBalancer, RandomBalancer

def plot_history(ax, history, title):
    # Transpose history from list of dicts to dict of lists (per server)
    num_servers = len(history[0])
    lines = {i: [] for i in range(num_servers)}
    for snapshot in history:
        for i in range(num_servers):
            lines[i].append(snapshot[i])
            
    for i in range(num_servers):
        ax.plot(lines[i], label=f'Server {i}')
        
    ax.set_title(title)
    ax.set_xlabel('Time (Requests)')
    ax.set_ylabel('Current Load')
    ax.legend()

def main():
    print("Welcome to Load Balancer Simulator")
    
    num_servers = 4
    server_capacity = 50
    num_requests = 100

    balancers = [
        ("Round Robin", RoundRobinBalancer),
        ("Least Connections", LeastConnectionsBalancer),
        ("Random", RandomBalancer)
    ]

    fig, axes = plt.subplots(1, len(balancers), figsize=(15, 5))

    for idx, (name, balancer_class) in enumerate(balancers):
        print(f"\nRunning simulation for {name}...")
        sim = Simulator(balancer_class, num_servers, server_capacity, num_requests)
        sim.run()
        
        # Check distribution
        stats = sim.get_distribution_stats()
        print(f"Request distribution: {stats}")
        
        # Check overload
        overloaded = sim.get_overloaded_servers()
        if overloaded:
            print(f"Warning: {len(overloaded)} server(s) overloaded!")
        else:
            print("System stable: No overloaded servers.")

        # Plot
        plot_history(axes[idx], sim.history, name)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
