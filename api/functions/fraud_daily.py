"""
Daily Fraud Detection Cron Handler
Runs daily via Vercel Crons to analyze Mdundo charts across all countries
"""

import os
import json
from datetime import datetime
from typing import Dict

# Import our modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lib.fraud_detector import MdundoFraudDetector
from lib.mdundo_scraper import MdundoScraper
from lib.slack_notifier import SlackNotifier
from lib.kv_storage import KVStorage


class FraudDetectionJob:
    """Manages the daily fraud detection job"""

    COUNTRIES = ["ng", "tz", "ke", "za", "ug", "gh", "cm"]

    def __init__(self):
        self.scraper = MdundoScraper()
        self.kv = KVStorage()
        self.spotify_token = os.getenv("SPOTIFY_TOKEN")
        self.slack_enabled = bool(os.getenv("SLACK_WEBHOOK"))

    async def run(self) -> Dict:
        """Execute the complete fraud detection job"""

        print("\n" + "="*70)
        print("🔍 MDUNDO DAILY FRAUD DETECTION - VERCEL CRON JOB")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("="*70 + "\n")

        all_results = {}
        all_summary = {}
        critical_alerts = {}

        # Process each country
        for country in self.COUNTRIES:
            print(f"Processing {country.upper()}...")

            try:
                # Step 1: Scrape chart
                artists, error = self.scraper.scrape_chart(country, limit=50)

                if error:
                    print(f"  ⚠️  {error}")
                    all_results[country] = {"error": error}
                    continue

                if not artists:
                    print(f"  ⚠️  No data found for {country.upper()}")
                    all_results[country] = {"artists": [], "summary": {}}
                    continue

                print(f"  ✓ Found {len(artists)} artists")

                # Step 2: Run fraud detection
                detector = MdundoFraudDetector(spotify_api_token=self.spotify_token)

                for artist in artists:
                    detector.analyze_artist(
                        rank=artist['rank'],
                        artist_name=artist['artist'],
                        mdundo_song=artist['song'],
                        mdundo_url=artist['url']
                    )

                print(f"  ✓ Analysis complete")

                # Step 3: Get results and summary
                summary = detector.get_results_summary()
                all_summary[country] = summary

                # Prepare results for storage
                results_data = {
                    "artists": detector.results_to_dict(),
                    "summary": summary
                }

                all_results[country] = results_data

                # Step 4: Save to KV storage
                await self.kv.save_daily_results(country, results_data["artists"], summary)
                print(f"  ✓ Saved to KV storage")

                # Check for critical alerts
                critical_artists = detector.get_critical_artists()
                if critical_artists:
                    critical_alerts[country] = {
                        "artists": critical_artists,
                        "summary": summary
                    }
                    print(f"  🔴 {len(critical_artists)} CRITICAL risk artist(s) detected")

            except Exception as e:
                print(f"  ❌ Error processing {country.upper()}: {str(e)}")
                all_results[country] = {"error": str(e)}

        # Step 5: Send notifications
        if self.slack_enabled:
            await self._send_notifications(all_results, all_summary, critical_alerts)

        # Step 6: Generate report
        report = self._generate_report(all_results, all_summary, critical_alerts)

        print("\n" + "="*70)
        print("✅ DAILY CHECK COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")

        return report

    async def _send_notifications(self, results: Dict, summary: Dict, critical_alerts: Dict):
        """Send Slack notifications"""
        try:
            notifier = SlackNotifier()

            # Send main daily report
            notifier.send_daily_report(results, summary)
            print("  ✓ Daily report sent to Slack")

            # Send critical alerts
            for country, alert_data in critical_alerts.items():
                notifier.send_critical_alert(
                    country,
                    alert_data["artists"],
                    alert_data["summary"]
                )
                print(f"  ✓ Critical alert sent for {country.upper()}")

        except Exception as e:
            print(f"  ⚠️  Error sending Slack notifications: {str(e)}")

    @staticmethod
    def _generate_report(results: Dict, summary: Dict, critical_alerts: Dict) -> Dict:
        """Generate final report"""
        total_analyzed = sum(
            s.get("total_analyzed", 0)
            for s in summary.values()
        )

        total_critical = sum(
            s.get("critical_risk", 0)
            for s in summary.values()
        )

        total_high = sum(
            s.get("high_risk", 0)
            for s in summary.values()
        )

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_analyzed": total_analyzed,
                "total_critical": total_critical,
                "total_high": total_high,
                "countries_processed": len(summary),
                "critical_alerts": len(critical_alerts)
            },
            "countries": summary,
            "critical_artists_by_country": {
                country: len(data["artists"])
                for country, data in critical_alerts.items()
            }
        }


# Vercel serverless handler
async def handler(request):
    """Vercel serverless function handler"""

    # Verify this is a cron request (optional security check)
    auth_header = request.headers.get('authorization', '')
    if auth_header != f"Bearer {os.getenv('CRON_SECRET', '')}":
        # In development/testing, allow without auth
        if os.getenv('CRON_SECRET'):
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Unauthorized"})
            }

    job = FraudDetectionJob()

    try:
        report = await job.run()

        return {
            "statusCode": 200,
            "body": json.dumps(report)
        }

    except Exception as e:
        error_report = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

        return {
            "statusCode": 500,
            "body": json.dumps(error_report)
        }


# For local testing
if __name__ == "__main__":
    import asyncio

    job = FraudDetectionJob()
    report = asyncio.run(job.run())
    print(json.dumps(report, indent=2))
