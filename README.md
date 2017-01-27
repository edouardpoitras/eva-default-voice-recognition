Default Voice Recognition
=========================

The default voice recognition plugin used by Eva.

Makes heavy use of the Python [speech_recognition](https://github.com/Uberi/speech_recognition) module.

## Installation

Can be easily installed through the Web UI by using [Web UI Plugins](https://github.com/edouardpoitras/eva-web-ui-plugins).

Alternatively, add `default_voice_recognition` to your `eva.conf` file in the `enabled_plugins` option list and restart Eva.

The default configuration will use a limited version of Google Speech Recognition.
For long-term use you will need to either setup pocketsphinx, or setup API keys for one or more of the supported third-party services.
See the [speech_recognition](https://github.com/Uberi/speech_recognition) docs for more info.

## Usage

No extra steps need to be performed by the user.

Once properly installed, if a query/command does not contain text data, Eva will use the voice recognition service configured in this plugin to transcribe audio data into text.
The transcribed text will be attached to the query/command data and passed along to proceed with the usual Eva interaction process.
This removes the need for Eva clients to do the transcription (they can simply send the audio data to Eva via the usual pubsub channel, or stream the audio directly to Eva if the [audio_server](https://github.com/edouardpoitras/eva-audio-server) plugin is enabled.

## Configuration

Default configuration options can be changed by adding a `default_voice_recognition.conf` file in your plugin configuration path (can be configured in `eva.conf`, but usually `~/eva/configs`).

To get an idea of what configuration options are available, you can take a look at the `default_voice_recognition.conf.spec` file in this repository, or use the [Web UI](https://github.com/edouardpoitras/eva-web-ui) plugin and view them at `/plugins/configuration/default_voice_recognition`.

Here is a breakdown of the available options:

    active_voice_recognition
        Type: String
        Default: 'google_speech_recognition'
        Used to specify the default voice recognition service used.
        Can be any of the following:
            pocketsphinx
            google_speech_recognition
            google_cloud_speech
            wit_ai
            bing
            houndify
            ibm
            random
        All of the options, except for pocketsphinx and random, require corresponding credentials/API keys to have been setup in the configuration.
        Pocketsphinx refers to a local intallation (see [speech_recognition](https://github.com/Uberi/speech_recognition) docs for installation instructions).
        Random will choose a random service for every query/command.
        Random will only choose services that have credentials/API keys setup.
        Random will never use pocketsphinx.
    google_speech_recognition_api_key
        Type: String
        Default: ''
        The Google Speech Recognition API key to use.
        TODO: Provide link
    google_cloud_speech_json_credentials
        Type: String
        Default: ''
        The JSON credentials to use with this service.
        TODO: Provide link
    wit_ai_api_key
        Type: String
        Default: ''
        The Wit.ai API key to use.
        TODO: Provide link
    bing_api_key
        Type: String
        Default: ''
        The Bing API key to use.
        TODO: Provide link
    houndify_client_id
        Type: String
        Default: ''
        The Houndify client ID to use.
        TODO: Provide link
    houndify_client_key
        Type: String
        Default: ''
        The Houndify client key to use.
    ibm_speech_to_text_username
        Type: String
        Default: ''
        The IBM Speech-to-Text username to use.
        TODO: Provide link
    ibm_speech_to_text_password
        Type: String
        Default: ''
        The IBM Speech-to-Text password to use.
