import numpy as np

class LookThroughOptimizer:
    """
    Akıllı Look-Through (LT) Optimizasyon Sınıfı.
    Elektronik Harp ortamında hedef izleme ve karıştırma arasındaki dengeyi yönetir.
    """
    def __init__(self, radar_freq=5.0e9, modulation="LFM"):
        self.radar_freq = radar_freq
        self.modulation = modulation
        self.noise_floor = -110 # dBm (Gürültü Tabanı)
        self.jammer_power = 40 # dBm (Karıştırıcı Gücü)
        
    def calculate_snr(self, distance, jammer_active=True):
        """
        Sinyal-Gürültü Oranı (SNR) Hesaplama.
        Mesafe ve karıştırıcı durumuna göre hedef sinyal gücünü belirler.
        """
        # Basitleştirilmiş yol kaybı (Path Loss) hesaplaması
        path_loss = 20 * np.log10(distance) + 20 * np.log10(self.radar_freq) - 147.55
        signal_power = 60 - path_loss # Varsayılan 60 dBm EIRP
        
        if jammer_active:
            total_noise = self.noise_floor + self.jammer_power - path_loss + 10 # Karıştırma marjı
        else:
            total_noise = self.noise_floor
            
        return signal_power - total_noise

    def optimize_look_through(self, current_threats):
        """
        Tehdit seviyesine göre Look-Through penceresini optimize eder.
        Geri dönüş: pulse_width (PW - ms) ve interval (Tekrar Aralığı - ms).
        """
        # Adaptif Mantık: SNR ve tehdit hızına göre LT pencerelerini daraltır veya genişletir.
        # Yüksek risk -> daha sık ölçüm (kısa aralık), daha uzun ölçüm (geniş PW)
        
        threat_count = len(current_threats)
        if threat_count == 0:
            return 10, 500 # Varsayılan pasif ölçüm: 500ms'de bir 10ms
        
        avg_velocity = np.mean([t['velocity'] for t in current_threats])
        
        # Sezgisel optimizasyon formülü
        pulse_width = np.clip(5 + (threat_count * 2), 5, 50)
        interval = np.clip(1000 / (avg_velocity + 1), 50, 500)
        
        return pulse_width, interval

if __name__ == "__main__":
    opt = LookThroughOptimizer()
    tehditler = [{"velocity": 300}, {"velocity": 450}]
    pw, iv = opt.optimize_look_through(tehditler)
    print(f"Optimal Look-Through Penceresi: {pw}ms, Her {iv:.2f}ms'de bir")
