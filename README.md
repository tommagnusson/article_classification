# Article Classification for Quikfo
Manual Article Spam or Ham Classification program

<p align="center">
  <img width="600" src="https://raw.githubusercontent.com/tommagnusson/article_classification/master/articleSVG.svg" alt="example of article classification for Quikfo">
</p>

# Getting Started

## Dependencies

1. Install python3 (example is using homebrew on mac).
1. Install `pandas` and `numpy` using `pip`

```
$ brew install python3
$ python3 -m pip install numpy
$ python3 -m pip install pandas
```

## Running the program

1. Run the program with `spamScoredArticles.csv`, the file that contains the articles
1. Manually classify away

`$ python3 classify.py spamScoredArticles.csv`

## Exporting just the scored articles into separate CSV
Saves just the scored articles from the first csv into the second csv.

`$ python3 classify.py spamScoredArticles.csv --scored onlyScored.csv`
> Saves just the scored articles from `spamScoredArticles.csv` in `onlyScored.csv`

## Browser mode
Automatically open a google search of the stock symbol, as well as the article url.

`$ python3 classify.py spamScoredArticles.csv --browse`

## TODO
 - Auto close chrome tabs in `--browse` mode
