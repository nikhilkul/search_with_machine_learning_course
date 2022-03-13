import re
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv
from nltk import word_tokenize
from functools import lru_cache

nltk.download("punkt")

# Useful if you want to perform stemming.
import nltk

stemmer = nltk.stem.PorterStemmer()

categories_file_name = r"/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml"

queries_file_name = r"/workspace/datasets/train.csv"
output_file_name = r"/workspace/datasets/labeled_query_data.txt"

parser = argparse.ArgumentParser(description="Process arguments.")
general = parser.add_argument_group("general")
general.add_argument(
    "--min_queries",
    default=1,
    help="The minimum number of queries per category label (default is 1)",
)
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = "cat00000"

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find("id").text
    cat_path = child.find("path")
    cat_path_ids = [cat.find("id").text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(
    list(zip(categories, parents)), columns=["category", "parent"]
)

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[["category", "query"]]
df = df[df["category"].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.
@lru_cache
def clean_query(query, simple=False):
    if simple:
        return query.strip().lower()
    words = word_tokenize(query)
    words = [stemmer.stem(word.lower()) for word in words if (word.isalnum())]
    if len(words) == 0:
        return np.nan
    else:
        clean_query = " ".join(words)
    return clean_query


df["clean_query"] = df["query"].apply(clean_query)
df = df.dropna()

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.
df = df.join(parents_df.set_index("category"), on="category")
df["parent_g"] = df.groupby("parent")["clean_query"].transform(lambda x: len(set(x)))
df["cat_g"] = df.groupby("category")["clean_query"].transform(lambda x: len(set(x)))
df.loc[df["parent_g"] < min_queries, "drop"] = 1
df.drop(df.index[df["drop"] == 1], inplace=True)
print("How many unique cateogies: ", len(df["category"].unique()))
# Create labels in fastText format.
df["label"] = "__label__" + df["category"]

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df["category"].isin(categories)]
df["output"] = df["label"] + " " + df["query"]
df[["output"]].to_csv(
    output_file_name,
    header=False,
    sep="|",
    escapechar="\\",
    quoting=csv.QUOTE_NONE,
    index=False,
)
