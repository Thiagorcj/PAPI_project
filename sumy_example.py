from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words



def resumindo(text,language,sentences_count):
    resumo = ''
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    
    stemmer = Stemmer(language)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)

    for sentence in summarizer(parser.document, sentences_count):
        resumo += f" {str(sentence)}"
    return resumo