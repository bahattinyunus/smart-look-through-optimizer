import asyncio
import json
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from core.optimizer import LookThroughOptimizer
from core.simulator import EWSimulator

app = FastAPI()

# Enable CORS for local GUI development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RealTimeSimulator(EWSimulator):
    """WebSocket üzerinden veri yayını yapabilen genişletilmiş simülatör."""
    def __init__(self):
        super().__init__()
        
    async def stream_data(self, websocket: WebSocket):
        print("[SERVER] İstemci bağlandı, yayın başlatılıyor...")
        try:
            while True:
                # Rastgele tehdit oluşturma (Simulator logic)
                if random.random() > 0.8:
                    self.spawn_threat()
                
                # Optimizasyon
                pw, iv = self.optimizer.optimize_look_through(self.active_threats)
                
                # Tehditleri güncelle
                for t in self.active_threats[:]:
                    t['distance'] -= (t['velocity'] * 0.5) / 1000
                    if t['distance'] < 0:
                        self.active_threats.remove(t)
                
                # Veriyi paketle
                payload = {
                    "metrics": {
                        "pw": round(pw, 2),
                        "iv": round(iv, 2),
                        "avg_vel": round(sum(t['velocity'] for t in self.active_threats)/len(self.active_threats), 1) if self.active_threats else 0,
                        "loss": round(120 + random.uniform(0, 10), 1) # Demo placeholder
                    },
                    "threats": self.active_threats,
                    "log": f"Yeni Optimizasyon: PW={pw:.1f}ms, IV={iv:.1f}ms" if random.random() > 0.7 else None
                }
                
                await websocket.send_text(json.dumps(payload))
                await asyncio.sleep(0.5) # 2 Hz update rate
        except Exception as e:
            print(f"[SERVER] Bağlantı kesildi: {e}")

sim = RealTimeSimulator()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await sim.stream_data(websocket)

@app.get("/status")
async def get_status():
    return {"status": "online", "engine": "SLT-X AI v4.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
