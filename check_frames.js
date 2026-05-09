#!/usr/bin/env node
const crypto = require('crypto');
const https = require('https');

const token = process.env.SWITCHBOT_TOKEN;
const secret = process.env.SWITCHBOT_SECRET;

function headers() {
  const t = Date.now().toString();
  const nonce = crypto.randomUUID();
  const sign = crypto
    .createHmac('sha256', secret)
    .update(token + t + nonce)
    .digest('base64');
  return {
    'Content-Type': 'application/json; charset=utf8',
    'Authorization': token,
    't': t,
    'nonce': nonce,
    'sign': sign,
    'src': 'OpenClaw',
  };
}

function request(method, path, body) {
  const data = body ? JSON.stringify(body) : undefined;
  const opts = new URL('https://api.switch-bot.com' + path);
  return new Promise((resolve, reject) => {
    const req = https.request({
      method,
      hostname: opts.hostname,
      path: opts.pathname + (opts.search || ''),
      headers: { ...headers(), ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}) },
    }, (res) => {
      let buf = '';
      res.on('data', (c) => (buf += c));
      res.on('end', () => {
        try { resolve(buf ? JSON.parse(buf) : {}); }
        catch { resolve(buf); }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function main() {
  try {
    const resp = await request('GET', '/v1.1/devices');
    const deviceList = resp.body?.deviceList || [];
    
    const frames = deviceList.filter(d => d.deviceType === 'AI Art Frame');
    
    console.log(`\n📊 AI Art Frame 设备总数: ${frames.length}\n`);
    
    frames.forEach((frame, idx) => {
      console.log(`${idx + 1}. ${frame.deviceName} (${frame.deviceId})`);
      console.log(`   类型: ${frame.deviceType}`);
      console.log(`   云服务: ${frame.enableCloudService ? '✅ 已启用' : '❌ 未启用'}`);
      console.log(`   所属家庭: ${frame.familyName || '未分配'}\n`);
    });
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

main();
