"""
google translator API
"""
import json
from .constants import BASE_URLS, PAPAGO_LANGUAGE_TO_CODE
from .exceptions import TranslationNotFound
from .base import BaseTranslator
import requests


class PapagoTranslator(BaseTranslator):
    """
    class that wraps functions, which use google translate under the hood to translate text(s)
    """

    def __init__(self, client_id=None, secret_key=None, source="auto", target="en", **kwargs):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        if not client_id or not secret_key:
            raise Exception(
                "Please pass your client id and secret key! visit the papago website for more infos")

        self._base_url = BASE_URLS.get("PAPAGO_API")
        self.client_id = client_id
        self.secret_key = secret_key
        super().__init__(
            source=source,
            target=target,
            languages=PAPAGO_LANGUAGE_TO_CODE,
            **kwargs
        )

    def translate(self, text, **kwargs):
        """
        function that uses google translate to translate a text
        @param text: desired text to translate
        @return: str: translated text
        """

        payload = {
            "source": self._source,
            "target": self._target,
            "text": text
        }
        headers = {
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.secret_key,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        response = requests.post(
            self._base_url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(
                f'Translation error! -> status code: {response.status_code}')
        res_body = json.loads(response.text)
        if "message" not in res_body:
            raise TranslationNotFound(text)

        msg = res_body.get("message")
        result = msg.get("result", None)
        if not result:
            raise TranslationNotFound(text)
        translated_text = result.get("translatedText")
        return translated_text

    def translate_file(self, path, **kwargs):
        """
        translate directly from file
        @param path: path to the target file
        @type path: str
        @param kwargs: additional args
        @return: str
        """
        return self._translate_file(path, **kwargs)

    def translate_batch(self, batch=None, **kwargs):
        """
        translate a list of texts
        @param batch: list of texts you want to translate
        @return: list of translations
        """
        return self._translate_batch(batch, **kwargs)
