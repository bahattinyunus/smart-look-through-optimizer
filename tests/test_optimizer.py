import unittest
import numpy as np
from core.optimizer import LookThroughOptimizer

class TestLookThroughOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = LookThroughOptimizer()

    def test_path_loss_calculation(self):
        # 100km mesafede yaklaşık 146dB bekliyoruz (5GHz için)
        loss = self.optimizer.calculate_path_loss(100)
        self.assertGreater(loss, 140)
        self.assertLess(loss, 160)

    def test_snr_jammer_on_off(self):
        dist = 50
        snr_on = self.optimizer.calculate_snr(dist, jammer_active=True)
        snr_off = self.optimizer.calculate_snr(dist, jammer_active=False)
        
        # Jammer aktifken SNR daha düşük olmalı
        self.assertLess(snr_on, snr_off)

    def test_optimization_logic(self):
        # Hiç tehdit yoksa varsayılan değerler
        pw, iv = self.optimizer.optimize_look_through([])
        self.assertEqual(pw, 10.0)
        self.assertEqual(iv, 500.0)

        # Çok sayıda ve hızlı tehdit varsa
        threats = [
            {"velocity": 800, "type": "FireControl", "distance": 20},
            {"velocity": 700, "type": "TargetTrack", "distance": 15}
        ]
        pw2, iv2 = self.optimizer.optimize_look_through(threats)
        
        # Hızlı ve çok tehdit varken interval kısalmalı
        self.assertLess(iv2, 500.0)

    def test_ai_learning_bounds(self):
        threats = [{"velocity": 300, "type": "Search", "distance": 100}]
        # Çok sayıda iterasyonda patlama/çatlama kontrolü
        for _ in range(100):
            pw, iv = self.optimizer.optimize_look_through(threats)
            self.assertGreaterEqual(pw, 5.0)
            self.assertLessEqual(pw, 100.0)
            self.assertGreaterEqual(iv, 20.0)

if __name__ == '__main__':
    unittest.main()
