import os
import requests
from datetime import datetime, timezone

from features.base_feature import BaseFeature

class ReplizFeature(BaseFeature):
    """
    Integration with Repliz API to post content.
    """
    BASE_URL = "https://api.repliz.com"

    def __init__(self):
        self.access_key = os.environ.get("REPLIZ_ACCESS_KEY")
        self.secret_key = os.environ.get("REPLIZ_SECRET_KEY")

        if not self.access_key or not self.secret_key:
            print("⚠️ REPLIZ_ACCESS_KEY or REPLIZ_SECRET_KEY not set in environment.")

    def _get_auth(self):
        return (self.access_key, self.secret_key)

    def get_accounts(self):
        """Fetch all connected social media accounts."""
        if not self.access_key:
            return []

        url = f"{self.BASE_URL}/public/account?page=1&limit=50"
        try:
            resp = requests.get(url, auth=self._get_auth())
            resp.raise_for_status()
            data = resp.json()
            return data.get("docs", [])
        except Exception as e:
            print(f"❌ Repliz Error: Could not fetch accounts - {e}")
            return []

    def create_schedule(self, account_ids, text, media_urls):
        """
        Create a schedule to post immediately using the provided media URLs.
        media_urls is a list of dicts: {"type": "image"|"video", "url": "..."}
        """
        if not account_ids:
            return False

        # If it's a list, post to each account. If it's single, put in array context
        if not isinstance(account_ids, list):
            account_ids = [account_ids]

        # Determine type based on media
        content_type = "text"
        if media_urls:
            if len(media_urls) == 1:
                content_type = media_urls[0]["type"]
            else:
                content_type = "album"

        # Prepare payload
        payload = {
            "title": "",
            "description": text,
            "type": content_type,
            "medias": media_urls
        }

        # Set scheduleAt exactly to now (instantly posts)
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        payload["scheduleAt"] = now_iso

        created_schedules = []
        for acc_id in account_ids:
            payload["accountId"] = acc_id
            url = f"{self.BASE_URL}/public/schedule"
            try:
                resp = requests.post(url, json=payload, auth=self._get_auth())
                resp.raise_for_status()
                data = resp.json()
                created_schedules.append({
                    "account_id": acc_id,
                    "schedule_id": data.get("_id"),
                    "status": data.get("status", "pending")
                })
                print(f"  ✅ Successfully scheduled on Repliz account {acc_id}")
            except Exception as e:
                print(f"  ❌ Repliz Error for account {acc_id}: {e}")
                if hasattr(e, "response") and e.response is not None:
                    print(f"     Details: {e.response.text}")

        return created_schedules

    def get_schedule_status(self, schedule_id):
        """Fetch the status of a scheduled post by its ID."""
        if not self.access_key or not schedule_id:
            return None
        
        url = f"{self.BASE_URL}/public/schedule/{schedule_id}"
        try:
            resp = requests.get(url, auth=self._get_auth())
            resp.raise_for_status()
            data = resp.json()
            return data
        except Exception as e:
            print(f"❌ Repliz Error: Could not fetch schedule status for {schedule_id} - {e}")
            return None

    def execute(self, *args, **kwargs):
        pass
