language = {"afrikaans": "af", "arabic": "ar", "bengali": "bn", "bosnian": "bs", "catalan": "ca", "czech": "cs",
            "welsh": "cy", "danish": "da", "german": "de", "greek": "el", "australian": "en-au", "canadian": "en-ca",
            "british": "en-gb", "irish": "en-ie", "indian": "en-ie", "united kingdom british": "en-uk", "english": "en",
            "finnish": "fi", "spain spanish": "es-es", "united states spanish": "es-us", "canadian french": "fr-ca",
            "french": "fr-fr", "hindi": "hi", "croatian": "hr", "hungarian": "hu", "armenian": "hy", "korean": "ko",
            "italian": "it", "japanese": "jw", "dutch": "nl", "norwegian": "no", "portuguese": "pt-br", "russian": "ru",
            "slovak": "sk", "thai": "th", "filipino": "tl", "turkish": "tr", "ukrainian": "uk", "vietnamese": "vi",
            "chinese": "zh-cn"}

print(language.keys())
if "korean" in language.keys():
    print(language.get("korean"))