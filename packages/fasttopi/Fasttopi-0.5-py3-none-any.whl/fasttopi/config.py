import yaml
import os
from os.path import abspath

def load_config():
    with open("config.yaml") as file:
        config= yaml.safe_load(file)
        return config

def get_holdout_percentage():
    config = load_config()
    return config['experiment']['holdout_percentage']

def get_path_dataset_dir():
    config = load_config()
    path_dataset = config["dataset"]["path_dir"]
    return path_dataset

def get_path_model(model_name):
    config = load_config()
    path_model = config[model_name]["path"]
    return path_model

def get_path_preprocessed_dataset():
    config = load_config()
    path_dataset_preprocessed = config["dataset"]["path_preprocessed"]
    return path_dataset_preprocessed

def get_path_source_dataset():
    config = load_config()
    path_source_dataset =  config["dataset"]["path_source"]
    return path_source_dataset


def get_sample_experiment_size():
    """
    Get the count of titles that will be used in the sample experiments
    :return: an Integer
    """
    config = load_config()
    return config['experiment-sample']['size']

def get_path_zip_dataset():
    config = load_config()
    path_zip_dataset = config["dataset"]["path_zip"]
    return path_zip_dataset

def get_pathes_experiment(sample=False):
    """
    Get the holdout and training split pathes of the sample experiment
    :return: a tuple including path of the holdout and the training splits
    """
    config = load_config()
    if sample:
        path_holdout = config["experiment-sample"]["path_holdout"]
        path_training =  config["experiment-sample"]["path_training"]
    else:
        path_holdout = config["experiment"]["path_holdout"]
        path_training =  config["experiment"]["path_training"]

    return path_holdout, path_training

def get_splits_count():
    config = load_config()
    return config["experiment"]["splits_count"]

def get_url_dataset():
    config = load_config()
    url_dataset = config["dataset"]["url"]
    return url_dataset

def get_hyper_parameter():
    config = load_config()
    all_cs = config["model"]["c"]
    return all_cs

def get_best_hyper_parameter():
    config = load_config()
    c= config["model"]["c_best"]
    return c

