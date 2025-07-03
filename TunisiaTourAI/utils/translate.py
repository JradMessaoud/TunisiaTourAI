from deep_translator import GoogleTranslator

def translate_text(text, dest_lang):
    # deep-translator utilise 'english' et 'french' comme noms de langue
    lang_map = {'fr': 'french', 'en': 'english'}
    dest = lang_map.get(dest_lang, 'french')
    return GoogleTranslator(target=dest).translate(text) 