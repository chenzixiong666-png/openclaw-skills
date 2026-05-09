#!/usr/bin/env node
// 用 Base64 直接上传本地图片到 SwitchBot 画框
const crypto = require('crypto');
const https = require('https');
const fs = require('fs');

const token = process.env.SWITCHBOT_TOKEN;
const secret = process.env.SWITCHBOT_SECRET;
const imageFile = 'C:\\Users\\woan\\.openclaw\\media\\inbound\\fb6d278a-6db8-4d93-808b-1a4027e04f1a.jpg';
const frames = ['B0E9FE7A1A77', 'B0E9FEB3F9A7', 'B0E9FEA8B080'];

if (!token || !secret) {
  console.error('Missing SWITCHBOT_TOKEN or SWITCHBOT_SECRET');
  process.exit(1);
}

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

async function uploadToFrames() {
  try {
    // 读取本地图片
    const imageBuffer = fs.readFileSync(imageFile);
    const imageBase64 = imageBuffer.toString('base64');

    console.log(`📸 图片已加载: ${imageFile}`);
    console.log(`📊 原始大小: ${imageBuffer.length} 字节`);
    console.log(`🔤 Base64 长度: ${imageBase64.length} 字符\n`);

    // 尝试上传到各画框
    for (const frameId of frames) {
      console.log(`⬆️  上传到画框 ${frameId}...`);
      try {
        // 正确的参数格式：{"imageBase64":"..."}
        const body = {
          commandType: 'command',
          command: 'uploadImage',
          parameter: { imageBase64: imageBase64 }
        };
        const resp = await request('POST', `/v1.1/devices/${frameId}/commands`, body);
        const status = resp.statusCode === 100 ? '✅' : '❌';
        console.log(`   ${status} 状态码: ${resp.statusCode}, 消息: ${resp.message}\n`);
      } catch (e) {
        console.error(`   ❌ 错误: ${e.message}\n`);
      }
    }
  } catch (e) {
    console.error('Fatal error:', e.message);
    process.exit(1);
  }
}

uploadToFrames();
