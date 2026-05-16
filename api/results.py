"""
Results API Endpoint
Query fraud detection results from KV storage
"""

import os
import json
from datetime import datetime

import sys
sys.path.insert(0, os.path.dirname(__file__))

from lib.kv_storage import KVStorage


async def handler(request):
    """
    GET /api/results?country=ng[&days=30]
    Returns fraud detection results for a country
    """

    # Parse query parameters
    country = request.args.get('country', '').lower()
    days = int(request.args.get('days', '1'))

    if not country:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing country parameter",
                "example": "/api/results?country=ng"
            })
        }

    valid_countries = ["ng", "tz", "ke", "za", "ug", "gh", "cm"]
    if country not in valid_countries:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Invalid country. Valid options: {', '.join(valid_countries)}"
            })
        }

    try:
        kv = KVStorage()

        if days == 1:
            # Get latest results for today
            results = await kv.get_latest_results(country)
            if not results:
                return {
                    "statusCode": 404,
                    "body": json.dumps({
                        "error": f"No results found for {country.upper()}",
                        "timestamp": datetime.now().isoformat()
                    })
                }
        else:
            # Get historical results
            results = await kv.get_historical_results(country, days)
            if not results:
                return {
                    "statusCode": 404,
                    "body": json.dumps({
                        "error": f"No results found for {country.upper()} in last {days} days"
                    })
                }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Cache-Control": "public, s-maxage=3600"  # Cache for 1 hour
            },
            "body": json.dumps({
                "country": country.upper(),
                "results": results if isinstance(results, list) else [results],
                "timestamp": datetime.now().isoformat()
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"Server error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            })
        }
