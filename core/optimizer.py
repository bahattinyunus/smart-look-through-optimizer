import numpy as np
from q_learning import QLearningAgent

class LookThroughOptimizer:
    """
    SLT-X Akıllı Look-Through Optimizasyon Motoru.
    
    Bu motor, karmaşık EH ortamlarında radar tehditlerini analiz ederek
    jammer yayınındaki LT (Look-Through) pencerelerini optimize eder.
    """
    def __init__(self, radar_freq=5.0e9, modulation="LFM"):
        self.radar_freq = radar_freq
        self.modulation = modulation
        self.noise_floor = -110 # dBm
        self.jammer_power = 40 # dBm (EIRP)
        self.jamming_margin = 10 # dB
        self.agent = QLearningAgent()
        self.last_state = 0
        self.last_action = 0
        
    def calculate_path_loss(self, distance_km):
        """Friis bazlı log-mesafe yol kaybı modeli."""
        return 20 * np.log10(distance_km) + 20 * np.log10(self.radar_freq) - 147.55
        
    def calculate_snr(self, distance_km, jammer_active=True):
        """Efektif Sinyal-Gürültü Oranı hesaplaması."""
        path_loss = self.calculate_path_loss(max(0.1, distance_km))
        signal_power = 60 - path_loss # Varsayılan hedef gücü
        
        if jammer_active:
            # Karıştırıcı etkisindeki gürültü artışı
            total_noise = self.noise_floor + self.jammer_power - path_loss + self.jamming_margin
        else:
            total_noise = self.noise_floor
            
        return signal_power - total_noise

    def optimize_look_through(self, current_threats):
        """
        Gelişmiş adaptif ölçeklendirme algoritması (Önceliklendirme Destekli).
        
        Tehdit sayısı, hızı ve türüne göre PW ve RI değerlerini optimize eder.
        """
        threat_count = len(current_threats)
        if threat_count == 0:
            return 10.0, 500.0
        
        # Tehdit önceliklendirme
        # FireControl (Atış Kontrol) -> Yüksek Öncelik
        # SAR/Search -> Orta/Düşük Öncelik
        high_priority_detected = any(t.get('type') == 'FireControl' for t in current_threats)
        
        velocities = [t.get('velocity', 300) for t in current_threats]
        avg_velocity = np.mean(velocities)
        
        # Heuristic base values
        pulse_width = np.clip(10 + (threat_count * 5), 10, 60)
        interval = np.clip(1000 / (avg_velocity / 100 + 1), 50, 400)
        
        # AI-Steering
        state = self.agent.get_state(threat_count)
        action = self.agent.choose_action(state)
        
        # Apply AI action modifiers
        if action == 0: interval *= 0.8  # Shorten RI
        if action == 1: interval *= 1.2  # Longen RI
        if action == 2: pulse_width *= 0.8 # Shrink PW
        if action == 3: pulse_width *= 1.2 # Expand PW
        
        # Learning step (Simple reward feedback based on SNR estimate at average distance)
        avg_dist = np.mean([t.get('distance', 100) for t in current_threats]) if current_threats else 100
        current_snr = self.calculate_snr(avg_dist)
        reward = self.agent.get_reward(current_snr, interval, threat_count)
        self.agent.learn(self.last_state, self.last_action, reward, state)
        
        self.last_state = state
        self.last_action = action

        # Security clamps
        return float(np.clip(pulse_width, 5, 100)), float(np.clip(interval, 20, 800))

if __name__ == "__main__":
    opt = LookThroughOptimizer()
    # Simüle edilmiş tehdit verisi
    test_threats = [
        {"velocity": 750, "type": "SAR"}, 
        {"velocity": 400, "type": "FireControl"}
    ]
    pw, iv = opt.optimize_look_through(test_threats)
    print(f"[OPTIMIZASYON] LT Genişliği: {pw}ms, LT Tekrarı: {iv:.2f}ms")
