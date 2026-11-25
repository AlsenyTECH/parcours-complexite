// Capture tuto.html image par image.
//   node capturer_tuto.js plan.json sortie.mp4            → la vidéo (muette)
//   node capturer_tuto.js plan.json dossier --images 3,8  → des PNG aux instants donnés (contrôle)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const plan = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => { console.error('ERREUR PAGE', e.message); process.exitCode = 1; });
  await p.goto('file://' + path.join(__dirname, 'tuto.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(s => charger(s), plan);
  const i = process.argv.indexOf('--images');
  if (i > 0) {
    const ts = process.argv[i + 1].split(',').map(Number);
    fs.mkdirSync(process.argv[3], { recursive: true });
    for (const t of ts) {
      await p.evaluate(t => rendre(t), t);
      await p.screenshot({ path: path.join(process.argv[3], 't' + String(t.toFixed(1)).padStart(6, '0') + '.png') });
    }
    await b.close(); return;
  }
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(plan.ips), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-tune', 'stillimage', '-pix_fmt', 'yuv420p', '-r', String(plan.ips), process.argv[3]],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.ceil(plan.total * plan.ips);
  for (let k = 0; k < n; k++) {
    await p.evaluate(t => rendre(t), k / plan.ips);
    const img = await p.screenshot({ type: 'jpeg', quality: 88 });
    if (!ff.stdin.write(img)) await new Promise(r => ff.stdin.once('drain', r));
    if (k % 1200 === 0) console.log('  image', k, '/', n);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
