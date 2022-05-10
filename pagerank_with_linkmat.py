import numpy as np
THRESHOLD = 1e-8
Prob = 0.2

def load_link_mat(f,Len = 8298):
    num = 0
    link_mat = [[i, 0, []] for i in range(0, Len + 1)]
    with open(f) as file:
        lines = file.readlines()
        for line in lines:
            split = line.split()
            fm, to = int(split[0]), int(split[1])
            num = max(num, max(fm, to))
            link_mat[fm][1] += 1
            link_mat[fm][2].append(to)
    return link_mat
def linkmatmul(Node_Num, orank,link_matrix):
    nrank = [0] * Node_Num
    for entry in link_matrix:
        for destination in entry[2]:
            nrank[destination] += orank[entry[0]] / entry[1]
    return nrank
def pagerank(num, link_mat):    
    old = [1 / float(num)] * num
    round = 0
    while True:
        # 矩阵乘法得到r_new
        new = linkmatmul(num, old,link_mat)
        # 标准化
        new = [i + (1 - float(sum(new))) / float(num) for i in new]
        # r_new*beta+（1-beta）/N
        new = [i * (1 - Prob) + Prob / float(num) for i in new]
        if np.sum(abs(np.array(old)-np.array(new))) <= THRESHOLD * num or round == 1000:
            print("拟合完成", round)
            return new
        else:
            old = new
            round += 1

if __name__ == "__main__":
    d = load_link_mat('data.txt',8298)
    r = pagerank(8298, d)
    sort_result = dict(zip(np.argsort(-np.array(r)), sorted(np.array(r), reverse=True)))