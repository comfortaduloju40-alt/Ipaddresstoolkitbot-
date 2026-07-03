# 🌐 IP Address Toolkit Bot (@Ipaddresstoolkitbot)

An enterprise-ready, asynchronous Telegram bot built with **Python 3.12**, **python-telegram-bot v21+**, and **FastAPI** to retrieve telemetry, geolocation data, and cyber intelligence profiling fields for IPv4 and IPv6 addresses. Fully optimized for instant deployment onto **Render.com**.

## ✨ Features

- **Asynchronous Lifespan Architecture:** Built entirely on top of high-concurrency loops (`FastAPI` + `uvicorn` + `httpx`).
- **Production Webhook Framework:** Avoids high-latency polling by registering persistent webhooks with auto-initialization hooks on startup.
- **Provider Agnostic Extensibility:** Easily swap underlying data vendors (e.g., ip-api, IPinfo, MaxMind) by editing a single decoupled module file (`ip_lookup.py`).
- **Comprehensive Geolocation Mapping:** Tracks Country flags, ISP, ASN structures, Region data, Currency parameters, and physical coordinates.
- **Threat Vector Intelligence Checks:** Scans endpoints automatically for active proxies, VPN routes, or Tor exit relay systems.

---

## 🛠️ Step-by-Step Configuration & Local Setup

### 1. Generate Your Bot Token from Telegram
1. Open your Telegram client, search for [@BotFather](https://t.me/BotFather), and initiate a chat conversation loop.
2. Execute the `/newbot` command parameters.
3. Assign a public name (`IP Address Toolkit Bot`) and a unique username handle (e.g., `@Ipaddresstoolkitbot`).
4. Securely copy the generated HTTP API access token (`BOT_TOKEN`).

### 2. Configure the Source Environment Locally
Clone this codebase structure to your working desktop system and construct an insulated virtual development environment:

```bash
# Clone the repository structure
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
cd YOUR_REPOSITORY

# Initialize a clean environment block
python -m venv venv
source venv/bin/activate  # On Windows, execute: venv\Scripts\activate

# Install application project dependencies 
pip install -r requirements.txt

# Replicate and complete configuration variables
cp .env.example .env
