"""IOS notifications module."""
from pyicloud import PyiCloudService
import datetime

from todo.constants import DATA_DIR
from todo.notifications.ios_reminders import RemindersService

# TODO credential handling.

def authenticate(api: PyiCloudService):
    # Check if 2FA is required
    
    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            return False

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
    elif api.requires_2sa:
        import click
        print("Two-step authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print(
                "  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber')))
            )

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            return False

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            return False
        
    return True

def create_icloud_reminder(summary, due_date):
    api = PyiCloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD, cookie_directory=DATA_DIR)

    # Perform authentication
    if not authenticate(api):
        print("Authentication failed.")
        return

    # Access reminders service
    service_root = api._get_webservice_url("reminders")
    reminders = RemindersService(service_root, api.session, api.params)

    # Add the reminder
    reminders.post(title="test", description=summary, due_date=due_date)
    reminders.lists.
    print(f'Reminder "{summary}" created, due on {due_date}')

# Example usage
summary = 'Complete Python project'
due_date = datetime.datetime(2024, 6, 3, 12, 0, 0)  # Year, Month, Day, Hour, Minute, Second
create_icloud_reminder(summary, due_date)