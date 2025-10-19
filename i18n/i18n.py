from i18n.zh import text as zh
from i18n.en import text as en
from i18n.ja import text as ja

SUPPORTED_LANGS = {
    "中文": "zh",
    "English": "en",
    "日本語": "ja"
}

class Translator:
    def __init__(self, lang="zh"):
        self.lang = lang
        self.texts = {
            "zh": zh,
            "en": en,
            "ja": ja
        }

    def t(self, section, key):
        return self.texts[self.lang].get(section, {}).get(key, f"[{section}.{key}]")

translator = Translator()
