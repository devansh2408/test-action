import os
import json
from deep_translator import GoogleTranslator

def translate_to_locale(text, target_locale):
    if isinstance(text,dict):
        return {key: translate_to_locale(value, target_locale) for key, value in text.items()}
    
    # Edge case handling for chinese
    if target_locale in ("zh-CN","zh-TW"):
        translator = GoogleTranslator(source='en', target=target_locale)
    else:
        translator = GoogleTranslator(source='en', target=target_locale.split('-')[0])

    return translator.translate(text)

def update_translated_data(existing_data, en_data, locale):
    for key, value in en_data.items():
        # If the key is missing in the existing data or the value is different and is a string, translate it.
        if key not in existing_data or (isinstance(value, str) and existing_data[key] != value):
            existing_data[key] = translate_to_locale(value, locale)
        # If the value is a dictionary, recurse.
        elif isinstance(value, dict):
            # Initialize a nested dictionary if the key does not exist
            if key not in existing_data or not isinstance(existing_data[key], dict):
                existing_data[key] = {}
            update_translated_data(existing_data[key], value, locale)
    return existing_data


def translate_json_to_locales(input_file, output_directory, locales):

    with open(input_file, 'r', encoding='utf-8') as file:
        en_data = json.load(file)
    for locale in locales:
        output_file = f"{locale.split('-')[0]}/translation.json"

        # Check if the translation file already exists
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as existing_file:
                existing_data = json.load(existing_file)

            # Translate only keys that are not present in the existing file
            translated_data = update_translated_data(existing_data, en_data, locale)
        else:

            output_dir = f"{locale.split('-')[0]}"
            # If the locale folder is not present create folder
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            
            # If the translation file doesn't exist, translate all keys
            translated_data = {key: translate_to_locale(value, locale) for key, value in en_data.items()}

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(translated_data, file, ensure_ascii=False, indent=2)

        print(f"Translation for {locale} saved to {output_file}")

if __name__ == "__main__":
    en_us_file = "extension/assets/locales/en/translation.json"
    output_dir = "extension/assets/locales"  # Change this to the desired output directory
    supported_locales = ["zh-CN", "es-ES", "de-DE"]
    translate_json_to_locales(en_us_file, output_dir, supported_locales)