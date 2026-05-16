# Quick Reference Guide

## 📋 Common Commands

### Local Development
```bash
# Setup
bash setup.sh
source venv/bin/activate

# Test
python api/functions/fraud_daily.py

# Check status
curl http://localhost:3000/api/status
```

### GitHub
```bash
# Push changes
git add .
git commit -m "Your message"
git push origin main

# Create new branch
git checkout -b feature/name

# Pull latest
git pull origin main
```

### Vercel
```bash
# View logs
vercel logs project-name --follow

# Deploy
git push origin main  # Auto-deploys via GitHub

# Set env vars
vercel env add SPOTIFY_TOKEN
```

## 🔌 API Quick Calls

### Status
```bash
curl https://your-project.vercel.app/api/status
```

### Get Results
```bash
# Today's Nigeria results
curl https://your-project.vercel.app/api/results?country=ng

# 30 days history
curl https://your-project.vercel.app/api/results?country=ng&days=30

# Other countries
# tz, ke, za, ug, gh, cm
```

### Trigger Cron Manually
```bash
curl -X POST https://your-project.vercel.app/api/functions/fraud_daily \
  -H "Authorization: Bearer YOUR_CRON_SECRET"
```

## 📊 Fraud Risk Levels

| Score | Level | Icon | Action |
|-------|-------|------|--------|
| 0-10 | Clean | 🟢 | OK |
| 10-30 | Low | 🔵 | Monitor |
| 30-50 | Medium | 🟡 | Watch |
| 50-70 | High | 🟠 | Investigate |
| 70+ | Critical | 🔴 | Act now |

## 🌍 Countries

| Code | Country | Shorthand |
|------|---------|-----------|
| ng | Nigeria | NG |
| tz | Tanzania | TZ |
| ke | Kenya | KE |
| za | South Africa | ZA |
| ug | Uganda | UG |
| gh | Ghana | GH |
| cm | Cameroon | CM |

## 🔑 Environment Variables

| Variable | Purpose | Where to Get |
|----------|---------|--------------|
| SPOTIFY_TOKEN | Artist data lookup | Spotify Dev Dashboard |
| SLACK_WEBHOOK | Fraud alerts | Slack API Dashboard |
| CRON_SECRET | Job authentication | Generate random hex |

## 📁 Project Structure

```
fraud_detection_vercel/
├── api/                    # Vercel serverless functions
│   ├── functions/
│   │   └── fraud_daily.py # Main cron job
│   ├── status.py          # Health check
│   └── results.py         # Query results
├── lib/                    # Core modules
│   ├── fraud_detector.py  # Detection engine
│   ├── mdundo_scraper.py  # Web scraper
│   ├── slack_notifier.py  # Notifications
│   └── kv_storage.py      # Data storage
├── vercel.json            # Vercel config
├── requirements.txt       # Python deps
└── README.md             # Full docs
```

## 🔍 Debugging

### Check Logs
```bash
# Vercel Dashboard → Deployments → Select → Functions → fraud_daily
# Or CLI:
vercel logs
```

### Test Slack
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"test"}' \
  YOUR_SLACK_WEBHOOK_URL
```

### Test Spotify
```python
from lib.fraud_detector import MdundoFraudDetector
detector = MdundoFraudDetector(spotify_api_token='TOKEN')
result = detector.check_spotify_artist('Wizkid')
print(result)
```

### Test Scraper
```python
from lib.mdundo_scraper import MdundoScraper
scraper = MdundoScraper()
artists, error = scraper.scrape_chart('ng')
print(f'Found {len(artists)} artists')
```

## ⚙️ Change Cron Time

Edit `vercel.json`:
```json
"crons": [{
  "path": "/api/functions/fraud_daily",
  "schedule": "0 7 * * *"  // minute hour day month weekday
}]
```

Examples:
- `0 7 * * *` = 7:00 AM daily
- `0 9 * * 1-5` = 9:00 AM weekdays
- `0 2 1 * *` = 2:00 AM on 1st of month
- `*/15 * * * *` = Every 15 minutes

## 🚨 Common Issues

### Cron Not Running
1. Check Vercel Dashboard → Crons
2. Verify env vars are set
3. Check logs for errors
4. Test manually: `curl /api/functions/fraud_daily`

### No Slack Messages
1. Test webhook: `curl -X POST YOUR_WEBHOOK --data '{"text":"test"}'`
2. Verify SLACK_WEBHOOK env var
3. Check channel permissions
4. Review logs for errors

### No Mdundo Data
1. Mdundo may block automated access
2. Check if URL is accessible
3. Add delays/retries in scraper
4. Check BeautifulSoup selectors

### Spotify Token Issues
1. Token expires - regenerate
2. Rate limit - add caching
3. Invalid token - verify credentials
4. Check logs for 401/403 errors

## 📈 Monitoring

### Key Metrics
- Daily artists analyzed
- Critical fraud detections
- Cron job success rate
- Slack notification delivery
- API response times

### View in Vercel
- Dashboard → Analytics
- Functions → fraud_daily → Runtime

### Alerts to Setup
- Function errors
- Cron failures
- High latency
- KV storage usage

## 🔐 Security

- ✅ Environment variables for secrets
- ✅ CRON_SECRET for job authentication
- ✅ Public endpoints (no auth needed)
- ✅ Slack webhook validation
- ⚠️ Don't commit .env files
- ⚠️ Rotate tokens periodically

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Full documentation |
| DEPLOYMENT.md | Step-by-step deploy guide |
| QUICKREF.md | This file |
| CONTRIBUTING.md | How to contribute |
| .env.example | Environment template |

## 🎯 Next Steps

1. **Deploy**: Follow DEPLOYMENT.md
2. **Test**: Run first cron manually
3. **Monitor**: Check logs daily for 1 week
4. **Optimize**: Adjust thresholds/schedule
5. **Enhance**: Add features/integrations

## 📞 Getting Help

1. Check README.md "Troubleshooting" section
2. Review Vercel logs: `vercel logs`
3. Check GitHub Issues
4. Create new Issue if stuck
5. Contact maintainer

## 📅 Maintenance

- Check Spotify token monthly (expires)
- Review fraud thresholds quarterly
- Monitor KV storage usage
- Update dependencies
- Analyze detection accuracy

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-16  
**Status:** Ready for Production
