import re

standart_dirt = 'хуй|бля|пизд'

def _get_search(pattern: str):
    """
    return function to search words with the pattern
    """
    def hide_search(word: str) -> bool:
        return bool(re.search(pattern, word))

    return hide_search


def is_dirt(pattern: str=standart_dirt):
    """
    return function to search pattern in text
    """
    funk = _get_search(pattern)

    def hide_search(text: str) -> bool:
        for word in re.findall(r'\w+', text):
            if funk(word.lower()):
                return True
        
        return False

    return hide_search

