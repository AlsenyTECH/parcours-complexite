// Capture page.html image par image et l'envoie à ffmpeg : node capturer.js plan.json sortie.mp4
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const plan = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(plan.ips), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '26', '-tune', 'stillimage', '-pix_fmt', 'yuv420p', '-r', String(plan.ips), process.argv[3]],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'page.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(s => charger(s), plan.scenes);
  const n = Math.ceil(plan.total * plan.ips);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => afficher(t), i / plan.ips);
    const img = await p.screenshot({ type: 'jpeg', quality: 88 });
    if (!ff.stdin.write(img)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
