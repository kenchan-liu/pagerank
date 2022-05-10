import numpy as np
with open('data.txt') as file:
    lines = file.readlines()
LEN=8297+1
import numpy as np
mat = np.zeros((LEN,LEN))
for line in lines:
    split = line.split()
    i, j = eval(split[0]), eval(split[1])
    mat[i][j]=1
def GtoM(G, N):
    M = np.zeros((N, N))
    D = np.sum(G,axis=0)
    for i in range(N):
        for j in range(N):
            if D[j] == 0:
                continue
            M[i][j] = G[i][j] / D[j]
    return M

def PageRank(M, N, T=30000, eps=1e-6, beta=0.8):
    R = np.ones(N) / N
    teleport = np.ones(N) / N
    for time in range(T):
        R_new = beta * np.dot(M, R) + (1-beta)*teleport
        if np.linalg.norm(R_new - R) < eps:
            break
        R = R_new.copy()
    return R_new
if __name__ == "__main__":
    ans = GtoM(mat,LEN)
    rank = PageRank(ans,LEN)
