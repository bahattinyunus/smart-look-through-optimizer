import numpy as np

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
        
        # Temel PW ve Interval hesaplama
        pulse_width = np.clip(10 + (threat_count * 5), 10, 60)
        interval = np.clip(1000 / (avg_velocity / 100 + 1), 50, 400)
        
        # Öncelik tabanlı agresiflik ayarı
        if high_priority_detected:
            # Atış kontrol radarı varsa, tespit olasılığını artırmak için:
            # - LT aralığını ciddi şekilde daralt (sık örnekleme)
            # - LT genişliğini (PW) biraz artır
            interval = max(30, interval * 0.5)
            pulse_width = min(70, pulse_width * 1.2)
            
        elif avg_velocity > 600:
            interval = max(50, interval * 0.8)
            
        return float(pulse_width), float(interval)

if __name__ == "__main__":
    opt = LookThroughOptimizer()
    # Simüle edilmiş tehdit verisi
    test_threats = [
        {"velocity": 750, "type": "SAR"}, 
        {"velocity": 400, "type": "FireControl"}
    ]
    pw, iv = opt.optimize_look_through(test_threats)
    print(f"[OPTIMIZASYON] LT Genişliği: {pw}ms, LT Tekrarı: {iv:.2f}ms")
