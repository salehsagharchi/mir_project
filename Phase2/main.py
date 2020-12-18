import os
import pickle
import click
from Phase2 import Parser
from Phase2.Parser import TextNormalizer as Normalizer, TextNormalizer
from Phase2 import Constants
from Phase2.DataModels import Document



def prompt_from_list(options: list, prompt_msg="Please Select One Option"):
    n = len(options)
    click.secho("\n:: ", nl=False, fg="green")
    click.echo(prompt_msg)
    for i in range(1, n + 1):
        click.secho(" " + str(i) + " ", nl=False, fg="blue")
        click.echo(options[i - 1])
    choice = click.prompt(
        click.style('> ', fg='green'),
        type=click.IntRange(1, n),
        prompt_suffix="",
    )
    print("\n")
    return choice - 1


class Main:

    def __init__(self, stopword_dir: str, docs_dir: str, tedtalks_raw_train: str, tedtalks_raw_test: str):
        self.stopword_dir = stopword_dir
        self.docs_dir = docs_dir
        self.tedtalks_raw_train = tedtalks_raw_train
        self.tedtalks_raw_test = tedtalks_raw_test
        self.parser: Parser.DocParser = Parser.DocParser(stopword_dir, docs_dir, tedtalks_raw_train, tedtalks_raw_test)

    # def initialize_classes(self):
    #     print("Loading files ...")
    #     try:
    #         Preferences.load_pref()
    #         Indexer.load_index()
    #         Bigram.load_file()
    #     except AttributeError:
    #         pass

    def parsing_files(self):
        self.parser.parse_tedtalks()

    def stopword_remove(self):
        self.parser.remove_stopwords("en")

    # def bigram_search(self):
    #     bi = input("please enter a bigram: ")
    #     if len(bi) != 2:
    #         print("invalid input")
    #         return False
    #     print(Bigram.get_terms_of_bigram(bi))

    # def create_index(self):
    #     Indexer.add_files()
    #     print("positional index was created successfully!")

    # def get_posting_list(self):
    #     term = input("please enter a term: ")
    #     term_norm = self.parser.prepare_query(term)[0]
    #     if len(term_norm) != 1:
    #         print("invalid input, please enter only one term")
    #         return
    #     term = term_norm[0]
    #     print("Normalized Term :", term)
    #     res = Indexer.get_docs_containing_term(term)
    #     if len(res) > 0:
    #         print(f"the term \"{term}\" has occurred in documents: {res}")
    #     else:
    #         print(f"the term \"{term}\" doesn't exist in index")

    # def get_positional_index(self):
    #     term = input("please enter a term: ")
    #     term_norm = self.parser.prepare_query(term)[0]
    #     if len(term_norm) != 1:
    #         print("invalid input, please enter only one term")
    #         return
    #     term = term_norm[0]
    #     print("Normalized Term :", term)
    #     if Indexer.index.get(term) is not None:
    #         print("doc id\tpositions")
    #         for posting in Indexer.index[term].keys():
    #             print(f"{posting}\t{Indexer.index[term][posting]}")
    #     else:
    #         print(f"the term \"{term}\" doesn't exist in index")

    # def save_via_var_byte(self):
    #     Preferences.pref[Constants.pref_compression_type_key] = Constants.VAR_BYTE_MODE
    #     Preferences.save_pref()
    #     space = Indexer.save_index()
    #     print("used space before compression: " + str(space[0]))
    #     print("used space after compression: " + str(space[1]))

    # def save_via_gama_codes(self):
    #     Preferences.pref[Constants.pref_compression_type_key] = Constants.GAMA_CODES_MODE
    #     Preferences.save_pref()
    #     space = Indexer.save_index()
    #     print("used space before compression: " + str(space[0]))
    #     print("used space after compression: " + str(space[1]))
    #
    # def jaccard(self):
    #     terms = input("please enter 2 terms separated by space: ").split(' ')
    #     if len(terms) != 2:
    #         print("invalid input")
    #         return
    #     bi_set1 = set([terms[0][i:i + 2] for i in range(len(terms[0]) - 1)])
    #     bi_set2 = set([terms[1][i:i + 2] for i in range(len(terms[1]) - 1)])
    #     print(f"Jaccard similarity between \"{terms[0]}\" and \"{terms[1]}\" is: {Bigram.jaccard_measure(bi_set1, bi_set2)}")
    #
    # def edit_distance(self):
    #     terms = input("please enter 2 terms separated by space: ").split(' ')
    #     if len(terms) != 2:
    #         print("invalid input")
    #         return
    #     print(f"Edit distance for \"{terms[0]}\" and \"{terms[1]}\" is: {Bigram.edit_distance_measure(terms[0], terms[1])}")
    #
    # def query(self):
    #     queryStatement = input("pls enter your query: ")
    #     score = Score()
    #     normalized_query = self.parser.prepare_query(queryStatement)
    #     queryTokens = normalized_query[0]
    #     print("Normalized query :", normalized_query[1])
    #     result = score.query(queryTokens)
    #     if result is not None:
    #         print(result[0:min(10, len(result))])

    # def printdoc(self):
    #     docid = input("Enter a document id : ")
    #     path = f"{self.docs_dir}/{docid}_fa.o"
    #     if not os.path.isfile(path):
    #         path = f"{self.docs_dir}/{docid}_en.o"
    #
    #     if not os.path.isfile(path):
    #         print(f"Couldn't find a document with id = {docid}")
    #         return
    #
    #     with open(path, "rb") as file:
    #         doc: Document = pickle.load(file)
    #         title = TextNormalizer.reshape_text(doc.title, "fa")
    #         toprint = f"\nDocument #{doc.docid} with title : {title}\n"
    #         map_object = map(lambda x: TextNormalizer.reshape_text(x, "fa"), doc.tokens)
    #         new_list = list(map_object)
    #         toprint += str(new_list)
    #     print(toprint)

    # def save(self):
    #     Preferences.save_pref()
    #     Indexer.save_index()
    #     Bigram.save_bigram()
    #     print("files were saved successfully!")

    def start(self):
        welcome_text = "Welcome to this application !"
        print(welcome_text)
        main_jobs = {
            "Parsing raw files and generating documents": self.parsing_files,
            "Removing stopwords": self.stopword_remove,
            "EXIT": -1
        }
        finish = False
        while not finish:
            job = prompt_from_list(list(main_jobs), "Please select a job you want to execute : ")
            command = list(main_jobs.values())[job]
            finish = command == -1
            if callable(command):
                command()


if __name__ == "__main__":
    my_main = Main(Constants.stopword_dir, Constants.docs_dir, Constants.tedtalks_raw_train, Constants.tedtalks_raw_test)
    my_main.start()