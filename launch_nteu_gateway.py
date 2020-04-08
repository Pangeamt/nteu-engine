import aiohttp
from typing import List, Dict
from nteu_gateway.server import Server
from nteu_gateway.translation_engine_adapter_base import (
    TranslationEngineAdapterBase
)


class FakeTranslationEngineAdapter(TranslationEngineAdapterBase):
    async def translate(self, texts: List[str], config: Dict) -> List[str]:
        host = config["translationEngineServer"]["host"]
        port = config["translationEngineServer"]["port"]

        url = f"http://{host}:{port}/mytranslation"
        params = {
            "texts": texts
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=params
            ) as resp:
                resp = await resp.json()
                translations = []
                for translation in resp["my_translations"]:
                    translations.append(translation["my_translation"])

        return translations


server = Server.run(
    config_path='/config.yml',
    translation_engine_adapter=FakeTranslationEngineAdapter()
)
