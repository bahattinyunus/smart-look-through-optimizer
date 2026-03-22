import numpy as np
import random
import json
import os

class QLearningAgent:
    """
    Look-Through optimizasyonu için hafızasız Q-Learning ajanı.
    Zamanlama (RI) ve Genişlik (PW) parametrelerini optimize etmeyi öğrenir.
    """
    def __init__(self, n_actions=4, n_states=10, learning_rate=0.1, discount_factor=0.9, epsilon=0.2):
        self.n_actions = n_actions # [Shorten RI, Longen RI, Shrink PW, Expand PW]
        self.n_states = n_states   # Tehdit yoğunluk seviyeleri (0-9)
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.model_path = os.path.join(os.path.dirname(__file__), "q_table.json")
        
        # Q-Tablosu: [Durum, Aksiyon]
        self.q_table = np.zeros((n_states, n_actions))
        self.load_model()

    def get_state(self, threat_count):
        """Tehdit sayısını 0-9 arası bir duruma normalize eder."""
        return min(self.n_states - 1, threat_count)

    def choose_action(self, state):
        """Epsilon-greedy stratejisi ile aksiyon seçimi."""
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return np.argmax(self.q_table[state])

    def learn(self, state, action, reward, next_state):
        """Bellman denklemi ile Q değerlerini günceller."""
        predict = self.q_table[state, action]
        target = reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state, action] += self.lr * (target - predict)

    def get_reward(self, snr, interval, threat_count):
        """
        Ödül Fonksiyonu:
        - SNR çok yüksekse (tespit riski) -> Negatif Ödül
        - Interval çok genişse (tracking kaybı) -> Negatif Ödül
        - Düşük Interval ve Güvenli SNR -> Pozitif Ödül
        """
        reward = 0
        if snr > 15: reward -= 5   # Çok yüksek SNR = Yakalanma riski
        if interval > 400: reward -= 2 # Çok seyrek LT = İz kaybı
        if snr < 10 and interval < 300: reward += 10 # Verimli EH
        
        return reward

    def save_model(self):
        """Q-tablosunu JSON olarak kaydeder."""
        try:
            with open(self.model_path, "w") as f:
                json.dump(self.q_table.tolist(), f)
            # print(f"[AI] Model kaydedildi: {self.model_path}")
        except Exception as e:
            print(f"[AI] Kayıt hatası: {e}")

    def load_model(self):
        """Q-tablosunu JSON'dan yükler."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "r") as f:
                    data = json.load(f)
                    self.q_table = np.array(data)
                print(f"[AI] Mevcut model yüklendi: {self.model_path}")
            except Exception as e:
                print(f"[AI] Yükleme hatası: {e}")
