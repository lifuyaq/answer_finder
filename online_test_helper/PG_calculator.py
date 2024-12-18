def generate_multiplication_dict():
    result_dict = {}

    for x in range(1, 11):
        for y in range(x + 1, 11):  # 从x+1开始，避免重复
            for z in range(y + 1, 11):  # 从y+1开始，保证z > y
                product = x * y * z
                # 只保存100到500之间的结果
                if 10 <= product <= 504:
                    # 如果key不存在，创建新列表
                    if product not in result_dict:
                        result_dict[product] = []
                    # 添加排序后的组合
                    result_dict[product].append((x, y, z))

    return result_dict


def solve_equation(n, plus=True):
    # 生成字典
    multiplication_dict = generate_multiplication_dict()

    solutions = []

    # 遍历字典中的每个乘积
    for product, combinations in multiplication_dict.items():
        if not plus:
            m = product - n
        else:
            m = n - product
        # 检查m是否在合理范围内
        if 1 <= m < 10:
            # 对于每个组合，添加解
            for combo in combinations:
                solutions.append((*combo, m))

    return solutions


# 测试函数
def performance_test(n, plus=True):
    import time

    start_time = time.time()
    results = solve_equation(n, plus=plus)
    end_time = time.time()

    if not plus:
        print(f"等式 x*y*z - m = {n} 的解:")
        for x, y, z, m in results:
            print(f"{x} * {y} * {z} - {m} = {n}")
    else:
        print(f"等式 x*y*z + m = {n} 的解:")
        for x, y, z, m in results:
            print(f"{x} * {y} * {z} + {m} = {n}")

    print(f"\n计算耗时: {end_time - start_time:.4f}秒")
    print(f"找到的解的数量: {len(results)}")


def main():
    while True:
        try:
            number = int(input("What's the number?"))
            plus = bool(input("Is it plus?If not enter nothing"))
            performance_test(number, plus=plus)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()