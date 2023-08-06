from torch.utils.data import IterableDataset
import pandas as pd


class Q2StreamSubset(IterableDataset):
    def __init__(self, tsv, local_rank, n_replicas):
        """
        Query2的流式子数据集
        Args:
            tsv: 数据文件
            local_rank: rank index
            n_replicas: 共分为几个数据子集
        """
        super(Q2StreamSubset, self).__init__()
        self.tsv_file = tsv
        self.local_rank = local_rank
        self.n_replicas = n_replicas

    def row_gen(self):
        """
        通过pandas chunksize，流式读取数据
        Returns:
            iterator
        """
        reader = pd.read_csv(self.tsv_file, sep='\t', header=0, na_filter=False, iterator=True, chunksize=1)
        count = -1
        for chunk in reader:
            row = chunk.iloc[0]
            if row['visible'] == 0:
                continue
            count += 1
            if count % self.n_replicas == self.local_rank:
                yield row['q2']

    def __iter__(self):
        return self.row_gen()
