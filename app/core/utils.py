import re, os
# app/utils/spell_utils.py
try:
    from spellchecker import SpellChecker
    spell = SpellChecker()
    SPELL_CHECKER_AVAILABLE = True
except ImportError:
    SPELL_CHECKER_AVAILABLE = False

def autocorrect_text(text: str) -> str:
    if SPELL_CHECKER_AVAILABLE:
        return " ".join([spell.correction(word) for word in text.split()])
    else:
        return text


def clean_topic(text):
    cleaned = re.sub(
        r'^\s*(tell me about|what is|who is|describe|explain|write about|presentation on|presentation about|on)\s+', 
        '', text, flags=re.I
    )
    return cleaned.strip()

def cleanup_temp_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except:
        pass
