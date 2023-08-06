import warnings
warnings.filterwarnings('ignore')
import argparse
from collections import namedtuple, defaultdict
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score, recall_score, precision_score
from config import *
from dataset import *
import os

from model import *

Split = namedtuple("Split", "test training")


class Metrics:
    def __init__(self, p, r, f1):
        self.p = p
        self.r = r
        self.f1 = f1

    def __repr__(self):
        return f"precision {self.p:2.2f}    recall {self.r:2.2f}       f1-score  {self.f1:2.2f}"

def select(titles, index):
    selected_titles = []
    for i in index:
        selected_titles.append(titles[i])
    return selected_titles


def split_dataset(dataset_df, holdout_perc):
    """
    Splits a given dataframe into two frames based on the holdout percentage.
    The holdout set will be sampled from the dataset using the holdout percentage while the training set will contain
    the rest of the dataset.

    :param dataset_df: dataframe to be split.
    :param holdout_perc: percentage of the holdout set.
    :return: split consisting of the holdout and the training sets.
    """
    holdout_df = dataset_df.sample(frac=holdout_perc)
    training_df = dataset_df[~dataset_df.index.isin(holdout_df.index)]
    return Split(test=holdout_df, training=training_df)


def calculate_metrics(labels, predictions, label):
    f1 = f1_score(labels, predictions, average=None, pos_label=label)
    precision = precision_score(labels, predictions, average=None, pos_label=label)
    recall = recall_score(labels, predictions, average=None, pos_label=label)
    return Metrics(p=precision, r=recall, f1=f1)


def calculate_effectiveness(model, test_set):
    """
    Calculates the precision, recall, and f1-score for the four labels and their macro-avareage.
    :param model: trained classifier model which takes strings as input and returns four labels
    :param test_set: test set to evaluate the model on
    :return: dictionary whose keys are the four labels and a 'macro' label and whose values are the
    precision, recall, and f1-score stored as Metrics
    """
    metrics = {}

    titles, labels = test_set.titles, test_set.labels
    predictions = predict(model, titles)

    f1s = f1_score(labels, predictions, average=None, labels=[0, 1, 2, 3])
    precisions = precision_score(labels, predictions, average=None, labels=[0, 1, 2, 3])
    recalls = recall_score(labels, predictions, average=None, labels=[0, 1, 2, 3])

    macro_f1_score = f1_score(labels, predictions, average='macro', labels=[0, 1, 2, 3])
    macro_precision = precision_score(labels, predictions, average='macro', labels=[0, 1, 2, 3])
    macro_recall = recall_score(labels, predictions, average='macro', labels=[0, 1, 2, 3])

    metrics['macro'] = Metrics(p=macro_precision, r=macro_recall, f1=macro_f1_score)

    for label, f1 in enumerate(f1s):
        metrics[label] = Metrics(p=precisions[label], r=recalls[label], f1=f1)

    return metrics


def average_metrics(splits_metrics):
    """
    Averages the metrics of a given split of the dataset. The splits are assumed to be of equal size and hence their
    average is not weighted
    :param splits_metrics:
    :return: dictionary whose keys are the four labels and a 'macro' label and whose values are the
    precision, recall, and f1-score stored as Metrics
    """

    average_metric = defaultdict(lambda: Metrics(p=0, r=0, f1=0))

    for split_metric in splits_metrics:
        for label in split_metric:
            average_metric[label].p = average_metric[label].p + split_metric[label].p
            average_metric[label].r = average_metric[label].r + split_metric[label].r
            average_metric[label].f1 = average_metric[label].f1 + split_metric[label].f1
    for label in average_metric:
        average_metric[label].p = average_metric[label].p / len(splits_metrics)
        average_metric[label].r = average_metric[label].r / len(splits_metrics)
        average_metric[label].f1 = average_metric[label].f1 / len(splits_metrics)

    return average_metric


def experiment_exists(sample=False):
    """
    Checks whether the holdout and training set of an experiment exists as files in the file system.
    :param sample: boolearn variable for whether to check the sample experiment or the main experiment
    :return: boolean variable indicating whether the experiment exists or not
    """
    path_holdout, path_training = get_pathes_experiment(sample)
    return os.path.exists(path_holdout) and os.path.exists(path_training)


def create_experiment(sample=False):
    """
    Creates a sample experiment with a training and test sets. The size of the test set depends on the holdout percentage
    In config.yaml. The sets will be stored in the configured path in config.yaml. An option for sampling the dataset can
    be set using the input parameter smpale.
    config.yaml.
    :param sample: boolearn variable for whether to create a sample experiment with the size in config.yaml
    :return: None
    """
    holdout_perc = get_holdout_percentage()
    path_holdout, path_training = get_pathes_experiment(sample)
    if sample:
        sample_experiment_size = get_sample_experiment_size()
        dataset_df = load_dataset(sample_experiment_size)
    else:
        dataset_df = load_dataset()
    dataset_df=dataset_df.sample(frac=1.0,random_state=85)
    split = split_dataset(dataset_df, holdout_perc)

    split.test.to_csv(path_holdout, sep="\t", encoding="utf-8")
    split.training.to_csv(path_training, sep="\t", encoding="utf-8")


def load_experiment(sample=False):
    """
    Loads the training and test sets for the experiment.
    :param sample: boolearn variable  for whether to loads the sample experiment
     or the main experiment.
    :return: a split the contains the test and training sets.
    """
    if not experiment_exists(sample):
        create_experiment(sample)
    path_holdout, path_training = get_pathes_experiment(sample)
    holdout_df = pd.read_csv(path_holdout, sep="\t", encoding="utf-8")
    training_df = pd.read_csv(path_training, sep="\t", encoding="utf-8")

    holdout = Set(titles=holdout_df['title'].values, labels=holdout_df['label'].values)
    training = Set(titles=training_df['title'].values, labels=training_df['label'].values)

    return Split(test=holdout, training=training)


def cross_validate(model, training_set, splits_count):
    """
    Runs a cross-validation experiments with a given split count for an input model. The training set stored in
    config.yaml will be divided into the input count of splits and the model will be trained and evaluated on
    each split.
    :param model: model to be evaluated.
    :param training_set to split into folds
    :param splits_count: count of splits to divide the trianing set into
    :return: average precision, recall, and f1_score for each label and the macro average after averaging them
    on all splits.
    """
    titles, labels = training_set.titles, training_set.labels
    kfold = KFold(n_splits=splits_count)
    indices = kfold.split(titles, labels)

    all_folds_metrics = []
    for training_index, test_index in indices:
        title_training, titles_test = select(titles, training_index), select(titles, test_index)
        labels_training, labels_test = labels[training_index], labels[test_index]

        training_fold_set = Set(titles=title_training, labels=labels_training)
        test_fold_set = Set(titles=titles_test, labels=labels_test)

        train_model(model, training_fold_set)

        metrics = calculate_effectiveness(model, test_fold_set)
        all_folds_metrics.append(metrics)
    averaged_metrics = average_metrics(all_folds_metrics)
    return averaged_metrics


def test(model, split):
    """
    Run an experiment on the holdout set after training it on the training set.

    :param model: model to be evaluated.
    :param split: split consisting of the holdout and the training sets
    :return: average precision, recall, and f1_score for each label and the macro average
    """
    training_set = split.training
    test_set = split.test
    train_model(model, training_set)
    metrics = calculate_effectiveness(model, test_set)
    return metrics


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action="store_true", help="run the experiment using the baseline")
    parser.add_argument("--train", action="store_true", help="train the model on the whole datasetand store it")
    parser.add_argument("--no-holdout", action="store_true", help="train the model only on the training set")
    parser.add_argument("--test", action="store_true",
                        help="train the model on the training set and test on the test dataset")
    parser.add_argument("--sample", action="store_true", help="use the sample dataset")
    parser.add_argument("--crossvalidate", action="store_true", help="run a cross validation experiment")
    args = parser.parse_args()
    return args


def validate_args(args):
    pass


def print_metrics(label_metrics):
    for label in label_metrics:
        print(f"{label:<5}          {label_metrics[label]}")

def main():
    args = parse_args()
    validate_args(args)

    if args.train:
        sample_size = get_sample_experiment_size()
        if args.no_holdout:
            split = load_experiment(args.sample)
            dataset= split.training
            path_model = get_path_model_training("model")
        else:
            if args.sample:
                dataset = load_dataset(sample_size, zip_dataset=True)
            else:
                dataset = load_dataset(zip_dataset=True)
            path_model = get_path_model("model")
        if args.baseline:
            model = create_baseline()
        else:
            c, max_iter = get_best_hyper_parameter()
            model = create_model(c, max_iter)
        train_model(model, dataset)
        print(path_model)
        dump_model(model, path_model)

    if args.crossvalidate:
        splits_count = get_splits_count()
        split = load_experiment(args.sample)
        training_set = split.training
        if args.baseline:
            model = create_baseline()
            metrics = cross_validate(model, training_set, splits_count)
            print_metrics(metrics)
        else:
            all_cs,all_max_iters = get_hyper_parameter()
            for max_iter in all_max_iters:
                for c in all_cs:
                    print(f"### Hyperparameter C {c}    max iteration {max_iter }    ###")
                    model = create_model(c, max_iter)
                    metrics = cross_validate(model, training_set, splits_count)
                    print_metrics(metrics)
                    print("####\n")

    if args.test:
        if args.baseline:
            model = create_baseline()
        else:
            c,max_iter = get_best_hyper_parameter()
            model = create_model(c, max_iter)
        split = load_experiment(args.sample)
        metrics = test(model, split)
        print_metrics(metrics)


if __name__ == '__main__':

    main()
