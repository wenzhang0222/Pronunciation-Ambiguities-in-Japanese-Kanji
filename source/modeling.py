#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Homograph disambiguation training and evaluation."""

import csv
import glob
import logging
import statistics

from typing import Dict, List, Tuple

import nltk  # type: ignore
import sklearn.feature_extraction  # type: ignore
import sklearn.linear_model  # type: ignore


FeatureVector = Dict[str, str]
FeatureVectors = List[FeatureVector]


TRAIN_TSV = "data/train/*.tsv"


def _token_feature(tokens: List[str], index: int) -> str:
    if index < 0:
        return "[$]"
    if index >= len(tokens):
        return "[^]"
    else:
        token = tokens[index]
        return "[NUMERIC]" if token.isnumeric() else token.casefold()


def extract_features(
    sentence: str, homograph: str, index: int
) -> FeatureVector:
    """Extracts  feature vector for a single sentence."""
    # to find the target homograph word.
    tokens = nltk.word_tokenize(sentence)
    t = index
    # feature extraction.
    features: Dict[str, str] = {}
    features["t-1"] = _token_feature(tokens, t - 1)
    features["t-2"] = _token_feature(tokens, t - 2)
    features["t+1"] = _token_feature(tokens, t + 1)
    features["t+2"] = _token_feature(tokens, t + 2)
    features["t-2^t-1"] = f"{features['t-2']}^{features['t-1']}"
    features["t+1^t+2"] = f"{features['t+1']}^{features['t+2']}"
    features["t-1^t+1"] = f"{features['t-1']}^{features['t+1']}"
    return features


def extract_features_file(path: str) -> Tuple[FeatureVectors, List[str]]:
    """Extracts feature vectors for an entire TSV file."""
    features: FeatureVectors = []
    labels: List[str] = []
    with open(path, "r") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            labels.append(row["reading"])
            features.append(
                extract_features(
                    row["sentence"],
                    row["kanji"],
                    int(row["index"])
                )
            )
    return features, labels


def main() -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s", level="INFO")
    correct: List[int] = []
    size: List[int] = []
    for train_path in glob.iglob(TRAIN_TSV):
        vectorizer = sklearn.feature_extraction.DictVectorizer(dtype=bool)
        # Training.
        feature_vectors, y = extract_features_file(train_path)
        x = vectorizer.fit_transform(feature_vectors)
        # Here I'm using some lightly tuned hyperparameters.
        model = sklearn.linear_model.LogisticRegression(
            penalty="l1",
            C=10,
            solver="liblinear",
        )
        model.fit(x, y)
        dev_path = train_path.replace("/train/", "/dev/")
        # test_path = train_path.replace("/train/", "/test/")
        # Evaluation.
        feature_vectors, y = extract_features_file(dev_path)
        x = vectorizer.transform(feature_vectors)
        yhat = model.predict(x)
        assert len(y) == len(yhat), "Mismatched lengths"
        correct.append(sum(y == yhat))
        size.append(len(y))
    # Accuracies.
    logging.info("Micro-average accuracy:\t%.4f", sum(correct) / sum(size))
    accuracies = [c / s for (c, s) in zip(correct, size)]
    logging.info("Macro-average accuracy:\t%.4f", statistics.mean(accuracies))


if __name__ == "__main__":
    main()
