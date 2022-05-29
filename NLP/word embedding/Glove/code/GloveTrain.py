import torch
import torch.utils.data as tud  # Pytorch读取训练集需要用到torch.utils.data类
from collections import Counter
import numpy as np
import time
import math
import sys

from WordEmbeddingDataset import WordEmbeddingDataset
from GloveModel import GloveModel

EMBEDDING_SIZE = 50
MAX_VOCAB_SIZE = 6000
WINDOW_SIZE = 5

NUM_EPOCHS = 5
BATCH_SIZE = 10
LEARNING_RATE = 0.05

TEXT_SIZE = 20000000
LOG_FILE = "../logs/word2vec_pubmed-{}.log".format(EMBEDDING_SIZE)
WEIGHT_FILE = "../weights/word2vec_pubmed-{}.th".format(EMBEDDING_SIZE)


def getCorpus(filetype, size):
    if filetype == 'train':
        filepath = '../corpus/pubmed.txt'
    elif filetype == 'test':
        filepath = '../corpus/pubmed_test.txt'
    else:
        filepath = '../corpus/pubmed_val.txt'

    with open(filepath, "r", encoding='utf-8') as f:
        text = f.read()
        text = text.lower().split()
        text = text[: min(len(text), size)]
        vocab_dict = dict(Counter(text).most_common(MAX_VOCAB_SIZE - 1))
        # vocab_dict = dict(Counter(text).most_common()[100: MAX_VOCAB_SIZE+100 - 1])
        vocab_dict['<unk>'] = len(text) - sum(list(vocab_dict.values()))
        idx_to_word = list(vocab_dict.keys())
        word_to_idx = {word: ind for ind, word in enumerate(idx_to_word)}
        word_counts = np.array(list(vocab_dict.values()), dtype=np.float32)
        word_freqs = word_counts / sum(word_counts)
        print("Words list length:{}".format(len(text)))
        print("Vocab size:{}".format(len(idx_to_word)))
    return text, idx_to_word, word_to_idx, word_counts, word_freqs


def buildCooccuranceMatrix(text, word_to_idx):
    vocab_size = len(word_to_idx)
    maxlength = len(text)
    text_ids = [word_to_idx.get(word, word_to_idx["<unk>"]) for word in text]
    cooccurance_matrix = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    print("Co-Matrix consumed mem:%.2fMB" % (sys.getsizeof(cooccurance_matrix) / (1024 * 1024)))
    for i, center_word_id in enumerate(text_ids):
        window_indices = list(range(i - WINDOW_SIZE, i)) + list(range(i + 1, i + WINDOW_SIZE + 1))
        window_indices = [i % maxlength for i in window_indices]
        window_word_ids = [text_ids[index] for index in window_indices]
        for context_word_id in window_word_ids:
            cooccurance_matrix[center_word_id][context_word_id] += 1
        if (i + 1) % 1000000 == 0:
            print(">>>>> Process %dth word" % (i + 1))
    print(">>>>> Build co-occurance matrix completed.")
    return cooccurance_matrix


def buildWeightMatrix(co_matrix):
    xmax = 100.0
    weight_matrix = np.zeros_like(co_matrix, dtype=np.float32)
    print("Weight-Matrix consumed mem:%.2fMB" % (sys.getsizeof(weight_matrix) / (1024 * 1024)))
    for i in range(co_matrix.shape[0]):
        for j in range(co_matrix.shape[1]):
            weight_matrix[i][j] = math.pow(co_matrix[i][j] / xmax, 0.75) if co_matrix[i][j] < xmax else 1
        if (i + 1) % 1000 == 0:
            print(">>>>> Process %dth weight" % (i + 1))
    print(">>>>> Build weight matrix completed.")
    return weight_matrix


def asMinutes(s):
    h = math.floor(s / 3600)
    s = s - h * 3600
    m = math.floor(s / 60)
    s -= m * 60
    return '%dh %dm %ds' % (h, m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / percent
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))


if __name__ == '__main__':
    text, idx_to_word, word_to_idx, word_counts, word_freqs = getCorpus('train', size=TEXT_SIZE)  # 加载语料及预处理
    co_matrix = buildCooccuranceMatrix(text, word_to_idx)  # 构建共现矩阵
    weight_matrix = buildWeightMatrix(co_matrix)  # 构建权重矩阵
    dataset = WordEmbeddingDataset(co_matrix, weight_matrix)  # 创建dataset
    dataloader = tud.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    model = GloveModel(MAX_VOCAB_SIZE, EMBEDDING_SIZE)  # 创建模型
    optimizer = torch.optim.Adagrad(model.parameters(), lr=LEARNING_RATE)  # 选择Adagrad优化器

    print_every = 10000
    save_every = 50000
    epochs = NUM_EPOCHS
    iters_per_epoch = int(dataset.__len__() / BATCH_SIZE)
    total_iterations = iters_per_epoch * epochs
    print("Iterations: %d per one epoch, Total iterations: %d " % (iters_per_epoch, total_iterations))

    start = time.time()
    for epoch in range(epochs):
        loss_print_avg = 0
        iteration = iters_per_epoch * epoch
        for i, j, co_occur, weight in dataloader:

            iteration += 1
            optimizer.zero_grad()  # 每一批样本训练前重置缓存的梯度
            loss = model(i, j, co_occur, weight)  # 前向传播
            loss.backward()  # 反向传播
            optimizer.step()  # 更新梯度
            loss_print_avg += loss.item()

            if iteration % print_every == 0:
                time_desc = timeSince(start, iteration / total_iterations)
                iter_percent = iteration / total_iterations * 100
                loss_avg = loss_print_avg / print_every
                loss_print_avg = 0
                with open(LOG_FILE, "a") as fout:
                    fout.write("epoch: %d, iter: %d (%.4f%%), loss: %.5f, %s\n" %
                               (epoch, iteration, iter_percent, loss_avg, time_desc))
                print("epoch: %d, iter: %d/%d (%.4f%%), loss: %.5f, %s" %
                      (epoch, iteration, total_iterations, iter_percent, loss_avg, time_desc))
            if iteration % save_every == 0:
                torch.save(model.state_dict(), WEIGHT_FILE)
    torch.save(model.state_dict(), WEIGHT_FILE)
