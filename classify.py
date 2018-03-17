import pandas as pd
import numpy as np
import argparse

# Creates a loop where users are served articles
# and stock symbols, and are asked if the given title is either
# - "s" for Spam
# - "h" for Ham
class ManualClassifier:

    def __init__(self, csv_file):
        self.file = csv_file

    # Classify the actual news articles
    def loop(self):
        # original csv, the one that should be mutated when saved
        df = pd.read_csv(self.file, index_col=['article_id'])

        # number of titles classified so far
        classifiedSoFar = df.dropna().spam

        csfCount = classifiedSoFar.count()
        csfPct = csfCount / df.title.count() * 100
        pctSpam = classifiedSoFar[classifiedSoFar == 'h'].count() / csfCount * 100
        pctHam = classifiedSoFar[classifiedSoFar == 's'].count() / csfCount * 100

        # all the rows we have left [t]o [c]lassify
        tc = df[pd.isnull(df.spam)].sample(frac=1)

        head('Welcome to Spam or Ham! Article titles are either spam or ham. Classify them.')
        ok(f'Classified {csfCount} articles ({csfPct} percent).')
        ok(f'{pctSpam} percent spam, {pctHam} percent ham')
        for t in tc.title:
            row = tc[tc.title.isin([t])]

            classification = self.__spamOrHam(t, list(row.symbol), list(row.url), df)
            if(classification == 's'):
                warn('Looks like some spam.')
            else:
                ok('Delicious ham.')

            # mutate the actual file
            df.at[df.title.isin([t]), 'spam'] = classification


    # Takes user input, s or h, for the given article title.
    # Handles invalid input by running the function again
    def __spamOrHam(self, title, stock, url, df):
        normal(f'{stock}\n{url}\n{title}')
        classification = input('Spam (s) or Ham (h)? Save (w) or exit (e):')
        if(classification == 'w'):
            self.__saveFile(df)
            return self.__spamOrHam(title, stock, url, df)
        if(classification == 'e'):
            self.__saveFile(df)
            exit()
            return;
        if(classification not in ['s', 'h']):
            # recurse if the wrong input's given
            fail('\nLooks like you didn\'t enter s(pam), h(am), or e(xit).\nTry entering one of those')
            return self.__spamOrHam(title, stock, url, df)
        return classification

    # make sure to save the results of the csv
    def __saveFile(self, df):
        normal(f'Saving {self.file}...')
        df.to_csv(self.file, encoding='utf-8')
        ok(f'{self.file} saved!')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file',
                        help='The path to the csv file containing the articles, with a column for spam or ham.')

    args = parser.parse_args()
    csv_file = args.file

    classifier = ManualClassifier(csv_file)
    classifier.loop()

# Color the terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def console(string, color):
    print(color + string + bcolors.ENDC)

def warn(string):
    console(string, bcolors.WARNING)

def head(string):
    console(string, bcolors.HEADER)

def normal(string):
    console(string, bcolors.OKBLUE)

def ok(string):
    console(string, bcolors.OKGREEN)

def fail(string):
    console(string, bcolors.FAIL)



if __name__ == '__main__':
    main()
