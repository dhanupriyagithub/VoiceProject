
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AudioRecordForm  # Import your AudioRecordForm
import time


# Your Twilio Account SID and Auth Token
account_sid = "ACf1a498b26cacb62bbe689adf0697130d"
auth_token = "d8e546a1597143d56b9063002a7923a7"
# Create a Twilio client
client = Client(account_sid, auth_token)

# Twilio phone number (your Twilio phone number)
from_phone_number = "+14423334087"  # Your Twilio phone number

# Function to initiate the call and enter phone number
def initiate_and_enter(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Create a TwiML response
        voice_response = VoiceResponse()

        # Add instructions for the call
        voice_response.say("You are about to initiate a call. Please wait.")
        voice_response.dial(phone_number)

        # Make the call
        call = client.calls.create(
            to=phone_number,
            from_=from_phone_number,
            twiml=str(voice_response)
        )

        # Store the call SID in the session to use it later
        request.session['call_sid'] = call.sid

        # Wait for a few seconds (adjust as needed) to allow the call to complete
        
        time.sleep(10)  # Wait for 10 seconds

        # Use the Twilio API to get the call recording URL
        call_sid = request.session.get('call_sid')
        call = client.calls.get(call_sid)
        print(call)
        recording_url = call.recordings.list()[0].uri
        print(recording_url)

        # Save the recording URL and phone number to your database using your AudioRecordForm
        form = AudioRecordForm({'recording_url': recording_url, 'phone_number': phone_number})
        if form.is_valid():
            form.save()

        return HttpResponse('Audio saved successfully')  # You can customize this response
    else:
        return render(request, 'home.html')  # Render the phone call form
