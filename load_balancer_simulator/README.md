# ⚖️ Load Balancer Simulator

![Live on Vercel](https://img.shields.io/badge/Deployed_on-Vercel-black?logo=vercel)
![Python](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![Frontend](https://img.shields.io/badge/Frontend-Chart.js-FF6384?logo=chartdotjs)

A visual simulator demonstrating how different web traffic routing algorithms (Round Robin, Least Connections, Random) handle uneven traffic spikes across a cluster of servers.

**🚀 Live Demo:** [https://cis-hackathon-one.vercel.app/](https://cis-hackathon-one.vercel.app/)

## 📖 Built for Hackathons & Presentations
Modern web applications face uneven traffic distribution, leading to server overload. This project simulates a server environment where each incoming user request carries a different "weight" (processing difficulty - e.g., loading a text file vs. uploading a 4K video). 

By passing identical traffic through three different load balancers, the dashboard mathematically proves why "smart routing" (Least Connections) prevents crashes, while naive routing (Round Robin/Random) inevitably leads to system failures.

## ⚙️ How It Works (The Algorithms)

*   **🔁 Round Robin:** Passes requests sequentially to each server in a loop (1→2→3→1). It's fast but blind. If it accidentally hands multiple "heavy" requests to Server #2, Server #2's capacity spikes and it becomes overloaded.
*   **🧠 Least Connections (Optimal):** Smart routing. Before assigning a request, it checks which server is currently the least busy and routes traffic there. This dynamically prevents bottlenecks and keeps the server cluster stable.
*   **🎲 Random:** Picks a server purely by chance. Highly unpredictable and frequently causes accidental overloads and unequal load distribution.

## 🛠️ How to Run Locally

1. **Navigate to the project folder:**
   ```bash
   cd load_balancer_simulator
   ```

2. **Install dependencies:**  
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI backend:**
   ```bash
   python -m uvicorn api.index:app --reload
   ```

4. **Open the Dashboard:**  
   Open your browser and navigate to exactly: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

## 🗂️ Project Structure

*   `api/index.py` - FastAPI backend. Simulates the load balancing logic, creates the servers & requests, computes the data step-by-step, and serves the frontend.
*   `public/index.html` - Sleek, modern frontend utilizing `Chart.js` for dynamic visualizations and animations.
*   `vercel.json` - Serverless deployment configuration for Vercel.
