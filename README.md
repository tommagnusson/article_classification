# Article Classification for Quikfo
Manual Article Spam or Ham Classification program

<p align="center">
  <img width="600" src="https://cdn.rawgit.com/tommagnusson/article_classification/830a52b4/articleSVG.svg">
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

