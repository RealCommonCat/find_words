
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary


train = []
def lda_(lines):
    output=[]

    for line in lines:
        if line != '':
            line = line.split()
            train.append([w for w in line])
    dictionary = corpora.Dictionary(train)

    corpus = [dictionary.doc2bow(text) for text in train]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=20, passes=60)
    for topic in lda.print_topics(num_words = 20):
        termNumber = topic[0]
        listOfTerms = topic[1].split('+')
        for term in listOfTerms:
            listItems = term.split('*')
            output.append('  '+listItems[1]+'('+listItems[0]+')')
    return output