def check_reservation(n, m, occupied_indices, l, r):
    # 转换为集合，提高查找效率
    occupied_set = set(occupied_indices)

    # 遍历区间 [l, r]
    for i in range(l, r + 1):
        if i not in occupied_set:
            return i  # 返回第一个未被占用的序号

    # 如果区间全被占用
    return -1


# 示例
n = 10  # 总长度
m = 3  # 被占用的数量
occupied_indices = [2, 4, 7]  # 被占用的序号
l, r = 3, 6  # 闭区间

# 检查区间是否排满
result = check_reservation(n, m, occupied_indices, l, r)
print("结果:", result)