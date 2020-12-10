import pandas as pd
group = pd.read_excel('1.xlsx', header=None)
group.columns = ['问题', '答案', '等级']
print(group)