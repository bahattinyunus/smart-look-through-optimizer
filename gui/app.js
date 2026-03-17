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

// Dinamik Veri Simülasyonu
setInterval(() => {
    const pw = (15 + Math.random() * 10).toFixed(1);
    const iv = (250 + Math.random() * 100).toFixed(1);
    const vel = (300 + Math.random() * 400).toFixed(0);
    const loss = (120 + Math.random() * 15).toFixed(1);
    
    pwEl.textContent = pw + " ms";
    ivEl.textContent = iv + " ms";
    velEl.textContent = vel + " m/s";
    lossEl.textContent = loss + " dB";

    if (Math.random() > 0.9) {
        addLog(`Adaptif PW Güncellemesi: ${pw}ms`, 'info');
    }
    if (vel > 650) {
        addLog(`KRİTİK TEHDİT: Hız Sınırı Aşıldı (${vel} m/s)`, 'alert');
    }
}, 1500);

draw();
addLog("Sistem senkronizasyonu tamamlandı.");
addLog("Fiziksel sinyal modelleri aktif.");
