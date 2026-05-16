# Mdundo Fraud Detection System - Vercel Deployment

Enterprise fraud detection system for Mdundo music platform. Analyzes charts across 7 African markets, identifies suspicious artists, and sends daily reports via Slack.

## 🎯 Features

- **Multi-Country Analysis**: Monitors Nigeria, Tanzania, Kenya, South Africa, Uganda, Ghana, and Cameroon
- **Real-time Fraud Scoring**: Analyzes artists against Spotify & Apple Music data
- **Automated Daily Reports**: Scheduled cron jobs with Slack notifications
- **Historical Tracking**: Stores results in Vercel KV for 90 days
- **Critical Alerts**: Instant Slack alerts for high-risk detections
- **REST API**: Query results programmatically

## 🚀 Quick Start

### Prerequisites

- GitHub account
- Vercel account (free tier)
- Slack workspace with admin access
- Spotify API credentials (free developer account)

### 1. Clone & Setup Repository

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/mdundo-fraud-detection.git
cd mdundo-fraud-detection

# Create local environment file
cp .env.example .env.local

# Install dependencies (local development)
pip install -r requirements.txt
```

### 2. Get API Credentials

#### Spotify API
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Get your Client ID and Client Secret
4. Create access token using Client Credentials flow
5. Save token to `SPOTIFY_TOKEN`

#### Slack Webhook
1. Go to [Slack App Directory](https://api.slack.com/apps)
2. Create New App → From scratch
3. Name it "Mdundo Fraud Detection"
4. Go to Incoming Webhooks → Add New Webhook
5. Select your channel
6. Copy webhook URL to `SLACK_WEBHOOK`

### 3. Deploy to Vercel

#### Option A: Web UI (Easiest)
1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project" → Import GitHub repository
4. Select your repo
5. Go to Settings → Environment Variables
6. Add:
   - `SPOTIFY_TOKEN` = your_token
   - `SLACK_WEBHOOK` = your_webhook
   - `CRON_SECRET` = random_secret
7. Click Deploy

#### Option B: CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Set environment variables
vercel env add SPOTIFY_TOKEN
vercel env add SLACK_WEBHOOK
vercel env add CRON_SECRET
```

### 4. Configure Cron Schedule

Edit `vercel.json` to change cron time:

```json
"crons": [{
  "path": "/api/functions/fraud_daily",
  "schedule": "0 7 * * *"  // 7 AM UTC daily
}]
```

Cron syntax: `minute hour dayOfMonth month dayOfWeek`
- `0 7 * * *` = Daily at 7:00 AM UTC
- `0 9 * * 1-5` = Weekdays at 9:00 AM UTC
- `30 8 * * 0` = Every Sunday at 8:30 AM UTC

## 📊 API Endpoints

### Daily Fraud Check (Cron)
```
POST /api/functions/fraud_daily
```
Triggered automatically by Vercel cron. Runs fraud detection across all countries.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2026-05-16T07:00:00Z",
  "summary": {
    "total_analyzed": 350,
    "total_critical": 5,
    "total_high": 12,
    "countries_processed": 7,
    "critical_alerts": 2
  },
  "countries": {
    "ng": {
      "total_analyzed": 50,
      "critical_risk": 2,
      "high_risk": 5,
      "medium_risk": 8,
      "low_risk": 15,
      "clean": 20
    }
  }
}
```

### Get Results
```
GET /api/results?country=ng[&days=30]
```

**Parameters:**
- `country`: Country code (ng, tz, ke, za, ug, gh, cm) - **required**
- `days`: Number of days of history (default: 1)

**Example:**
```bash
# Get today's results for Nigeria
curl https://your-project.vercel.app/api/results?country=ng

# Get 30 days of history
curl https://your-project.vercel.app/api/results?country=ng&days=30
```

**Response:**
```json
{
  "country": "NG",
  "results": [
    {
      "timestamp": "2026-05-16T07:00:00Z",
      "summary": {
        "total_analyzed": 50,
        "critical_risk": 2,
        "high_risk": 5
      },
      "artists": [
        {
          "rank": 1,
          "name": "Artist Name",
          "fraud_score": 75.5,
          "risk_level": "Critical",
          "flags": [
            "Not found on Spotify",
            "Top 10 position but only 5000 monthly listeners"
          ]
        }
      ]
    }
  ]
}
```

### System Status
```
GET /api/status
```

**Response:**
```json
{
  "status": "operational",
  "service": "Mdundo Fraud Detection",
  "version": "1.0.0",
  "timestamp": "2026-05-16T10:30:00Z"
}
```

## 📈 Fraud Risk Scoring

### Scoring Criteria

| Indicator | Risk Points | Threshold |
|-----------|------------|-----------|
| Not on Spotify | 30 | |
| Low followers (<10K) | 25 | |
| Position mismatch (top 10) | 35 | <20K listeners |
| Position mismatch (top 20) | 20 | <10K listeners |
| Not on Apple Music | 15 | |

### Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 0-10 | 🟢 Clean | No action |
| 10-30 | 🔵 Low Risk | Monitor |
| 30-50 | 🟡 Medium Risk | Watch closely |
| 50-70 | 🟠 High Risk | Investigate |
| 70+ | 🔴 Critical | Immediate action |

## 🔧 Local Development

### Run Locally
```bash
# Create .env.local with your credentials
python -m api.functions.fraud_daily

# Or test specific country
python -c "
import asyncio
from api.functions.fraud_daily import FraudDetectionJob
job = FraudDetectionJob()
asyncio.run(job.run())
"
```

### Testing
```bash
# Test Spotify API
python -c "
from lib.fraud_detector import MdundoFraudDetector
detector = MdundoFraudDetector(spotify_api_token='YOUR_TOKEN')
result = detector.check_spotify_artist('Wizkid')
print(result)
"

# Test scraper
python -c "
from lib.mdundo_scraper import MdundoScraper
scraper = MdundoScraper()
artists, error = scraper.scrape_chart('ng', limit=10)
print(f'Found {len(artists)} artists')
"
```

## 📁 Project Structure

```
fraud_detection_vercel/
├── api/
│   ├── functions/
│   │   └── fraud_daily.py      # Main cron handler
│   ├── status.py               # System status endpoint
│   └── results.py              # Results query endpoint
├── lib/
│   ├── fraud_detector.py       # Core detection logic
│   ├── mdundo_scraper.py       # Chart scraping
│   ├── slack_notifier.py       # Slack integration
│   └── kv_storage.py           # Vercel KV utilities
├── vercel.json                 # Vercel configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🔐 Security

### Environment Variables
Never commit `.env` files to GitHub. Use Vercel's environment variable management:

```bash
vercel env add SPOTIFY_TOKEN
vercel env add SLACK_WEBHOOK
vercel env add CRON_SECRET
```

### Cron Authentication (Optional)
Add header authentication to prevent unauthorized cron triggers:

```python
auth_header = request.headers.get('authorization', '')
if auth_header != f"Bearer {os.getenv('CRON_SECRET')}":
    return {"statusCode": 401}
```

## 💰 Costs

| Service | Cost | Notes |
|---------|------|-------|
| Vercel | Free | Includes serverless functions + cron |
| Vercel KV | Free | 3GB included (grows with usage) |
| Spotify API | Free | Developer tier |
| Slack | Free | Webhook integration |
| **Total** | **$0** | Completely free tier |

## 📊 Monitoring

### View Logs
```bash
# Vercel CLI
vercel logs

# Or via Vercel Dashboard
# Project → Deployments → Select deployment → Logs
```

### Set Up Alerts
1. Vercel Dashboard → Project → Monitoring
2. Add alert for function errors
3. Set notification channel (email)

## 🚨 Troubleshooting

### Cron Not Running
- Check Vercel Dashboard → Settings → Cron Jobs
- Verify environment variables are set
- Check function logs for errors

### Slack Messages Not Sending
- Verify `SLACK_WEBHOOK` is correct
- Check Slack workspace security settings
- Test webhook: `curl -X POST -H 'Content-type: application/json' --data '{"text":"Test"}' YOUR_WEBHOOK_URL`

### No Mdundo Data
- Scraper may be blocked by Mdundo rate limiting
- Add exponential backoff in `mdundo_scraper.py`
- Consider using proxy service

### Spotify API Errors
- Verify token is still valid (tokens expire)
- Check rate limit: max 180,000 requests per 15 minutes
- Implement caching to reduce API calls

## 🔄 Updating

### Pull Latest Changes
```bash
git pull origin main
git push origin main  # Triggers Vercel redeploy
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git commit -am "Update dependencies"
git push
```

## 📞 Support

For issues:
1. Check logs: `vercel logs`
2. Test locally: `python api/functions/fraud_daily.py`
3. Review error messages in Slack
4. Check GitHub issues

## 📄 License

MIT License - See LICENSE file

## 👤 Author

Mdundo Fraud Detection Team  
Chief Data Analyst & Chief Revenue Officer

---

**Last Updated:** 2026-05-16  
**Version:** 1.0.0  
**Status:** Production Ready
