"""
Status API Endpoint
Check the status of fraud detection system and view latest results
"""

import os
import json
from datetime import datetime

# For Vercel deployment
async def handler(request):
    """GET /api/status - Returns system status"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "status": "operational",
            "service": "Mdundo Fraud Detection",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "daily_check": "/api/functions/fraud_daily",
                "status": "/api/status",
                "results": "/api/results",
                "health": "/api/health"
            }
        })
    }
