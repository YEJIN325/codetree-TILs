from collections import deque

# l, n, q = map(int, input().split())
# chess = []
# for _ in range(l):
#     chess.append(list(map(int, input().split())))

# gmap = [[0 for _ in range(l)] for _ in range(l)]
# gisa = []
# for t in range(1, n+1):
#     r, c, h, w, k = map(int, input().split())
#     gisa.append([r-1, c-1, h, w, k, True])
#     for i in range(r-1, r+h-1):
#         for j in range(c-1, c+w-1):
#             gmap[i][j] = t

# dx = [-1, 0, 1, 0]
# dy = [0, 1, 0, -1]
# for _ in range(q):
#     i, d = map(int, input().split())
#     r, c, h, w, k, alive = gisa[i-1]

#     queue = deque()
#     queue.append((r, c))
#     move = True
#     route = deque()
#     while queue:
#         r, c = queue.popleft()
#         for x in range(r, r+h):
#             if move:
#                 for y in range(c, c+w):
#                     nx = x + dx[d]
#                     ny = y + dy[d]
#                     if chess[nx][ny] == 2:
#                         queue = deque()
#                         move = False
#                         continue
#                     if nx < 0 or nx >= l or ny < 0 or ny >= l:
#                         queue = deque()
#                         move = False
#                         continue
#                     if gmap[nx][ny] != i and gmap[nx][ny] > 0:
#                         if gmap[nx][ny] not in route:
#                             route.appendleft(gmap[nx][ny])
#                         num = gmap[nx][ny]-1
#                         queue.append((gisa[num][0], gisa[num][1]))

#     print(move)
#     # 기사 이동
#     if move:
#         for num in route:
#             num = num - 1
#             if gisa[num][5]:
#                 r, c, h, w, k, alive = gisa[num]
#                 for x in range(r, r+h):
#                     for y in range(c, c+w):
#                         nx = x + dx[d]
#                         ny = y + dy[d]
#                         if nx < 0 or nx > l or ny < 0 or ny > l:
#                             continue
#                         gmap[nx][ny] = num + 1
#                         gmap[x][y] = 0
#                 gisa[num][0] = r + dx[d]
#                 gisa[num][1] = c + dy[d]
        
#     print(gmap)

MAX_N = 31
MAX_L = 41
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

info = [[0 for _ in range(MAX_L)] for _ in range(MAX_L)]
bef_k = [0 for _ in range(MAX_N)]
r = [0 for _ in range(MAX_N)]
c = [0 for _ in range(MAX_N)]
h = [0 for _ in range(MAX_N)]
w = [0 for _ in range(MAX_N)]
k = [0 for _ in range(MAX_N)]
nr = [0 for _ in range(MAX_N)]
nc = [0 for _ in range(MAX_N)]
dmg = [0 for _ in range(MAX_N)]
is_moved = [False for _ in range(MAX_N)]


def try_move(idx, drt):
    q = deque()
    
    for i in range(1, n+1):
        dmg[i] = 0
        is_moved[i] = False
        nr[i] = r[i]
        nc[i] = c[i]

    q.append(idx)
    is_moved[idx] = True

    while q:
        x = q.popleft()

        nr[x] += dx[drt]
        nc[x] += dy[drt]

        if nr[x] < 1 or nr[x] + h[x] - 1 > l or nc[x] < 1 or nc[x] + w[x] - 1 > l:
            return False
        
        for i in range(nr[x], nr[x]+h[x]):
            for j in range(nc[x], nc[x]+w[x]):
                if info[i][j] == 1:
                    dmg[x] += 1
                if info[i][j] == 2:
                    return False
        
        for i in range(1, n+1):
            if is_moved[i] or k[i] <= 0:
                continue
            if r[i] > nr[x] + h[x] - 1 or nr[x] > r[i] + h[i] - 1:
                continue
            if c[i] > nc[x] + w[x] - 1 or nc[x] > c[i] + w[i] - 1:
                continue
            
            is_moved[i] = True
            q.append(i)
        
    dmg[idx] = 0
    return True


def move(idx, drt):
    if k[idx] <= 0:
        return
    
    if try_move(idx, drt):
        for i in range(1, n+1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]

            
l, n, q = map(int, input().split())
for i in range(1, l+1):
    info[i][1:] = map(int, input().split())
for i in range(1, n+1):
    r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    bef_k[i] = k[i]

for _ in range(q):
    idx, d = map(int, input().split())
    move(idx, d)

ans = sum([bef_k[i] - k[i] for i in range(1, n+1) if k[i] > 0])
print(ans)