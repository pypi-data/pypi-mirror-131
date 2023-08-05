import logging

from cltl.combot.infra.resource.api import ResourceManager

from cltl.backend.api.microphone import AUDIO_RESOURCE_NAME
from cltl.backend.api.text_to_speech import TextToSpeech
from cltl.backend.spi.audio import AudioSource

logger = logging.getLogger(__name__)


class SynchronizedTextToSpeech(TextToSpeech):
    def __init__(self, tts: TextToSpeech, resource_manager: ResourceManager):
        """
        A SynchronizedMicrophone can be synchronized with other audio activity.

        Parameters
        ----------
        source: AudioSource
            The source of audio data
        resource_manager : ResourceManager
            Resource manager to manage access to the microphone resource
        """
        self._tts = tts
        self._resource_manager = resource_manager

    def start(self):
        return self._tts.start()

    def stop(self):
        return self._tts.start()

    def say(self, text: str):
        try:
            logger.debug("Await talking")
            with self._resource_manager.get_write_lock(AUDIO_RESOURCE_NAME):
                self._tts.say(text)
        except:
            logger.exception("Failed to convert text to speech")

    @property
    def is_talking(self) -> bool:
        return self._tts.is_talking

    @property
    def language(self) -> str:
        return self._tts.language
