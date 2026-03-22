const canvas = document.getElementById('spectrogramCanvas');
const ctx = canvas.getContext('2d');
const logContent = document.getElementById('logContent');
const pwEl = document.getElementById('pwValue');
const ivEl = document.getElementById('ivValue');
const velEl = document.getElementById('velValue');
const lossEl = document.getElementById('lossValue');

function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
}
window.addEventListener('resize', resize);
resize();

function addLog(msg, type = 'info') {
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    if (type === 'warning') entry.style.color = '#ffaa00';
    if (type === 'alert') entry.style.color = '#ff4444';
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    logContent.prepend(entry);
    
    // Log sayısını sınırla
    if (logContent.children.length > 50) {
        logContent.removeChild(logContent.lastChild);
    }
}

function draw() {
    ctx.fillStyle = '#0a0b10';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Grid (Siber Izgara)
    ctx.strokeStyle = 'rgba(0, 242, 255, 0.03)';
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 50) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 30) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }

    // Sinyal Akışı
    const time = Date.now() / 1000;
    ctx.shadowBlur = 10;
    ctx.shadowColor = 'rgba(0, 242, 255, 0.5)';
    
    for (let i = 0; i < 8; i++) {
        let x = (time * 50 + i * 150) % canvas.width;
        let opacity = Math.sin(time + i) * 0.5 + 0.5;
        ctx.fillStyle = `rgba(0, 242, 255, ${opacity})`;
        ctx.fillRect(x, 40, 2, canvas.height - 80);
        
        // Sinyal başlıkları (Blips)
        ctx.fillRect(x-5, 40, 10, 2);
        ctx.fillRect(x-5, canvas.height-42, 10, 2);
    }

    // Look-Through (Görsel Kararma)
    ctx.shadowBlur = 0;
    ctx.fillStyle = 'rgba(0, 10, 20, 0.85)';
    let ltWidth = 60;
    let ltX = (time * 120) % (canvas.width + ltWidth) - ltWidth;
    ctx.fillRect(ltX, 0, ltWidth, canvas.height);
    
    // LT Kenar Çizgileri
    ctx.strokeStyle = 'rgba(0, 242, 255, 0.2)';
    ctx.beginPath(); ctx.moveTo(ltX, 0); ctx.lineTo(ltX, canvas.height); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(ltX + ltWidth, 0); ctx.lineTo(ltX + ltWidth, canvas.height); ctx.stroke();

    requestAnimationFrame(draw);
}

let socket = null;
const connStatusEl = document.getElementById('connStatus');

function connect() {
    socket = new WebSocket('ws://localhost:8000/ws');
    
    socket.onopen = () => {
        addLog("Sunucu bağlantısı sağlandı. Gerçek zamanlı veriye geçiliyor.", "info");
        connStatusEl.textContent = "ÇEVRİMİÇİ (CANLI)";
        connStatusEl.className = "value online";
        if (simInterval) clearInterval(simInterval);
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        renderData(data);
    };

    socket.onclose = () => {
        addLog("Sunucu bağlantısı kesildi. Simülasyon moduna dönülüyor.", "warning");
        connStatusEl.textContent = "ÇEVRİMDIŞI (SİM)";
        connStatusEl.className = "value offline";
        startSimulation();
    };

    socket.onerror = () => {
        // Sessiz hata, simülasyon zaten çalışıyor olacak
    };
}

function renderData(data) {
    const { metrics, threats, log } = data;
    
    // Metrikler
    pwEl.textContent = metrics.pw + " ms";
    ivEl.textContent = metrics.iv + " ms";
    velEl.textContent = metrics.avg_vel + " m/s";
    lossEl.textContent = metrics.loss + " dB";

    // Tehdit Tablosu
    threatBody.innerHTML = '';
    threats.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${t.id}</td>
            <td class="t-type ${t.type === 'FireControl' ? 'fire-control' : ''}">${t.type}</td>
            <td>${t.distance.toFixed(1)} km</td>
            <td>${t.velocity.toFixed(0)} m/s</td>
        `;
        threatBody.appendChild(tr);
    });

    if (log) addLog(log, 'info');
}

// Fallback Simülasyonu (Orijinal Mantık)
let simInterval = null;
function startSimulation() {
    if (simInterval) clearInterval(simInterval);
    simInterval = setInterval(updateThreatsManual, 2000);
}

function updateThreatsManual() {
    const types = ["Search", "SAR", "FireControl", "TargetTrack"];
    const count = Math.floor(Math.random() * 4) + 1;
    let threats = [];
    let totalVel = 0;
    
    for (let i = 0; i < count; i++) {
        const vel = 200 + Math.random() * 600;
        totalVel += vel;
        threats.push({
            id: 1000 + Math.floor(Math.random() * 9000),
            type: types[Math.floor(Math.random() * types.length)],
            distance: 50 + Math.random() * 150,
            velocity: vel
        });
    }

    renderData({
        metrics: {
            pw: (15 + (count * 5) + Math.random() * 5).toFixed(1),
            iv: (250 - (totalVel / count / 10) + Math.random() * 20).toFixed(1),
            avg_vel: (totalVel / count).toFixed(0),
            loss: (120 + Math.random() * 15).toFixed(1)
        },
        threats: threats
    });
}

// Başlangıç
draw();
startSimulation();
setTimeout(connect, 1000); // Sunucuya bağlanmayı dene

addLog("Sistem senkronizasyonu tamamlandı.");
addLog("Fiziksel sinyal modelleri aktif.");
