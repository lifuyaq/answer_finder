def max_flip_1d_fast(board, player='B'):
    n = len(board)
    max_flips = 0
    best_position = -1

    # 定义辅助函数计算单个方向的翻转数
    def count_flips(pos, direction):
        flips = 0
        i = pos + direction
        while 0 <= i < n and board[i] == ('W' if player == 'B' else 'B'):
            flips += 1
            i += direction
        # 如果遇到己方棋子，返回翻转数，否则无效
        if 0 <= i < n and board[i] == player:
            return flips
        return 0

    # 遍历所有空位
    for pos in range(n):
        if board[pos] == '.':  # 只能在空位落子
            # 计算左右方向的翻转数
            left_flips = count_flips(pos, -1)  # 向左检查
            right_flips = count_flips(pos, 1)  # 向右检查
            total_flips = left_flips + right_flips

            # 更新最大翻转数和位置
            if total_flips > max_flips:
                max_flips = total_flips
                best_position = pos

    return best_position, max_flips


# 示例棋盘
board = ".WBW.BBW"

# 计算最佳落子点
best_position, max_flips = max_flip_1d_fast(board, player='W')
print(f"最佳落子位置: {best_position}, 最大翻转数: {max_flips}")