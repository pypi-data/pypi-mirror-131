import csv
import numpy as np
import pandas as pd
import urllib.request
import zipfile
from config import *

class Set:
    def __init__(self,titles, labels):
        self.titles = titles
        self.labels = np.array(labels)


def download_dataset(url_dataset, path_zip_dataset):
    urllib.request.urlretrieve(url_dataset, path_zip_dataset)

def unpack_dataset(path_zip_dataset,path_dataset_dir):
    if not os.path.exists(path_dataset_dir):
        os.mkdir(path_dataset_dir)
    with zipfile.ZipFile(path_zip_dataset, 'r') as zip_ref:
        zip_ref.extractall(path_dataset_dir)

def remove_zip():
    path_zip_dataset = get_path_zip_dataset()
    os.remove(path_zip_dataset)

def dataset_exist(path_source_dataset):
    return os.path.exists(path_source_dataset)

def get_dataset():
    path_source_dataset = get_path_source_dataset()
    if not dataset_exist(path_source_dataset):
        path_dataset = get_path_dataset_dir()
        url_dataset = get_url_dataset()
        path_zip_dataset = get_path_zip_dataset()

        if not os.path.exists(path_zip_dataset):
            download_dataset(url_dataset,path_zip_dataset)
        unpack_dataset(path_zip_dataset,path_dataset)
        remove_zip()

def preprocess_dataset():
    path_preprocessed_dataset = get_path_preprocessed_dataset()
    path_source_dataset = get_path_source_dataset()
    dataset_df= pd.read_csv(path_source_dataset,sep="\t",encoding="utf-8",names=["id","title","url","publisher","category","story","hostname","timestamp"],quoting=csv.QUOTE_NONE)
    dataset_df['label']=dataset_df['category'].apply(get_label)
    dataset_df['title']=dataset_df['title'].apply(lambda x: x.lower())
    dataset_df[['title','label']].to_csv(path_preprocessed_dataset,sep="\t",encoding="utf-8",index=False)

def load_dataset(sample_size=None,zip_dataset=False):
    path_preprocessed_dataset = get_path_preprocessed_dataset()
    if not os.path.exists(path_preprocessed_dataset):
        get_dataset()
        preprocess_dataset()

    dataset_df = pd.read_csv(path_preprocessed_dataset,sep="\t",encoding="utf-8")
    if sample_size != None:
        dataset_df = dataset_df.sample(sample_size)

    if zip_dataset:
        dataset = Set(titles=dataset_df['title'].values, labels=dataset_df['label'].values)
        return dataset
    else:
        return dataset_df


def get_label(category):
    if category == "e":
        return 0
    elif category =="b":
        return 1
    elif category =="t":
        return 2
    elif category =="m":
        return 3
    else:
        raise ValueError("Unrecognized category")

def get_descriptive_category(label):
    if label==0:
        return "entertainment"
    elif label==1:
        return "business"
    elif label==2:
        return "tech"
    elif label==3:
        return "health"
    else:
        raise ValueError("Unrecognized label")