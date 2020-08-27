def importFasttext():
    try:
        import fasttext as ft
    except ImportError:
        ft = None
    
    if not ft:
        raise ImportError("Couldn't import fasttext.")

    return ft

def importNltk():
    try:
        from nltk.tokenize import word_tokenize as wt
        print("INFO: import nltk.tokenize.word_tokenize function")
    except ImportError:
        wt = None

    if not wt:
        raise ImportError("Couldn't import nltk.tokenize.word_tokenize function.")
    
    return wt

