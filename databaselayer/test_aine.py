import pandas as pd

from itertools import chain

start = [1,3,5]
end = [2,4,5]
gene = 'GENE'
df = pd.DataFrame({'G':gene, 'Start':start,'End':end})


start_ls = ['3606 5599 6312 7897 8781 9893 11336 14271', '2394', '84 1046', '1', '1']
start_ls_ls = [['3606','5599','6312','7897','8781','9893','11336','14271'], ['2394'], ['84,1046'], ['1046'], ['1']]
####
end_ls = ['3666 5691 6581 8076 9095 10001 11493 16639', '3680', '137 1186', '45', '94']
end_ls_ls =   [['3666','5691','6581','8076','9095','10001','11493','16639'], ['3680'], ['137','1186'], ['45'], ['94']]
####
gene_id = ['AB022430', 'AB024537', 'AB043103', 'AB051349', 'AB051628']

#df1 = pd.DataFrame({'ID':gene_id, 'end':end_ls, 'start':start_ls})


df2 = pd.DataFrame({'ID':gene_id, 'end':end_ls_ls, 'start':start_ls_ls})

new = [(gene_id, v) for gene_id, val in zip(gene_id, start_ls_ls) for v in val]



new1 = [(item, v) for item, val in zip(new, end_ls_ls) for v in val]

new2 = [(ID, v1, v2) for ID, val1, val2 in zip(gene_id, start_ls_ls, end_ls_ls) for v1, v2 in zip(val1, val2)]

for item in new2:
    print(item)

