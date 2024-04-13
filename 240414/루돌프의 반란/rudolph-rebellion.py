def get_distance(rx, ry, sx, sy):
    return (rx - sx) ** 2 + (ry - sy) ** 2


def transaction(x, y, mx, my, num):
    # 벗어난 산타 탈락
    if x < 0 or x >= n or y < 0 or y >= n:
        if num > 0:
            santas[num - 1][4] = 1
            # print("탈락" + str(num))
        return

    now_num = board[x][y]
    board[x][y] = num
    santas[num - 1][0] = x
    santas[num - 1][1] = y

    # 칸에 산타가 없으면
    if board[x][y] == 0:
        return

    # 산타가 있으면
    transaction(x + mx, y + my, mx, my, now_num)


n, m, s, rp, sp = map(int, input().split())
board = [[0] * n for _ in range(n)]

rx, ry = map(int, input().split())
rx -= 1
ry -= 1

santas = [[] for _ in range(s)]
for i in range(s):
    si, sx, sy = map(int, input().split())
    board[sx - 1][sy - 1] = si
    santas[si - 1] = [sx - 1, sy - 1, si, 0, 0]  # 기절 여부, 탈락 여부

score = [0 for _ in range(s)]
for tt in range(m):
    # print("turn" + str(tt+1))
    rmove_log = [0, 0]
    # 루돌프 움직임
    s_cnt = len(santas)
    select_santa = []
    for i in range(s_cnt):
        if santas[i][4] == 0:
            d = get_distance(rx, ry, santas[i][0], santas[i][1])
            select_santa.append((d, santas[i][0], santas[i][1], santas[i][2]))

    select_santa.sort(key=lambda x: (x[0], -x[1], -x[2]))
    selected_sx = select_santa[0][1]
    selected_sy = select_santa[0][2]
    selected_sidx = select_santa[0][3]

    # 루돌프 돌진 방향 구하기
    drx = 0
    if selected_sx - rx > 0:
        drx = 1
    elif selected_sx - rx < 0:
        drx = -1

    dry = 0
    if selected_sy - ry > 0:
        dry = 1
    elif selected_sy - ry < 0:
        dry = -1

    # 루돌프 돌진
    rx = rx + drx
    ry = ry + dry
    rmove_log = [drx, dry]

    sdx = [-1, 0, 1, 0]
    sdy = [0, 1, 0, -1]
    smove_log = [[0, 0] for _ in range(s_cnt)]
    # 산타가 순서대로 움직임
    for i in range(s_cnt):
        # 기절한 산타 제외 + 게임 탈락
        if santas[i][3] == 1 or santas[i][4] == 1:
            continue
        sx = santas[i][0]
        sy = santas[i][1]

        # 산타 이동 방향 구하기
        min_d = get_distance(rx, ry, sx, sy)
        selected_sd = -1
        for d in range(4):
            nsx = sx + sdx[d]
            nsy = sy + sdy[d]
            if nsx < 0 or nsx >= n or nsy < 0 or nsy >= n:
                continue
            # 다른 산타가 있다면
            if board[nsx][nsy] > 0:
                continue

            tmp_d = get_distance(rx, ry, nsx, nsy)
            if min_d > tmp_d:
                min_d = tmp_d
                selected_sd = d

        # 산타 이동
        # print(i, selected_sd)
        if selected_sd != -1:
            nsx = sx + sdx[selected_sd]
            nsy = sy + sdy[selected_sd]

            santas[i][0] = nsx
            santas[i][1] = nsy

            santa_num = board[sx][sy]
            board[sx][sy] = 0
            board[nsx][nsy] = santa_num

            smove_log[i] = [sdx[selected_sd], sdy[selected_sd]]

    # print("충돌 전 산타 위치")
    # for i in range(n):
    #     for j in range(n):
    #         print(board[i][j], end=" ")
    #     print()

    # 신타와 루돌프 출돌 체크
    for i in range(s_cnt):
        x = santas[i][0]
        y = santas[i][1]
        if x == rx and y == ry:
            # 기절
            santas[i][3] = 2

            # 루돌프로 인해 충돌
            if rmove_log != [0, 0]:
                score[santas[i][2] - 1] += rp

                mx = rmove_log[0]
                my = rmove_log[1]

                # 산타 밀려남
                nx = x + mx * rp
                ny = y + my * rp

            # 산타로 인해 충돌
            else:
                # 반대 방향으로 밀려남
                score[santas[i][2] - 1] += sp
                mx = smove_log[i][0] * (-1)
                my = smove_log[i][1] * (-1)

                nx = x + mx * sp
                ny = y + my * sp

            now_num = board[x][y]
            board[x][y] = 0

            transaction(nx, ny, mx, my, now_num)

    # print("===============")
    # print("충돌 후 산타 위치")
    # for i in range(n):
    #     for j in range(n):
    #         print(board[i][j], end=" ")
    #     print()

    for i in range(s_cnt):
        if santas[i][3] > 0 and santas[i][4] == 0:
            santas[i][3] -= 1

    # print("============")
    # print("산타 상태 확인")
    # for i in range(s_cnt):
    #     print(santas[i])

    # 종료조건 체크
    isEnd = 0
    for i in range(s_cnt):
        if santas[i][4] == 1:
            isEnd += 1
    if isEnd == s_cnt:
        break

    # 탈락하지 않은 산타 점수 부여
    for i in range(s_cnt):
        if santas[i][4] == 0:
            score[i] += 1

for i in range(s_cnt):
    print(score[i], end=" ")