from io import BytesIO
import random
import speech_recognition as sr
import gossip
from eva import log
from eva import conf
from eva import scheduler

ACTIVE_VOICE_RECOGNITION = \
    conf['plugins']['default_voice_recognition']['config']['active_voice_recognition']
GOOGLE_SPEECH_RECOGNITION_API_KEY = \
    conf['plugins']['default_voice_recognition']['config']['google_speech_recognition_api_key']
GOOGLE_CLOUD_SPEECH_JSON_CREDENTIALS = \
    conf['plugins']['default_voice_recognition']['config']['google_cloud_speech_json_credentials']
WIT_AI_API_KEY = conf['plugins']['default_voice_recognition']['config']['wit_ai_api_key']
BING_API_KEY = conf['plugins']['default_voice_recognition']['config']['bing_api_key']
HOUNDIFY_CLIENT_ID = conf['plugins']['default_voice_recognition']['config']['houndify_client_id']
HOUNDIFY_CLIENT_KEY = conf['plugins']['default_voice_recognition']['config']['houndify_client_key']
IBM_SPEECH_TO_TEXT_USERNAME = \
    conf['plugins']['default_voice_recognition']['config']['ibm_speech_to_text_username']
IBM_SPEECH_TO_TEXT_PASSWORD = \
    conf['plugins']['default_voice_recognition']['config']['ibm_speech_to_text_password']

@gossip.register('eva.voice_recognition')
def eva_voice_recognition(data):
    audio_file = BytesIO(data['input_audio']['audio'])
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    text = transcribe(audio, ACTIVE_VOICE_RECOGNITION)
    if text is not None:
        data['input_text'] = text

def transcribe(audio, service=None):
    if service == 'pocketsphinx':
        return transcribe_pocketsphinx(audio)
    elif service == 'google_speech_recognition':
        return transcribe_google_speech_recognition(audio)
    elif service == 'google_cloud_speech':
        return transcribe_google_cloud_speech(audio)
    elif service == 'wit_ai':
        return transcribe_wit_ai(audio)
    elif service == 'bing':
        return transcribe_bing(audio)
    elif service == 'houndify':
        return transcribe_houndify(audio)
    elif service == 'ibm':
        return transcribe_ibm(audio)
    else:
        # Don't use pocketsphinx when randomizing service.
        available_services = get_available_services(pocketsphinx=False)
        if len(available_services) < 1:
            log.error('No available voice recognition system, ensure you have \
                       specified API credentials in configuration')
            return
        random_selection = random.choice(available_services)
        return transcribe(audio, random_selection)

def get_available_services(pocketsphinx=True):
    available = []
    if pocketsphinx:
        available.append('pocketsphinx')
    if valid_google_speech_recognition_creds():
        available.append('google_speech_recognition')
    if valid_google_cloud_speech_creds():
        available.append('google_cloud_speech')
    if valid_wit_ai_creds():
        available.append('wit_ai')
    if valid_bing_creds():
        available.append('bing')
    if valid_houndify_creds():
        available.append('houndify')
    if valid_ibm_creds():
        available.append('ibm')
    return available

def valid_google_speech_recognition_creds():
    if GOOGLE_SPEECH_RECOGNITION_API_KEY is not None and \
       GOOGLE_SPEECH_RECOGNITION_API_KEY != '':
        return True
    return False

def valid_google_cloud_speech_creds():
    if GOOGLE_CLOUD_SPEECH_JSON_CREDENTIALS is not None and \
       GOOGLE_CLOUD_SPEECH_JSON_CREDENTIALS != '':
        return True
    return False

def valid_wit_ai_creds():
    if WIT_AI_API_KEY is not None and WIT_AI_API_KEY != '':
        return True
    return False

def valid_bing_creds():
    if BING_API_KEY is not None and BING_API_KEY != '':
        return True
    return False

def valid_houndify_creds():
    client_id = HOUNDIFY_CLIENT_ID
    client_key = HOUNDIFY_CLIENT_KEY
    if client_id is not None and client_id != '' and client_key is not None and client_key != '':
        return True
    return False

def valid_ibm_creds():
    username = IBM_SPEECH_TO_TEXT_USERNAME
    password = IBM_SPEECH_TO_TEXT_PASSWORD
    if username is not None and username != '' and password is not None and password != '':
        return True
    return False

def transcribe_pocketsphinx(audio):
    try:
        recognizer = sr.Recognizer()
        result = recognizer.recognize_sphinx(audio)
        log.info('Pocketsphinx recognition results: %s' %result)
        return result
    except sr.UnknownValueError:
        log.error('Sphinx could not understand audio')
    except sr.RequestError as e:
        log.error('Sphinx error: {0}'.format(e))

def transcribe_google_speech_recognition(audio):
    try:
        recognizer = sr.Recognizer()
        api_key = GOOGLE_SPEECH_RECOGNITION_API_KEY
        if api_key == '':
            api_key = None
        result = recognizer.recognize_google(audio, key=api_key)
        log.info('Google speech recognition results: %s' %result)
        return result
    except sr.UnknownValueError:
        log.error('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        log.error('Could not request results from Google Speech Recognition service: {0}'.format(e))

def transcribe_google_cloud_speech(audio):
    creds = GOOGLE_CLOUD_SPEECH_JSON_CREDENTIALS
    if creds is None or creds == '':
        log.error('Can not use Google cloud speech for recognition without JSON credentials')
        return
    try:
        recognizer = sr.Recognizer()
        result = recognizer.recognize_google_cloud(audio, credentials_json=creds)
        log.info('Google cloud speech recognition results: %s' %result)
        return result
    except sr.UnknownValueError:
        log.error('Google Cloud Speech could not understand audio')
    except sr.RequestError as e:
        log.error('Could not request results from Google Cloud Speech service: {0}'.format(e))

def transcribe_wit_ai(audio):
    api_key = WIT_AI_API_KEY
    if api_key is None or api_key == '':
        log.error('Can not use Wit.ai for recognition without API key')
        return
    try:
        recognizer = sr.Recognizer()
        result = recognizer.recognize_wit(audio, key=api_key)
        log.info('Wit.ai recognition results: %s' %result)
        return result
    except sr.UnknownValueError:
        log.error('Wit.ai could not understand audio')
    except sr.RequestError as e:
        log.error('Could not request results from Wit.ai service: {0}'.format(e))

def transcribe_bing(audio):
    api_key = BING_API_KEY
    if api_key is None or api_key == '':
        log.error('Can not use Bing for recognition without API key')
        return
    try:
        recognizer = sr.Recognizer()
        result = recognizer.recognize_bing(audio, key=api_key)
        log.info('Bing recognition results: %s' %result)
        return result
    except sr.UnknownValueError:
        log.error('Microsoft Bing Voice Recognition could not understand audio')
    except sr.RequestError as e:
        log.error('Could not request results from Microsoft Bing Voice Recognition: {0}'.format(e))

def transcribe_houndify(audio):
    client_id = HOUNDIFY_CLIENT_ID
    client_key = HOUNDIFY_CLIENT_KEY
    if client_id is None or client_id == '' or client_key is None or client_key == '':
        log.error('Can not use Houndify for recognition without client id and key')
        return
    try:
        recognizer = sr.Recognizer()
        result = recognizer.recognize_houndify(audio, client_id=client_id, client_key=client_key)
        log.info('Houndify recognition results: %s' %result)
        return result
    except sr.UnknownValueError:
        log.error('Houndify could not understand audio')
    except sr.RequestError as e:
        log.error('Could not request results from Houndify service: {0}'.format(e))

def transcribe_ibm(audio):
    username = IBM_SPEECH_TO_TEXT_USERNAME
    password = IBM_SPEECH_TO_TEXT_PASSWORD
    if username is None or username == '' or password is None or password == '':
        log.error('Can not use IBM for recognition without username and password')
        return
    try:
        recognizer = sr.Recognizer()
        result = recognizer.recognize_ibm(audio, username=username, password=password)
        log.info('IBM recognition results: %s' %result)
        return result
    except sr.UnknownValueError:
        log.error('IBM Speech to Text could not understand audio')
    except sr.RequestError as e:
        log.error('Could not request results from IBM Speech to Text service: {0}'.format(e))
