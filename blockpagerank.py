import numpy as np
import pickle
def norm(lst):
    a = 0
    for i in lst:
        a += i
    ret = lst
    for i in range(0, len(ret)):
        ret[i] /= a
    return ret

def targetBlock(item, totalno, blocknum):
    return item // (((totalno + 1) // blocknum) + 1)
def load_data():
    totalno, link_mat, nodedic = 0, [[i, 0, []] for i in range(0, 8298)], {}
    with open("./data.txt",'rb') as file:
        lines = file.readlines()
        for line in lines:
            split = line.split()
            fm, to = int(split[0]), int(split[1])
            totalno = max(totalno, max(fm, to))
            link_mat[fm][1] += 1
            link_mat[fm][2].append(to)
            nodedic[fm] = nodedic[to] = 1
    print('load into link matrix')

    LinkMat = [[[i, 0, []] for i in range(0, 8298)]for j in range(0, 20)]
    for entry in link_mat:
        for item in entry[2]:
            index = targetBlock(item, 8297, 20)
            # print(aim_block_index)
            LinkMat[index][entry[0]][1] = entry[1]
            LinkMat[index][entry[0]][2].append(item)
    for i in range(20):
        name = 'linkmat' + str(i)
        f = open(name, "wb")
        pickle.dump(LinkMat[i],f)
    return LinkMat,len(nodedic.keys()),nodedic
    
def tostripe(num_in_group, dest):
        return dest - dest // num_in_group * num_in_group
def ranklist(num_in_group, nodedic, sno,node_num):
    r_ret = [0] * num_in_group
    for key in nodedic.keys():
        if key // num_in_group == sno:
            r_ret[tostripe(num_in_group,key)] = 0.3 / node_num
    return r_ret
def ManhDis(list1, list2):
    ret = 0
    for i in range(0, len(list1)):
        ret += abs(list1[i] - list2[i])
    return ret

def blockpagerank(lml,totalno, nodenum, nodedic):
    rold = [0] * (totalno + 1)
    for key in nodedic.keys():
        rold[key] = 0.2 / nodenum
    round = 0
    blocknum = 20
    totalno = totalno
    nodenum = nodenum
    num_in_group = totalno // blocknum + 1
    partrank = []
    while True:
        for b in range(0, blocknum):
            partrank.append(ranklist(num_in_group, nodedic, b,nodenum))
            with open('rankvector'+str(b), "wb") as f:
                pickle.dump(ranklist(num_in_group, nodedic, b,nodenum), f)
        for b in range(0, blocknum):
            rloc = partrank[b]
            f = open('linkmat'+str(b), "rb")
            lmlb = pickle.load(f)
            for entry in lmlb:
                for destination in entry[2]:
                    rloc[tostripe(num_in_group,destination)] += (1 - 0.2) * rold[entry[0]] / entry[1]
            partrank[b] = rloc
        rnew = []
        for b in range(0, blocknum):
            if b != blocknum - 1:
                rnew += partrank[b]
            else:
                rnew += partrank[b][0:tostripe(num_in_group,totalno) + 1]
        rnew = norm(rnew)
        if np.sum(abs(np.array(rold)-np.array(rnew))) < 0.01 or round==100:#拟合或者到100轮
            print("convergence at round", round)
            return rnew
        else:
            rold = rnew
            round += 1
if __name__ == "__main__":
    lml,MAX,ND = load_data()
    r = blockpagerank(lml,8298,6263,ND)
    sort_result = dict(zip(np.argsort(-np.array(r)), sorted(np.array(r), reverse=True)))
    f= open("result.txt",'w')
    for i in sort_result:
        f.write(str(i)+"\t"+str(sort_result[i])+'\n')