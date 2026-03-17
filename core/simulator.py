import time
import random
from optimizer import LookThroughOptimizer

class EWSimulator:
    def __init__(self):
        self.optimizer = LookThroughOptimizer()
        self.active_threats = []
        self.running = True

    def spawn_threat(self):
        threat = {
            "id": random.randint(1000, 9999),
            "velocity": random.uniform(200, 800),
            "distance": random.uniform(50, 200) # km
        }
        self.active_threats.append(threat)
        print(f"[THREAT SPAWNED] ID: {threat['id']}, Speed: {threat['velocity']:.2f} m/s")

    def run_simulation(self, iterations=10):
        print("--- Starting Smart Look-Through Simulation ---")
        for i in range(iterations):
            if random.random() > 0.7:
                self.spawn_threat()
            
            pw, iv = self.optimizer.optimize_look_through(self.active_threats)
            print(f"Iteration {i+1}: Active Threats: {len(self.active_threats)}")
            print(f"Applying Look-Through -> PW: {pw:.2f}ms, Interval: {iv:.2f}ms")
            
            # Simulate real-time delay
            time.sleep(0.5)
            
            # Update threat distances
            for t in self.active_threats:
                t['distance'] -= (t['velocity'] * 0.5) / 1000 # Simplified
                if t['distance'] < 0:
                    self.active_threats.remove(t)
                    print(f"[TARGET NEUTRALIZED] ID: {t['id']}")

if __name__ == "__main__":
    sim = EWSimulator()
    sim.run_simulation(20)
