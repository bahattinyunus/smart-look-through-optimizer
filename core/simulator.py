import time
import random
from optimizer import LookThroughOptimizer

class EWSimulator:
    """
    Elektronik Harp (EH) Simülatörü.
    Sentetik tehditler oluşturur ve optimizasyon motorunun tepkilerini test eder.
    """
    def __init__(self):
        self.optimizer = LookThroughOptimizer()
        self.active_threats = [] # Aktif tehdit listesi
        self.running = True

    def spawn_threat(self):
        """Yeni bir radar tehdidi oluşturur."""
        threat = {
            "id": random.randint(1000, 9999),
            "velocity": random.uniform(200, 800), # m/s
            "distance": random.uniform(50, 200) # km
        }
        self.active_threats.append(threat)
        print(f"[TEHDİT TESPİT EDİLDİ] Kimlik: {threat['id']}, Hız: {threat['velocity']:.2f} m/s")

    def run_simulation(self, iterations=10):
        """Simülasyon döngüsünü başlatır."""
        print("--- Akıllı Look-Through Simülasyonu Başlatıldı ---")
        for i in range(iterations):
            if random.random() > 0.7:
                self.spawn_threat()
            
            pw, iv = self.optimizer.optimize_look_through(self.active_threats)
            print(f"İterasyon {i+1}: Aktif Tehdit Sayısı: {len(self.active_threats)}")
            print(f"Uygulanan Look-Through -> PW: {pw:.2f}ms, Aralık: {iv:.2f}ms")
            
            # Gerçek zamanlı gecikme simülasyonu
            time.sleep(0.5)
            
            # Tehdit mesafelerini güncelle
            for t in self.active_threats:
                t['distance'] -= (t['velocity'] * 0.5) / 1000 # Basit mesafe düşümü
                if t['distance'] < 0:
                    self.active_threats.remove(t)
                    print(f"[HEDEF ETKİSİZ HALE GETİRİLDİ] Kimlik: {t['id']}")

if __name__ == "__main__":
    sim = EWSimulator()
    sim.run_simulation(20)
