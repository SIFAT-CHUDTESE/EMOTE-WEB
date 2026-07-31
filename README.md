# ⚡ SIFAT FF Emote Bot

Free Fire emote sender bot with web UI. One-click deployable on **Render** or **Railway**.

---

## 🚀 Deploy in 1 Click

### Option A — Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` → click **Deploy**
5. Done ✅ — URL will be `https://ff-emote-api.onrender.com`

> **Region tip:** Select `Singapore` for best latency to BD/SEA FF servers.

---

### Option B — Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
3. Select the repo — Railway detects `Dockerfile` automatically
4. Click **Deploy** ✅

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `5000` | Web server port (set automatically by Render/Railway) |
| `SESSION_SECRET` | auto | Session secret (Render auto-generates) |

---

## 🐳 Local Docker Run

```bash
docker build -t ff-emote .
docker run -p 5000:5000 ff-emote
# Open http://localhost:5000
```

---

## 📁 Structure

```
main.py          — Flask API + bot TCP logic
templates/
  index.html     — Web UI
static/
  emotes/        — 486 emote PNG images
  emote_names.json — Real emote name database
Pb2/             — Protobuf definitions
xC4.py           — Crypto / packet helpers
xHeaders.py      — Header helpers
```
