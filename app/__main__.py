from includes.classes import PushoverNotifier
from includes.classes import OVHAvailabilityChecker
from load_dotenv import load_dotenv
import time
import os
import logging

def main():
    # Load environment variables
    load_dotenv()

    # API credentials for OVH and PushOver
    ovh_application_key = str(os.getenv("OVH_APP_KEY", None))
    ovh_application_secret = str(os.getenv("OVH_APP_SECRET", None))
    ovh_consumer_key = str(os.getenv("OVH_CONSUMER_KEY", None))
    pushover_token = str(os.getenv("PO_TOKEN", None))
    pushover_user_key = str(os.getenv("PO_USER_KEY", None))
    check_interval = int(os.getenv("CHECK_INTERVAL", 60))

    # Initialize OVHAvailabilityChecker and PushoverNotifier
    checker = OVHAvailabilityChecker(ovh_application_key, ovh_application_secret, ovh_consumer_key)
    notifier = PushoverNotifier(pushover_token, pushover_user_key)

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Define the server FQN to check
    fqns = [
        "24ska01.ram-64g-noecc-2133.softraid-1x480ssd",
        # "24sk50-syd.ram-64g-ecc-2400.softraid-2x450nvme"
    ]

    # "24sk50-syd.ram-64g-ecc-2400.softraid-2x450nvme" -> is praktisch altidj op voorraad. Test

    while True:
        for fqn in fqns:
            # Check availability
            available_datacenters = checker.check_availability(fqn)

            # If available, send a PushOver notification
            if available_datacenters:
                datacenter_info = "\n".join([f"{dc['datacenter']} : {dc['availability']}" for dc in available_datacenters])
                message = f"Server 'KS-A' is available in the following datacenters:\n{datacenter_info}"
                status, reason = notifier.send_message(message, title="OVH Server Availability", priority=1)

                # Report notification status
                if status == 200:
                    logging.info(f"YES, IN STOCK!!! Notification sent!")
                else:
                    logging.info(f"IN STOCK, but shit! Something went wrong with PushOver: {reason}")
            else:
                logging.info(f"Sad.. No availability found... ")
        time.sleep(check_interval)

if __name__ == "__main__":
    main()