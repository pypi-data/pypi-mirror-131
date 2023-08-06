import torch
import numpy as np
import pandas as pd
import sys

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
from tqdm import tqdm
from typing import List, Union
from pathlib import Path


BATCH_SIZE = 30
BERT_DIM = 768
MAX_LENGTH = 256
METHOD = "complete"

def batchlines_to_vector(batch_lines: List[str], tokenizer, model):
    inputs = tokenizer(
            batch_lines, 
            return_tensors='pt',
            truncation=True,
            max_length=MAX_LENGTH,
            padding=True,
            add_special_tokens=True
            )

    out = model(input_ids = torch.tensor(inputs['input_ids']),
            attention_mask = torch.tensor(inputs['attention_mask']))

    pooler_output = out.pooler_output.detach().numpy()

    return pooler_output

def convert_lines_from_excel(file_path: Union[str, Path], line_idx: int, tokenizer, model):
    print("Converting strings to vectors")
    df = pd.read_excel(file_path, engine='openpyxl')
    lines = df.iloc[:, line_idx]
    N = len(lines)
    
    num_epoch = N // BATCH_SIZE
    converge_idx = num_epoch * BATCH_SIZE
    
    final_vectors = np.empty((0, BERT_DIM), int)
    
    batch_lines = []
    for line in tqdm(lines[:converge_idx], total=converge_idx):
        batch_lines.append(line.strip())
        if len(batch_lines) == BATCH_SIZE:
            batch_vectors = batchlines_to_vector(batch_lines, tokenizer, model)
            final_vectors = np.concatenate([final_vectors, batch_vectors])
            batch_lines = []
    
    if converge_idx < N:
        remaining_batch_lines = [line.strip() for line in lines[converge_idx:]]
        remaining_batch_vectors = batchlines_to_vector(remaining_batch_lines, tokenizer, model)

        final_vectors = np.concatenate([final_vectors, remaining_batch_vectors])

    assert N == final_vectors.shape[0], f"N:{N}, final_shape: {final_vectors.shape}"

    return final_vectors

def plot_dendogram(data):
    print("Processing Clustering")
    print("This could take a few minutes")
    plt.figure(figsize=(10, 7))
    plt.title("Dendograms")
    
    N = np.shape(data)[0]
    labelList = range(1, N+1)
    dend = dendrogram(linkage(data, method=METHOD), labels=labelList)
    plt.savefig('dendogram.png')
    print("Dendogram saved")

def predict_cluster_from_threshold(data, threshold: int):
    prediction = fcluster(linkage(data, method=METHOD),threshold,criterion='distance')
    return prediction

def save_prediction_to_excel(prediction, file_path: Union[str, Path], line_idx: int):
    df = pd.read_excel(file_path, engine='openpyxl')
    lines = df.iloc[:, line_idx]
    
    new_df = pd.DataFrame({"labels": prediction, "sent": lines})
    new_df.to_excel("predicted_result.xlsx")

if __name__ == "__main__":
    
    file_path = sys.argv[1]
    line_idx = int(sys.argv[2])
    mode = sys.argv[3]
    
    assert mode in ["predict", "plot"]
    
    from kobert_transformers import get_kobert_model, get_tokenizer
    tokenizer = get_tokenizer()
    model = get_kobert_model()
    
    result = convert_lines_from_excel(file_path, line_idx, tokenizer, model)
    
    if mode == "plot":
        plot_dendogram(result)
    elif mode == "predict":
        prediction = predict_cluster_from_threshold(result, 14)
        save_prediction_to_excel(prediction, file_path, line_idx)
        
