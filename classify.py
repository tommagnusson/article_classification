import pandas as pd # dataframes, for parsing csv
import numpy as np # required by numpy
import argparse # command line argument parsing
import webbrowser # chrome automation
from time import sleep

# Creates a loop where users are served articles
# and stock symbols, and are asked if the given title is either
# - "s" for Spam
# - "h" for Ham
class ManualClassifier:

    def __init__(self, csv_file, should_browse):
        self.file = csv_file
        self.should_browse = should_browse

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

            symbols = list(row.symbol)
            urls = list(row.url)
            if self.should_browse:
                ManualClassifier.browse(symbols, urls)
            classification = self.__spamOrHam(t, symbols, urls, df)
            if(classification == 's'):
                warn('Looks like some spam.')
            else:
                ok('Delicious ham.')

            # mutate the actual file
            df.at[df.title.isin([t]), 'spam'] = classification

    def export_scored(self, out_file):
        df = pd.read_csv(self.file, index_col=['article_id'])
        classifiedSoFar = df.dropna()
        ManualClassifier.saveFile(classifiedSoFar, out_file)

    # Takes user input, s or h, for the given article title.
    # Handles invalid input by running the function again
    def __spamOrHam(self, title, stock, url, df):
        normal(f'{stock}\n{url}\n{title}')
        classification = input('Spam (s) or Ham (h)? Save (w) or exit (e):')
        if(classification == 'w'):
            ManualClassifier.saveFile(df, self.file)
            return self.__spamOrHam(title, stock, url, df)
        if(classification == 'e'):
            ManualClassifier.saveFile(df, self.file)
            exit()
            return;
        if(classification not in ['s', 'h']):
            # recurse if the wrong input's given
            fail('\nLooks like you didn\'t enter s(pam), h(am), or e(xit).\nTry entering one of those')
            return self.__spamOrHam(title, stock, url, df)
        return classification

    # open web browser with a google search of the stocks
    # As well as the articles referenced
    def browse(stocks, urls):
        # prevent duplicates
        stocks = set(stocks)
        urls = set(urls)

        for s in stocks:
            webbrowser.open_new(f"https://www.google.com/search?q={s}+stock")
        sleep(0.5) # necessary for the processes to open correctly
        for u in urls:
            webbrowser.open_new_tab(u)

    # make sure to save the results of the csv
    def saveFile(df, file_name):
        normal(f'Saving {file_name}...')
        df.to_csv(file_name, encoding='utf-8')
        ok(f'{file_name} saved!')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('file',
                        help='The path to the csv file containing the articles, with a column for spam or ham.')
    parser.add_argument('-s', '--scored',
                        help='The name of the csv file to be created containing only the articles that are scored.')
    parser.add_argument('-b', '--browse',
                        help='Enable chrome to automatically open the link provided, as well as a description of the company.',
                        action='store_true', default=False)

    args = parser.parse_args()
    csv_file = args.file
    out_file = args.scored
    should_browse = args.browse

    classifier = ManualClassifier(csv_file, should_browse)
    if out_file:
        classifier.export_scored(out_file)
        exit()

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
