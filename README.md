# whatsapp-audio-bot
A WhatsApp bot to transcribe and translate audio messages

## Prequisites 

### 1. Setup a Python Virtual Environment

A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them.

Run following command to create a new virtual environment inside your project folder:

```
python -m venv myvenv
```

Activate the virtual environment by running following command:
 
```
source myvenv/bin/activate
```
### 2. Create an account on Twilio
The Twilio API for WhatsApp is the quickest way to be able to send and receive WhatApp messages through Python code.
[Twilio](https://www.twilio.com/)

### 3. Create an account on ngrok
ngrok allows you to tunnel your localhost to the web. 
This will be useful to test the app.

[Ngork](https://ngrok.com)

### 4. Install required Python Packages:

- [flask](https://github.com/pallets/flask)
    
    ```
    pip install flask
    ```
    
- [twilio](https://github.com/twilio/twilio-python)
    
    ```
    pip install twilio
    ```
- [ngrok](https://github.com/NGROK)
    
    ```
    brew install ngrok/ngrok/ngrok
    ```

### 4. Setup your variables in the whatsapp-bot-translator.py

- twilio_account_sid and twilio_auth_token that you can find on your Twilio account in the Verifications tab

- Your source and target languages for the audio that will be transcribed and translated, in my case I'm translating Portuguese into English : source='pt', target='en'
Make sure to edit the emojis as well 🇧🇷 🇺
🇸
- And you're good to go !
