from collections import deque

N = 5
K, M = map(int, input().split())
g = []
for _ in range(N):
    g.append(list(map(int, input().split())))

newer = deque(list(map(int, input().split())))
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def bfs(x, y, num, g):
    q = deque()
    q.append((x, y))
    count = 0
    while q:
        x, y = q.popleft()
        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            if not visited[nx][ny] and g[nx][ny] == num:
                q.append((nx, ny))
                visited[nx][ny] = 1
                count += 1

    return count


def rotate(cdd):
    i = cdd[3]-1
    j = cdd[2]-1
    d = cdd[1]
    for x in range(i, i + 3):
        for y in range(j, j + 3):
            # 영점으로 옮김
            ox, oy = x - i, y - j
            # 90도 회전
            if d == 0:
                rx, ry = oy, 3 - ox - 1
            # 180도 회전
            elif d == 1:
                rx, ry = 3 - ox - 1, 3 - oy - 1
            else:
                rx, ry = 3 - oy - 1, ox
            new_arr[rx + i][ry + j] = g[x][y]

    # g_copy 완성
    for x in range(i, i + 3):
        for y in range(j, j + 3):
            g[x][y] = new_arr[x][y]


for k in range(K):
    answer = 0
    # 탐사 진행
    # 격자 선택 (i, j)는 필터의 좌상단
    r_cdd = []
    for i in range(N - 2):
        for j in range(N - 2):
            g_copy = [ar[:] for ar in g]
            new_arr = [[0 for _ in range(N)] for _ in range(N)]
            for d in range(3):
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        # 영점으로 옮김
                        ox, oy = x - i, y - j
                        # 90도 회전
                        if d == 0:
                            rx, ry = oy, 3 - ox - 1
                        # 180도 회전
                        elif d == 1:
                            rx, ry = 3 - ox - 1, 3 - oy - 1
                        else:
                            rx, ry = 3 - oy - 1, ox
                        new_arr[rx + i][ry + j] = g[x][y]

                # g_copy 완성
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        g_copy[x][y] = new_arr[x][y]

                visited = [[0 for _ in range(N)] for _ in range(N)]
                total_size = 0
                for x in range(N):
                    for y in range(N):
                        if not visited[x][y]:
                            num = g_copy[x][y]
                            sz = bfs(x, y, num, g_copy)
                            if sz >= 3:
                                # print(x, y, sz)
                                total_size += sz

                r_cdd.append((total_size, d, j+1, i+1))

    r_cdd.sort(key=lambda l: (-l[0], l[1], l[2], l[3]))

    if r_cdd[0][0] == 0:
        break

    # 회전
    rotate(r_cdd[0])
    # print(g)

    while True:
        # disappear
        disappear = []
        visited = [[0 for _ in range(N)] for _ in range(N)]
        total_size = 0
        for x in range(N):
            for y in range(N):
                if not visited[x][y]:
                    num = g[x][y]
                    sz = bfs(x, y, num, g)
                    if sz >= 3:
                        total_size += sz
                        disappear.append((x, y))

        # 종료 조건
        if total_size == 0:
            break

        answer += total_size

        d_set = set()
        q = deque()
        visited = [[0 for _ in range(N)] for _ in range(N)]
        for x, y in disappear:
            num = g[x][y]
            q.append((x, y))
            while q:
                x, y = q.popleft()
                for d in range(4):
                    nx = x + dx[d]
                    ny = y + dy[d]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue
                    if not visited[nx][ny] and g[nx][ny] == num:
                        q.append((nx, ny))
                        visited[nx][ny] = 1
                        d_set.add((nx, ny))
        # print(d_set)

        for y in range(N):
            for x in range(N-1, -1, -1):
                if (x, y) in d_set:
                    val = newer.popleft()
                    g[x][y] = val

    print(answer, end=" ")