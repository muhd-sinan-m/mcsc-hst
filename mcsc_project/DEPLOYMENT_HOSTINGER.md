# Hostinger Docker & Custom Domain Deployment Guide

This guide provides step-by-step instructions to deploy the dockerized **MCSC Portal** application onto Hostinger VPS with a **Custom Domain** and SSL certificate.

---

## 1. Prerequisites

1. Hostinger VPS (or Hostinger Docker Hosting) with root SSH access.
2. A custom domain purchased or managed on Hostinger (or external DNS like Cloudflare/Namecheap).
3. Docker & Docker Compose installed on the host VPS:
   ```bash
   # Quick installation script for Ubuntu/Debian VPS
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

---

## 2. Hostinger DNS & Custom Domain Setup

Before running the application, point your custom domain to your Hostinger VPS IP:

1. **Find your VPS IP**: Log in to **Hostinger hPanel** → **VPS** → Copy your Server **IPv4 Address** (e.g. `185.xxx.xxx.xxx`).
2. **Configure DNS Records** in Hostinger DNS Manager (or your domain registrar):
   - **Type A Record**:
     - `Name`: `@` (or leave empty)
     - `Points to`: `YOUR_HOSTINGER_VPS_IP`
     - `TTL`: `3600`
   - **Type A Record** (for www subdomain):
     - `Name`: `www`
     - `Points to`: `YOUR_HOSTINGER_VPS_IP`
     - `TTL`: `3600`

---

## 3. Server Deployment & Environment Setup

### Step 1: Upload / Clone your Project
SSH into your Hostinger VPS and clone your repository:
```bash
git clone <your-repository-url> mcsc_project
cd mcsc_project
```

### Step 2: Configure Environment Variables for Custom Domain
Copy `.env.example` to `.env` and set your custom domain:
```bash
cp .env.example .env
nano .env
```

Configure your custom domain in `.env`:
```env
DEBUG=False
SECRET_KEY=generate-a-secure-random-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,YOUR_VPS_IP

# Database (Supabase PostgreSQL pooler or Hostinger Postgres)
DATABASE_URL=postgres://user:password@db-host:5432/dbname

# Resend Email with Custom Domain
RESEND_API_KEY=re_123456789...
RESEND_FROM_EMAIL=MCSC Portal <noreply@yourdomain.com>
```

### Step 3: Build and Start Containers
Launch the application:
```bash
docker compose up -d --build
```

Verify that the container is running:
```bash
docker compose ps
docker compose logs -f web
```

---

## 4. Nginx Reverse Proxy & Free SSL (HTTPS)

To expose your application on standard ports (`80` for HTTP and `443` for HTTPS) with your custom domain:

### Step 1: Install Nginx & Certbot
```bash
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx
```

### Step 2: Create Nginx Site Configuration
Create `/etc/nginx/sites-available/mcsc`:
```bash
sudo nano /etc/nginx/sites-available/mcsc
```

Paste the following configuration (replace `yourdomain.com` with your actual domain):
```nginx
server {
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 25M;
}
```

### Step 3: Enable Nginx & Issue SSL Certificate
```bash
# Enable site config
sudo ln -s /etc/nginx/sites-available/mcsc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Issue free SSL certificate via Let's Encrypt / Certbot
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot will automatically configure HTTPS redirect and SSL certificates for your custom domain!

---

## 5. Resend Custom Domain Verification (Optional but Recommended)

If using Resend to send emails from your custom domain (`noreply@yourdomain.com`):
1. Go to **Resend Dashboard** → **Domains** → **Add Domain** (`yourdomain.com`).
2. Add the provided **DKIM**, **SPF**, and **DMARC** DNS records into your **Hostinger DNS Manager**.
3. Once verified in Resend, set `RESEND_FROM_EMAIL=MCSC Council <noreply@yourdomain.com>` in `.env`.

---

## 6. Useful Commands

| Action | Command |
| --- | --- |
| **Start Containers** | `docker compose up -d` |
| **Stop Containers** | `docker compose down` |
| **Rebuild & Restart** | `docker compose up -d --build` |
| **View Live Logs** | `docker compose logs -f web` |
| **Create Django Superuser** | `docker compose exec web python manage.py createsuperuser` |
| **Check Nginx Status** | `sudo systemctl status nginx` |
