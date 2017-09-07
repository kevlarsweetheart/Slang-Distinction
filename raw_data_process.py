import nltk
import pymorphy2 as pm
import re

class jl_line:
    def __init__(self, item):
        self.label = list(item.keys())[0]
        self.content = item.get(self.label)


    def get_tokens(self):
        tokenizer = nltk.TweetTokenizer()
        tokens = []
        for p in self.content:
            raw_tokens = self.clean_tokens(tokenizer.tokenize(p))
            while raw_tokens.count('.') != 0:
                bound = raw_tokens.index('.')
                sentence = raw_tokens[:bound]
                raw_tokens = raw_tokens[bound + 1:]
                tokens.append(sentence)
            if len(raw_tokens) != 0:
                tokens.append(raw_tokens)
        return tokens[:]


    def clean_tokens(self, tokens):
        bound = len(tokens)
        for i in range(bound):
            if not tokens[i].isalnum() and tokens[i] != '.':
                tokens[i] = '#'
            elif tokens[i].isalnum():
                check = re.search('\d|[a-zA-Z]', tokens[i])
                if check:
                    tokens[i] = '#'
                else:
                    tokens[i] = tokens[i].lower()
        while tokens.count('#') != 0:
            tokens.remove('#')
        return tokens[:]


    def normalize(self):
        morph = pm.MorphAnalyzer()
        sentences = self.get_tokens()
        bound = len(sentences)
        for i in range(bound):
            sent_len = len(sentences[i])
            for j in range(sent_len):
                sentences[i][j] = morph.parse(sentences[i][j])[0].normal_form
        return sentences[:]