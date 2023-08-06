# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2021 Neongecko.com Inc.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
#    and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#    and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from inspect import signature
from time import time

import google

from google.cloud import speech_v1p1beta1 as speech
from google.oauth2.service_account import Credentials
from mycroft_bus_client import Message
from speech_recognition import AudioData

from neon_utils.logger import LOG

try:
    from neon_speech.stt import STT
except ImportError:
    from ovos_plugin_manager.templates.stt import STT

LOG.name = "stt_plugin"


class GoogleCloudBetaSTT(STT):
    """
        STT interface for Google Cloud Speech-To-Text
        To use pip install google-cloud-speech and add the
        Google API key to local mycroft.conf file. The STT config
        will look like this:

        "stt": {
            "module": "google_cloud_streaming",
            "google_cloud_streaming": {
                "credential": {
                    "json": {
                        # Paste Google API JSON here
        ...

    """

    def __init__(self, config=None):
        if len(signature(super(GoogleCloudBetaSTT, self).__init__).parameters) == 1:
            super(GoogleCloudBetaSTT, self).__init__(config)
        else:
            LOG.warning(f"Shorter Signature Found; config will be ignored!")
            super(GoogleCloudBetaSTT, self).__init__()
        # override language with module specific language selection
        self.queue = None

        if self.credential:
            if not self.credential.get("json"):
                self.credential["json"] = self.credential
            LOG.debug(f"Got credentials: {self.credential}")
            credentials = Credentials.from_service_account_info(
                self.credential.get('json')
            )
        else:
            import os
            cred_file = os.path.expanduser("~/.local/share/neon/google.json")
            if os.path.isfile(cred_file):
                credentials = Credentials.from_service_account_file(cred_file)
            else:
                credentials = None
        self.client = speech.SpeechClient(credentials=credentials)

    def execute(self, audio, language=None, alt_langs=None):
        start_time = time()
        try:
            flac_data = AudioData(audio.get_flac_data(), audio.sample_rate, audio.sample_width)
            new_audio = speech.RecognitionAudio(content=flac_data.frame_data)
        except Exception as e:
            LOG.error(e)
            LOG.debug("<p>Error: %s</p>" % e)
            new_audio = None
        if not language:
            language = 'en-US'

        LOG.debug(language)
        LOG.debug(alt_langs)
        config = speech.types.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            language_code=language,
            alternative_language_codes=alt_langs)

        # Detects speech in the audio file
        LOG.debug(config)
        response = None
        try:
            response = self.client.recognize(config=config, audio=new_audio)
            #            response = client.recognize(config, newAudio)
            LOG.debug(response)
        except google.api_core.exceptions.RetryError:
            LOG.error('google.api_core.exceptions.RetryError')
        except Exception as e:
            LOG.error(e)

        results = []
        if response:
            for result in response.results:
                results.append(result.alternatives[0].transcript)
                # language_detected = result.language_code
        else:
            LOG.error("Response is empty!")
        LOG.info(results)
        if hasattr(self, "server_bus") and self.server_bus:
            transcribe_time = time() - start_time
            stt_name = repr(self.__class__.__name__)
            print(f"{stt_name} | time={transcribe_time}")

            self.server_bus.emit(Message("neon.metric", {"name": "stt execute",
                                                         "transcripts": results,
                                                         "time": transcribe_time,
                                                         "module": stt_name}))
        return results

