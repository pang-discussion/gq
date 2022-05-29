from CBOW_model import CBOWModel
from input_data import InputData
import torch.optim as optim
from tqdm import tqdm

# hyper parameters
WINDOW_SIZE = 4  # 上下文窗口c
BATCH_SIZE = 64  # mini-batch
MIN_COUNT = 3  # 需要剔除的 低频词 的频
EMB_DIMENSION = 300  # embedding维度
LR = 0.02  # 学习率
NEG_COUNT = 5  # 负采样数


class Word2Vec:
    def __init__(self, input_file_name, fn1, fn2):
        self.fn1 = fn1
        self.fn2 = fn2
        self.data = InputData(input_file_name, MIN_COUNT)
        self.model = CBOWModel(self.data.word_count, EMB_DIMENSION)
        self.lr = LR
        self.optimizer = optim.SGD(self.model.parameters(), lr=self.lr)

    def train(self):
        print("CBOW Training......")
        pairs_count = self.data.evaluate_pairs_count(WINDOW_SIZE)
        print("pairs_count", pairs_count)
        batch_count = pairs_count / BATCH_SIZE
        print("batch_count", batch_count)
        for epoch in range(30):
            process_bar = tqdm(range(int(batch_count)))
        
            for i in process_bar:
                pos_pairs = self.data.get_batch_pairs(BATCH_SIZE, WINDOW_SIZE)
                pos_u = [pair[0] for pair in pos_pairs]
                pos_w = [int(pair[1]) for pair in pos_pairs]
                neg_w = self.data.get_negative_sampling(pos_pairs, NEG_COUNT)

                self.optimizer.zero_grad()
                loss = self.model.forward(pos_u, pos_w, neg_w)
                loss.backward()
                self.optimizer.step()

                if i * BATCH_SIZE % 100000 == 0:
                    self.lr = self.lr * (1.0 - 1.0 * i / batch_count)
                    for param_group in self.optimizer.param_groups:
                        param_group['lr'] = self.lr

            self.model.save_embedding(self.data.id2word_dict, self.fn1, self.fn2)


if __name__ == '__main__':
    w2v = Word2Vec(input_file_name='', fn1="embedding.npy", fn2='vocab.npy')
    w2v.train()
