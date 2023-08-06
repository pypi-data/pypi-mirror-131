from torch.utils.data import Dataset
import pandas as pd


class Q2Dataset(Dataset):
    def __init__(self, file):
        """
        读取数据文件，并封装成dataset
        Args:
            file: 数据文件
        """
        super(Q2Dataset, self).__init__()
        df = pd.read_csv(file, sep='\t', header=0, na_filter=False)
        self.samples = df['q2'].map(lambda x: ''.join(x.split()))

    def __getitem__(self, item):
        return self.samples[item]

    def __len__(self):
        return len(self.samples)
