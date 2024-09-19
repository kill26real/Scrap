from tqdm import tnrange, tqdm
from time import sleep


for i in tqdm(range(10), desc='1 loop'):
    for j in tqdm(range(100), desc='2 loop'):
        sleep(0.01)
