import os
import logging
from flask import Flask, request
from twilio.rest import Client
import speech_recognition as sr
from deep_translator import GoogleTranslator
import requests
from requests.auth import HTTPBasicAuth
from pydub import AudioSegment

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='whatsapp_bot_translator.log')


# Static function that coverts an audio file from WhatsApp format (.ogg) to .wav
def convert_audio(input_file, output_file):
    # Converte o arquivo de áudio de ogg para wav
    audio = AudioSegment.from_file(input_file, format="ogg")
    audio.export(output_file, format="wav")


# Static function that transcribes an audio file
def transcribe_audio(audio_path):
    try:
        logging.info(f"Attempting to transcribe audio from: {audio_path}")
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            # Specify language as Portuguese (Brazil)
            transcription = recognizer.recognize_google(audio, language='pt-BR')
            logging.info(f"Transcription successful: {transcription}")
            return transcription
    except Exception as e:
        logging.error(f"Transcription error: {str(e)}")
        return f"Transcription error: {str(e)}"


class WhatsAppTranscriptionBot:
    def __init__(self):
        # Twilio configuration
        self.twilio_account_sid = 'your sid'
        self.twilio_auth_token = 'your token'
        self.twilio_phone_number = '+14155238886'

        # Initialize Twilio client
        self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)

        # Initialize speech recognizer and translator
        self.recognizer = sr.Recognizer()
        self.translator = GoogleTranslator(source='pt', target='en')

        # Flask app
        self.app = Flask(__name__)
        self.setup_routes()

    def translate_text(self, text):
        """Translate text from Portuguese to English"""
        try:
            logging.info(f"Translating text: {text}")
            translation = self.translator.translate(text)
            logging.info(f"Translation: {translation}")
            return translation
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            return f"Translation error: {str(e)}"

    def whatsapp_bot(self):
        audio_url = request.values.get('MediaUrl0')
        incoming_msg = ""

        if audio_url:
            logging.info(f"Audio URL: {audio_url}")
            try:
                # Accessing the URL with authentication
                response = requests.get(audio_url, auth=HTTPBasicAuth(self.twilio_account_sid, self.twilio_auth_token))
                logging.info(f"Audio download status code: {response.status_code}")
                if response.status_code == 200:
                    audio_content = response.content
                    logging.info(f"Audio file size: {len(audio_content)} bytes")
                    with open('audio_received.ogg', 'wb') as f:
                        f.write(audio_content)
                    try:
                        convert_audio('audio_received.ogg', 'audio_received.wav')
                        incoming_msg = transcribe_audio('audio_received.wav')
                        # Delete the audio files
                        os.unlink('audio_received.ogg')
                        os.unlink('audio_received.wav')
                        logging.info(f"Audio files deleted.")
                    except Exception as e:
                        logging.error(f"Error coverting or transcribing the audio: {str(e)}")
                        incoming_msg = "Erro ao processar o áudio."
                else:
                    incoming_msg = f"Error downloading audio. Status: {response.status_code}"
            except Exception as e:
                logging.error(f"Error downloading audio: {str(e)}")
                incoming_msg = "Error downloading audio."
        else:
            incoming_msg = request.values.get('Body', '').lower()

        # Translate transcription
        translation = self.translate_text(incoming_msg)

        # Construct the response with both the transcription and translation
        response_text = f"🇧🇷: {incoming_msg}\n\n🇺🇸: {translation}"

        # Send the message on WhatsApp
        to_number = request.values.get('From')
        message = self.twilio_client.messages.create(
            body=response_text,
            # Twilio's WhatsApp number
            from_='whatsapp:+14155238886',
            to=to_number
        )

        return str(message.sid)

    def setup_routes(self):
        """Set up Flask routes"""
        @self.app.route("/whatsapp", methods=['POST'])
        def webhook():
            return self.whatsapp_bot()

    def run(self, debug=True, port=8080):
        """Run the Flask application"""
        logging.info(f"Starting WhatsApp Transcription Bot on port {port}")
        self.app.run(host='0.0.0.0', debug=debug, port=port)


if __name__ == '__main__':
    bot = WhatsAppTranscriptionBot()
    bot.run()