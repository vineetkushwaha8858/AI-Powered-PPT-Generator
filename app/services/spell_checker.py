"""
Advanced Spell Checker Service
File: app/services/spell_checker.py
Purpose: Check and fix spelling in all text
"""

from spellchecker import SpellChecker
import re

class AdvancedSpellChecker:
    """Comprehensive spell checking and correction"""
    
    def __init__(self):
        # Initialize spell checker
        self.spell = SpellChecker()
        
        # Add custom words (technical terms that should not be corrected)
        custom_words = {
            'ai', 'ppt', 'pptx', 'api', 'llm', 'nvidia', 'openai',
            'powerpoint', 'fastapi', 'python', 'javascript', 'chatgpt',
            'ml', 'dl', 'nlp', 'gpu', 'cpu', 'api', 'json', 'http'
        }
        self.spell.word_frequency.load_words(custom_words)
        
        # Manual corrections for common mistakes
        self.manual_corrections = {
            'hintory': 'history',
            'genrative': 'generative',
            'artifical': 'artificial',
            'intellegence': 'intelligence',
            'techinology': 'technology',
            'developement': 'development',
            'databse': 'database',
            'programing': 'programming',
            'machiene': 'machine',
            'algorythm': 'algorithm'
        }
    
    def fix_text(self, text):
        """
        Fix spelling in entire text
        Args:
            text (str): Input text
        Returns:
            str: Corrected text
        """
        if not text or not isinstance(text, str):
            return text
        
        # Apply manual corrections first
        corrected_text = self._apply_manual_corrections(text)
        
        # Then apply dictionary-based corrections
        corrected_text = self._apply_spell_check(corrected_text)
        
        return corrected_text
    
    def _apply_manual_corrections(self, text):
        """Apply manual correction rules"""
        corrected = text
        
        for wrong, correct in self.manual_corrections.items():
            # Word boundary pattern for whole words only
            pattern = re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE)
            
            def replace_match(match):
                original = match.group(0)
                # Preserve capitalization
                if original[0].isupper():
                    if original.isupper():
                        return correct.upper()
                    return correct.capitalize()
                return correct
            
            corrected = pattern.sub(replace_match, corrected)
        
        return corrected
    
    def _apply_spell_check(self, text):
        """Apply spell checking to text"""
        
        # Split into words while preserving structure
        words = re.findall(r'\b\w+\b|\W+', text)
        
        corrected_words = []
        
        for word in words:
            # Skip non-alphabetic (punctuation, spaces)
            if not word.strip() or not word[0].isalpha():
                corrected_words.append(word)
                continue
            
            word_lower = word.lower()
            
            # Check if word is correct
            if word_lower in self.spell:
                corrected_words.append(word)
            else:
                # Get correction
                correction = self.spell.correction(word_lower)
                
                if correction and correction != word_lower:
                    # Preserve original case
                    if word[0].isupper():
                        if word.isupper():
                            corrected = correction.upper()
                        else:
                            corrected = correction.capitalize()
                    else:
                        corrected = correction
                    
                    corrected_words.append(corrected)
                else:
                    # No correction found
                    corrected_words.append(word)
        
        return ''.join(corrected_words)
    
    def check_word(self, word):
        """Check if word is spelled correctly"""
        return word.lower() in self.spell
    
    def get_suggestions(self, word):
        """Get spelling suggestions for a word"""
        return list(self.spell.candidates(word.lower()))


# Global instance
spell_checker = AdvancedSpellChecker()
