from math import sqrt

from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_selection import SelectKBest, chi2
import matplotlib.pyplot as plt

from Phase3.TFIDF import TFIDF
from Phase3.Constants import *
from Phase3.Utils import *
from Phase3.word2vec import *


class HierarchicalClustering:
    vector_list = list()
    link_list = list()
    reference_label_list = list()
    label_list = list()

    @classmethod
    def start(cls, vectorization_mode=TFIDF_MODE):
        cls.label_list = list()
        if vectorization_mode == TFIDF_MODE:
            TFIDF.start()
            cls.link_list = TFIDF.link_list
            cls.vector_list = TFIDF.document_vector_list
            cls.reference_label_list = TFIDF.reference_label_list
        elif vectorization_mode == WORD2VEC_MODE:
            w2v = Word2vec(2, 50, 3, 3, 1)
            cls.vector_list, cls.link_list, cls.reference_label_list = w2v.createVectorsOfSentenceByPath(FARSI_DOCUMENTS_PATH)

    @classmethod
    def get_k(cls):
        return int(sqrt(len(cls.link_list))) + 1

    @classmethod
    def cluster(cls, vectors=None, vectorization_mode=TFIDF_MODE):
        if vectors is None:
            vectors = cls.vector_list
        hc = AgglomerativeClustering(n_clusters=cls.get_k(), affinity='euclidean', linkage='ward')
        cls.label_list = hc.fit_predict(vectors)
        cls.write_results_to_file(vectorization_mode)

    @classmethod
    def write_results_to_file(cls, mode):
        if mode == TFIDF_MODE:
            path = HIERARCHICAL_TFIDF_RESULT_FILE
        elif mode == WORD2VEC_MODE:
            path = HIERARCHICAL_WORD2VEC_RESULT_FILE
        else:
            return
        write_to_file(path, cls.link_list, cls.label_list, cls.reference_label_list)

    @classmethod
    def read_results_from_file(cls, vectorization_mode=TFIDF_MODE):
        cls.link_list = list()
        cls.label_list = list()
        cls.reference_label_list = list()
        path = HIERARCHICAL_TFIDF_RESULT_FILE
        if vectorization_mode == WORD2VEC_MODE:
            path = HIERARCHICAL_WORD2VEC_RESULT_FILE
        with open(path, mode='r', encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0 and (line_count % 2 == 0):
                    cls.link_list.append(row[0])
                    cls.label_list.append(int(row[1]))
                    cls.reference_label_list.append(row[2])
                    pass
                line_count += 1

    @classmethod
    def select_k_best_features(cls, k):
        return SelectKBest(chi2, k=k).fit_transform(cls.vector_list, cls.reference_label_list)

    @classmethod
    def evaluate(cls):
        return evaluate_clustering(cls.label_list, cls.reference_label_list)

    @classmethod
    def get_graphical_results(cls, vectorization_mode=TFIDF_MODE):
        cls.start(vectorization_mode)
        k_list = []
        purity_list = []
        ARI_list = []
        NMI_list = []
        AMI_list = []

        cls.cluster(vectorization_mode=vectorization_mode)
        evaluation = evaluate_clustering(cls.label_list, cls.reference_label_list)
        k = len(cls.vector_list[0])
        k_list.append(k)
        purity_list.append(evaluation['purity'])
        ARI_list.append(evaluation['ARI'])
        NMI_list.append(evaluation['NMI'])
        AMI_list.append(evaluation['AMI'])
        k = int(k / 1.2)

        while k > cls.get_k():
            new_vectors = cls.select_k_best_features(k)
            cls.cluster(vectors=new_vectors, vectorization_mode=vectorization_mode)
            evaluation = evaluate_clustering(cls.label_list, cls.reference_label_list)
            k_list.append(k)
            purity_list.append(evaluation['purity'])
            ARI_list.append(evaluation['ARI'])
            NMI_list.append(evaluation['NMI'])
            AMI_list.append(evaluation['AMI'])
            print(k, evaluation)
            k = int(k / 1.2)

        plt.plot(k_list, purity_list, label='purity')
        plt.plot(k_list, ARI_list, label='ARI (adjusted rand index)')
        plt.plot(k_list, NMI_list, label='NMI (normalized mutual info)')
        plt.plot(k_list, AMI_list, label='AMI (adjusted mutual info)')
        plt.ylim(0, 1)
        plt.xlabel('vector size')
        plt.legend()
        plt.text(k, 0.9, f'number of clusters = {cls.get_k()}')
        plt.title('changes w.r.t. number of features selected')
        if vectorization_mode == TFIDF_MODE:
            plt.savefig('data/hierarchical_tfidf_plot_1.png')
        elif vectorization_mode == WORD2VEC_MODE:
            plt.savefig('data/hierarchical_word2vec_plot_1.png')
        plt.close()

    @classmethod
    def save_graphical_results(cls, vectorization_mode=TFIDF_MODE):
        cls.start(vectorization_mode)
        k_list = []
        purity_list = []
        ARI_list = []
        NMI_list = []
        AMI_list = []

        k = 10
        while k <= 500:
            new_vectors = cls.select_k_best_features(k)
            cls.cluster(vectors=new_vectors, vectorization_mode=vectorization_mode)
            evaluation = evaluate_clustering(cls.label_list, cls.reference_label_list)
            k_list.append(k)
            purity_list.append(evaluation['purity'])
            ARI_list.append(evaluation['ARI'])
            NMI_list.append(evaluation['NMI'])
            AMI_list.append(evaluation['AMI'])
            print(k, evaluation)
            k += 8

        with open("data/hierarchical_tfidf_metrics.csv", mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["k", "purity", "ARI", "NMI", "AMI"])
            for i in range(len(k_list)):
                csv_writer.writerow([k_list[i], purity_list[i], ARI_list[i], NMI_list[i], AMI_list[i]])



if __name__ == '__main__':
    HierarchicalClustering.save_graphical_results()