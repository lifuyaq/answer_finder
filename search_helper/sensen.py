import heapq


def generate_dungeon(k):
    n, m = 10, 10  # 初始设定较小的地图大小
    dungeon = [['#' for _ in range(m)] for _ in range(n)]
    start, goal = (0, 0), (n - 1, m - 1)
    dungeon[0][0] = 'S'
    dungeon[n - 1][m - 1] = 'G'

    def neighbors(x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                yield nx, ny

    pq = [(0, 0, 0)]  # (步数, x, y)
    dist = {(0, 0): 0}

    while pq:
        d, x, y = heapq.heappop(pq)
        if (x, y) == goal and d == k:
            break
        for nx, ny in neighbors(x, y):
            if dungeon[nx][ny] == '#' and (nx, ny) not in dist:
                dist[(nx, ny)] = d + 1
                heapq.heappush(pq, (d + 1, nx, ny))
                dungeon[nx][ny] = '.'

    return n, m, dungeon


k = int(input())
n, m, dungeon = generate_dungeon(k)
print(n, m)
for row in dungeon:
    print(''.join(row))
