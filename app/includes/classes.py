import json
import ovh
import http.client
import urllib.parse

class PushoverNotifier:
    def __init__(self, token, user_key):
        self.token = token
        self.user_key = user_key
        self.api_url = "api.pushover.net"
        self.api_endpoint = "/1/messages.json"

    def send_message(self, message, title=None, url=None, url_title=None, priority=0):
        """
            Sends a message to PushOver.
        """

        conn = http.client.HTTPSConnection(self.api_url)
        post_data = {
            "token": self.token,
            "user": self.user_key,
            "message": message,
            "priority": priority,
            "sound": "intermission"
        }

        if title:
            post_data["title"] = title
        if url:
            post_data["url"] = url
        if url_title:
            post_data["url_title"] = url_title

        post_data_encoded = urllib.parse.urlencode(post_data)
        conn.request("POST", self.api_endpoint, post_data_encoded, {"Content-type": "application/x-www-form-urlencoded"})
        response = conn.getresponse()
        return response.status, response.reason

class OVHAvailabilityChecker:
    def __init__(self, application_key, application_secret, consumer_key, endpoint='ovh-eu'):
        self.client = ovh.Client(
            endpoint=endpoint,
            application_key=application_key,
            application_secret=application_secret,
            consumer_key=consumer_key
        )

    def check_availability(self, fqn):
        """
            Checks the availability of a specific server by its fqn value.
        """

        result = self.client.get('/dedicated/server/datacenter/availabilities')
        data = next((entry for entry in result if entry.get('fqn') == fqn), None)

        if not data:
            print(f"No data found for FQN '{fqn}'")
            return None

        available_datacenters = [
            {"datacenter": dc["datacenter"], "availability": dc["availability"]}
            for dc in data.get("datacenters", [])
            if dc["availability"] != "unavailable"
        ]
        
        return available_datacenters