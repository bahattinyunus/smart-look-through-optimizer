const canvas = document.getElementById('spectrogramCanvas');
const ctx = canvas.getContext('2d');
const logContent = document.getElementById('logContent');
const pwEl = document.getElementById('pwValue');
const ivEl = document.getElementById('ivValue');
const velEl = document.getElementById('velValue');

function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
}
window.addEventListener('resize', resize);
resize();

function addLog(msg) {
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    logContent.prepend(entry);
}

function draw() {
    ctx.fillStyle = '#0a0b10';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Izgara Çizimi
    ctx.strokeStyle = 'rgba(0, 242, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 50) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 30) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }

    // Sinyal Darbe Simülasyonu
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#00f2ff';
    ctx.fillStyle = '#00f2ff';
    
    for (let i = 0; i < 5; i++) {
        let x = (Date.now() / 10 + i * 200) % canvas.width;
        ctx.fillRect(x, 50, 10, canvas.height - 100);
    }

    // Look-Through Katmanı (Karartılmış çubuklar)
    ctx.shadowBlur = 0;
    ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
    let ltX = (Date.now() / 5) % canvas.width;
    ctx.fillRect(ltX, 0, 40, canvas.height);

    requestAnimationFrame(draw);
}

// Adaptif güncelleme simülasyonu
setInterval(() => {
    const pw = (10 + Math.random() * 5).toFixed(1);
    const iv = (300 + Math.random() * 50).toFixed(1);
    const vel = (400 + Math.random() * 100).toFixed(0);
    
    pwEl.textContent = pw + " ms";
    ivEl.textContent = iv + " ms";
    velEl.textContent = vel + " m/s";

    if (Math.random() > 0.8) {
        addLog(`Optimizasyon Yeniden Hesaplandı: PW=${pw}`);
    }
}, 2000);

draw();
addLog("Başlatma tamamlandı. Tehdit girişi bekleniyor.");
