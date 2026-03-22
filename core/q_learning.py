import numpy as np
import random

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
        
        # Q-Tablosu: [Durum, Aksiyon]
        self.q_table = np.zeros((n_states, n_actions))

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
