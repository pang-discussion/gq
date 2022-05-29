
包含了glove在PubMed和wikitext2上预训练的权重文件，以及经过处理后的vocab和embedding矩阵。

--glove_pubmed-50.th : 预训练的权重文件，训练了10个epoch，截取了PubMed文件的前2千万个单词作为训练集，
		        词嵌入的维度为50维，窗口大小为5，vocab大小为10000，其他细节见代码

--glove_pubmed_embeddings.npy ： 是一个二维的矩阵，对应了词汇的词嵌入

--glove_pubmed_vocab.npy : 是一个字典，对应的是‘单词’：词嵌入行号

--glove_wikitext-50.th : 预训练的权重文件，训练了10个epoch，截取了PubMed文件的前2千万个单词作为训练集，
		        词嵌入的维度为50维，窗口大小为5，vocab大小为2000，其他细节见代码

--glove_wikitext_embeddings.npy ： 是一个二维的矩阵，对应了词汇的词嵌入

--glove_wikitext_vocab.npy : 是一个字典，对应的是‘单词’：词嵌入行号