class SparseBitmap:
    def __init__(self, chunk_size=1024):
        self.bitmap = {}  # 使用字典存储稀疏块
        self.chunk_size = chunk_size  # 每块的大小

    def set(self, index):
        """设置某个位为1"""
        chunk_id = index // self.chunk_size
        offset = index % self.chunk_size
        if chunk_id not in self.bitmap:
            self.bitmap[chunk_id] = 0
        self.bitmap[chunk_id] |= (1 << offset)

    def is_set(self, index):
        """检查某个位是否为1"""
        chunk_id = index // self.chunk_size
        offset = index % self.chunk_size
        if chunk_id not in self.bitmap:
            return False
        return (self.bitmap[chunk_id] & (1 << offset)) != 0

    # 这一段似乎用不上，是用来清除的
    # def unset(self, index):
    #     """将某个位设置为0"""
    #     chunk_id = index // self.chunk_size
    #     offset = index % self.chunk_size
    #     if chunk_id in self.bitmap:
    #         self.bitmap[chunk_id] &= ~(1 << offset)
    #         if self.bitmap[chunk_id] == 0:  # 如果整个块为空，删除该块
    #             del self.bitmap[chunk_id]

def check_reservation_sparse(n, occupied_indices, l, r):
    # 初始化稀疏位图
    bitmap = SparseBitmap()
    for idx in occupied_indices:
        bitmap.set(idx)

    # 检查区间 [l, r]
    for i in range(l, r + 1):
        if not bitmap.is_set(i):  # 找到第一个未占用的位置
            return i
    return -1  # 如果区间已排满

# 示例
n = 1000000000  # 总范围
occupied_indices = [2, 3, 4, 7]  # 被占用的序号
l, r = 4, 7 # 要检查的区间
result = check_reservation_sparse(n, occupied_indices, l, r)
print("结果:", result)