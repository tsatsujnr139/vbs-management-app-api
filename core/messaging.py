import requests
from django.conf import settings

from core.models import Participant

endPoint = settings.SMS_ENDPOINT
apiKey = settings.SMS_API_KEY


def send_attendance_message(participant: Participant, vbs_day: str, pickup_code: int):
    message = (
        f"Dear {participant.parent_name},\n"
        f"{participant.first_name} {participant.last_name} has been marked as present for VBS {vbs_day.replace('_', ' ')}. "
        f"Your pickup code for this participant is {pickup_code} for VBS {vbs_day.replace('_', ' ')}. "
        f"Please keep this code handy when picking up your ward because it will be required to confirm pickup rights."
        f"Only share this code with someone who would be picking up your ward if needed."
    )
    send_sms(phone_number=participant.primary_contact_no, message=message)


def send_pickup_message(participant: Participant, vbs_day: str, pickup_person: str):
    message = (
        f"Dear {participant.parent_name},\n"
        f"{participant.first_name} {participant.last_name} ({participant.grade}) has been picked up from the LIC premises "
        f"for VBS {vbs_day.replace('_', ' ')}. "
        f"Please contact LIC VBS Admin on 0206052429 / 0208207958 / 0249333630 "
        f"immediately if this is unexpected or you have any questions or concerns."
    )
    send_sms(phone_number=participant.primary_contact_no, message=message)


def send_sms(phone_number: str, message: str):
    data = {
        "sender": "LIC VBS",
        "recipient[]": [phone_number],
        "message": message,
    }
    response = requests.post(
        f"{settings.SMS_ENDPOINT}?key={settings.SMS_API_KEY}", data
    )
    res_data = response.json()
    if res_data.get("status") != "success":
        print("Error sending SMS")
        print(res_data)
