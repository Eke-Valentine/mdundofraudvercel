# Deployment Guide - Step by Step

Complete guide to deploy Mdundo Fraud Detection to Vercel.

## Prerequisites Checklist

- [ ] GitHub account
- [ ] Vercel account (free)
- [ ] Spotify Developer account
- [ ] Slack workspace admin access
- [ ] Git installed on your computer

## Step 1: Prepare GitHub Repository

### 1.1 Initialize Git (if not already done)
```bash
cd fraud_detection_vercel
git init
git add .
git commit -m "Initial commit: Mdundo fraud detection"
```

### 1.2 Create GitHub Repository
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `mdundo-fraud-detection`
3. Description: "Automated fraud detection for Mdundo charts"
4. Select "Public" (or Private if preferred)
5. Click "Create repository"

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/mdundo-fraud-detection.git
git branch -M main
git push -u origin main
```

## Step 2: Get API Credentials

### 2.1 Spotify API Token

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in (create account if needed)
3. Click "Create an App"
   - App name: "Mdundo Fraud Detection"
   - Accept terms
   - Click "Create"
4. Go to app settings
5. Copy **Client ID**
6. Click "Show Client Secret" and copy it
7. Generate token using cURL:

```bash
CLIENT_ID="your_client_id"
CLIENT_SECRET="your_client_secret"

TOKEN=$(curl -X POST https://accounts.spotify.com/api/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET" \
  | jq -r '.access_token')

echo "SPOTIFY_TOKEN=$TOKEN"
```

**Save the token** - you'll need it for Vercel.

### 2.2 Slack Webhook URL

1. Go to [Slack API Dashboard](https://api.slack.com/apps)
2. Click "Create New App"
   - Choose "From scratch"
   - App Name: "Mdundo Fraud Detection"
   - Workspace: Select your workspace
   - Click "Create App"
3. Left sidebar → "Incoming Webhooks"
4. Toggle "Activate Incoming Webhooks" → ON
5. Click "Add New Webhook to Workspace"
6. Select channel where you want fraud alerts
7. Click "Allow"
8. Copy the **Webhook URL**

**Save the webhook URL** - you'll need it for Vercel.

### 2.3 Create Random CRON_SECRET

```bash
# Generate random secret
openssl rand -hex 32
# or
python -c "import secrets; print(secrets.token_hex(32))"
```

**Save this secret** - you'll need it for Vercel.

## Step 3: Deploy to Vercel

### Option A: Web Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Sign up / Log in (GitHub sign-in recommended)
3. Click "New Project"
4. Select "Import Git Repository"
5. Paste your GitHub URL: `https://github.com/YOUR_USERNAME/mdundo-fraud-detection`
6. Click "Import"
7. Configure project:
   - Framework: "Other"
   - Root Directory: `./` (leave blank)
   - Build Command: Leave empty
   - Output Directory: Leave empty
8. Click "Deploy"
9. Wait for deployment to complete (~2-3 minutes)

### Option B: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to production
vercel --prod
```

## Step 4: Add Environment Variables

### Via Vercel Dashboard

1. Go to your Vercel project
2. Click "Settings"
3. Left sidebar → "Environment Variables"
4. Add three variables:

**Variable 1: SPOTIFY_TOKEN**
- Name: `SPOTIFY_TOKEN`
- Value: (paste your Spotify token from Step 2.1)
- Environments: ✓ Production ✓ Preview ✓ Development
- Click "Add"

**Variable 2: SLACK_WEBHOOK**
- Name: `SLACK_WEBHOOK`
- Value: (paste your Slack webhook URL from Step 2.2)
- Environments: ✓ Production ✓ Preview ✓ Development
- Click "Add"

**Variable 3: CRON_SECRET**
- Name: `CRON_SECRET`
- Value: (paste your random secret from Step 2.3)
- Environments: ✓ Production ✓ Preview ✓ Development
- Click "Add"

### Via Vercel CLI

```bash
vercel env add SPOTIFY_TOKEN
# Paste your Spotify token

vercel env add SLACK_WEBHOOK
# Paste your Slack webhook

vercel env add CRON_SECRET
# Paste your random secret
```

## Step 5: Verify Deployment

### 5.1 Test Status Endpoint
```bash
# Replace PROJECT_NAME with your Vercel project name
curl https://PROJECT_NAME.vercel.app/api/status

# Expected response:
# {
#   "status": "operational",
#   "service": "Mdundo Fraud Detection",
#   ...
# }
```

### 5.2 Trigger Cron Manually (First Run)
```bash
# In Vercel dashboard:
# Project → Deployments → Select latest → Functions
# Click on fraud_daily function → Test

# Or use curl with secret:
curl -X POST https://PROJECT_NAME.vercel.app/api/functions/fraud_daily \
  -H "Authorization: Bearer YOUR_CRON_SECRET" \
  -H "Content-Type: application/json"
```

### 5.3 Check Vercel Logs
1. Vercel Dashboard → Project → Deployments
2. Select latest deployment
3. Click "Functions" tab
4. Click `fraud_daily` to see logs
5. Look for "✅ DAILY CHECK COMPLETED SUCCESSFULLY"

## Step 6: Configure Cron Schedule

The cron is already configured in `vercel.json` to run daily at **7 AM UTC**.

To change the time:

1. Edit `vercel.json`:
```json
"crons": [
  {
    "path": "/api/functions/fraud_daily",
    "schedule": "0 7 * * *"  // Change this line
  }
]
```

2. Cron syntax: `minute hour dayOfMonth month dayOfWeek`
   - `0 7 * * *` = 7:00 AM UTC every day
   - `0 9 * * 1-5` = 9:00 AM UTC Mon-Fri
   - `30 8 * * 0` = 8:30 AM UTC Sundays

3. Commit and push:
```bash
git add vercel.json
git commit -m "Update cron schedule"
git push origin main
```

4. Vercel will automatically redeploy

## Step 7: Verify Slack Integration

### 7.1 Manual Test
```bash
python -c "
from lib.slack_notifier import SlackNotifier
import os

notifier = SlackNotifier(os.getenv('SLACK_WEBHOOK'))
result = notifier.send_critical_alert(
    'ng',
    [{
        'rank': 1,
        'name': 'Test Artist',
        'fraud_score': 75,
        'flags': ['Test flag']
    }],
    {'total_analyzed': 50, 'critical_risk': 1, 'high_risk': 2}
)
print('Slack message sent!' if result else 'Failed to send')
"
```

### 7.2 Check Slack Channel
- Look for fraud detection message in your Slack channel
- If received, integration is working!

## Step 8: Monitor Production

### Set up Email Alerts
1. Vercel Dashboard → Settings → Monitoring
2. Add alert for function errors
3. Set notification email

### View Logs Regularly
```bash
# Via CLI
vercel logs mdundo-fraud-detection --follow

# Or via dashboard - Project → Deployments → Select → Functions → fraud_daily
```

### Check KV Storage Usage
1. Dashboard → Storage → KV
2. Monitor data usage (you have 3GB free)

## Troubleshooting

### Cron Not Running
1. Check Vercel dashboard Crons tab
2. Verify environment variables are set
3. Check function logs for errors

### Slack Messages Not Sending
```bash
# Test webhook directly
curl -X POST \
  -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  YOUR_SLACK_WEBHOOK_URL
```

### No Data From Mdundo
- Mdundo may block automated scraping
- Check logs: `vercel logs mdundo-fraud-detection`
- Consider proxy rotation if blocked

### Spotify Token Expired
- Tokens have limited lifetime
- Regenerate: See Step 2.1
- Update in Vercel environment variables

## Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Deployed to Vercel
- [ ] Environment variables set (SPOTIFY_TOKEN, SLACK_WEBHOOK, CRON_SECRET)
- [ ] Status endpoint responds (status.py)
- [ ] Cron job scheduled in vercel.json
- [ ] Manual cron test successful
- [ ] Slack message received in channel
- [ ] Logs show "✅ DAILY CHECK COMPLETED SUCCESSFULLY"
- [ ] Set up monitoring alerts

## Next Steps

1. **Monitor**: Check logs daily for first week
2. **Optimize**: Adjust cron schedule based on your needs
3. **Enhance**: Add email reports, database storage, web dashboard
4. **Scale**: Add more countries, adjust fraud thresholds
5. **Integrate**: Connect to internal tools/dashboards

## Support Resources

- [Vercel Docs](https://vercel.com/docs)
- [Spotify API Docs](https://developer.spotify.com/documentation/web-api)
- [Slack API Docs](https://api.slack.com/docs)
- [Python Requests Docs](https://requests.readthedocs.io/)

---

**Last Updated:** 2026-05-16  
**Version:** 1.0.0
