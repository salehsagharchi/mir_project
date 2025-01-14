import math
from Phase1.Indexer import Indexer
from Phase1.Bigram import Bigram
from Phase1.Parser import TextNormalizer


class Score:
    def __init__(self):
        self.id = 0
        self.baseLog = 2

    def query(self, terms):
        n = self.getN()
        correction = False
        for i in range(len(terms)):
            if not (terms[i] in Indexer.index.keys()):
                correction = True
                terms[i] = Bigram.get_best_alternative(terms[i])
        terms = list(filter(lambda x: x is not None, terms))
        if not terms:
            print("Cannot find a good document :)")
            return
        if correction:
            print("Your query is misspelled, alternative execution is :", TextNormalizer.reshape_text(" ".join(terms), "fa"))
        vectors = {}
        for i in range(len(terms)):
            df, documentIndex, frequencyTerm = self.collectInformationAboutTerm(terms[i])
            for j in range(len(documentIndex)):
                if documentIndex[j] not in list(vectors):
                    vectors[documentIndex[j]] = [0 for k in range(len(terms))]
                vectors[documentIndex[j]][i] = (1 + math.log(frequencyTerm[j], self.baseLog)) * math.log(n / df,
                                                                                                         self.baseLog)
                # vectors[documentIndex[j]][i] = (1 + math.log(frequencyTerm[j], self.baseLog)) * math.log(n / df,
                #                                                                                          self.baseLog)
        for i in list(vectors):
            vectors[i] = self.normalizeVector(vectors[i])
        scores = self.calculateScore(self.createQueryVector(terms), vectors)
        sorted_scores = sorted(scores, reverse=True, key=lambda x: x[1])
        return sorted_scores

    def calculateScore(self, qVector, dVectors):
        result = [[0 for i in range(2)] for j in range(len(dVectors))]
        count = 0
        for i in list(dVectors):
            result[count] = [i, self.dotVectors(qVector, dVectors[i])]
            count += 1
        return result

    def dotVectors(self, firstVector, secondVector):
        result = 0
        for i in range(len(firstVector)):
            result += firstVector[i] * secondVector[i]
        return result

    def normalizeVector(self, vector):
        sum = 0
        for i in range(len(vector)):
            sum += math.pow(vector[i], 2)
        if sum == 0:
            return vector
        normal = 1 / math.sqrt(sum)
        for i in range(len(vector)):
            vector[i] = vector[i] * normal
        return vector

    def createQueryVector(self, terms):
        vector = [0] * len(terms)
        for i in range(len(terms)):
            tf = self.findFrequency(terms, terms[i])
            vector[i] = 1 + math.log(tf, self.baseLog)
        return self.normalizeVector(vector)

    def findFrequency(self, terms, term):
        count = 0
        for i in range(len(terms)):
            if term == terms[i]:
                count += 1
        return count

    def getN(self):
        return Indexer.TOTAL_DOCS

    def collectInformationAboutTerm(self, term):
        df = Indexer.get_df(term)
        documentIndex = Indexer.get_docs_containing_term(term)
        frequencyTerm = []
        for i in documentIndex:
            frequencyTerm.append(Indexer.get_tf(term, i))
        return df, documentIndex, frequencyTerm
