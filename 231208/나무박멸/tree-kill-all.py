def grow():
    for i in range(n):
        for j in range(n): 
            if g[i][j] > 0:
                cnt = 0
                for d in range(4):
                    x = i + dx[d]
                    y = j + dy[d]
                    if x < 0 or x >= n or y < 0 or y >= n:
                        continue
                    if g[x][y] > 0 and zecho[x][y] == 0:
                        cnt += 1
                g[i][j] += cnt


def breed():
    tmp = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if g[i][j] > 0:
                trees = g[i][j]
                cnt = 0
                for d in range(4):
                    x = i + dx[d]
                    y = j + dy[d]
                    if x < 0 or x >= n or y < 0 or y >= n:
                        continue
                    # 제초제 없는 것도 추가해야 함
                    if g[x][y] == 0 and zecho[x][y] == 0:
                        cnt += 1
                if cnt > 0:
                    added = trees // cnt
                    for d in range(4):
                        x = i + dx[d]
                        y = j + dy[d]
                        if x < 0 or x >= n or y < 0 or y >= n:
                            continue
                        if g[x][y] == 0 and zecho[x][y] == 0:
                            tmp[x][y] += added

    for i in range(n):
        for j in range(n):
            g[i][j] += tmp[i][j]


def select_maxi():
    maxi = 0
    sx, sy = 0, 0
    for x in range(n):
        for y in range(n):
            if g[x][y] > 0:
                total = g[x][y]
                for dd in range(4):
                    for z in range(1, k+1):
                        nx = x + ddx[dd] * z
                        ny = y + ddy[dd] * z
                        if nx < 0 or nx >= n or ny < 0 or ny >= n:
                            continue
                        total += g[nx][ny]

                        if g[nx][ny] == -1 or g[nx][ny] == 0:
                            break

                if total > maxi:
                    sx = x
                    sy = y
                    maxi = total

    return sx, sy

                
def kill():
    global dead
    sx, sy = select_maxi()
    zecho[sx][sy] = c
    dead += g[sx][sy]
    g[sx][sy] = 0
    for dd in range(4):
        for z in range(1, k+1):
            nx = sx + ddx[dd] * z
            ny = sy + ddy[dd] * z
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            if g[nx][ny] == -1:
                break
            zecho[nx][ny] = c
            dead += g[nx][ny]
            
            if g[nx][ny] == 0:
                break
            
            g[nx][ny] = 0


def time_set():
    for i in range(n):
        for j in range(n):
            if zecho[i][j] > 0:
                zecho[i][j] -= 1


n, m, k, c = map(int, input().split())
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
ddx = [-1, 1, 1, -1]
ddy = [1, 1, -1, -1]
zecho = [[0 for _ in range(n)] for _ in range(n)]
g = []
for _ in range(n):
    g.append(list(map(int, input().split())))

dead = 0
for i in range(m):
    grow()
    breed()
    time_set()
    kill()
    

print(dead)