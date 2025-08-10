# coding=utf-8
# 实现说明
#     算法选择：使用归并排序，因为它是稳定的排序算法（对于多字段排序很重要），且时间复杂度为O(n log n)。

# 多字段比较：
#     compare函数依次比较每个字段
#     如果字段值不同，立即返回比较结果
#     如果字段值相同，继续比较下一个字段
#     支持升序和降序排序

# 特殊处理：
#     处理字段缺失的情况（视为None）
#     None值被认为小于任何有值

# 使用方法：
#     传入要排序的数据列表（每个元素是字典）
#     指定排序字段和顺序，例如[("age", True), ("score", False)]表示先按age升序，再按score降序


def multi_field_sort(data, fields):
    """
    多字段排序的自定义实现
    参数:
        data: 要排序的数据列表，每个元素是一个字典
        fields: 排序字段列表，每个元素是元组 (字段名, 升序True/降序False)
    返回:
        排序后的新列表
    """
    if len(data) <= 1:
        return data.copy()

    # 分割阶段
    mid = len(data) // 2
    left = multi_field_sort(data[:mid], fields)
    right = multi_field_sort(data[mid:], fields)

    # 合并阶段
    return merge(left, right, fields)


def merge(left, right, fields):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if compare(left[i], right[j], fields) <= 0:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 添加剩余元素
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def compare(a, b, fields):
    """
    比较两个字典的多字段

    返回:
        -1: a < b
        0: a == b
        1: a > b
    """
    for field, ascending in fields:
        # 获取字段值，如果字段不存在则返回None
        val_a = a.get(field)
        val_b = b.get(field)

        # 处理None值情况（None被认为小于任何有值）
        if val_a is None and val_b is None:
            continue
        if val_a is None:
            return -1 if ascending else 1
        if val_b is None:
            return 1 if ascending else -1

        # 比较实际值
        if val_a < val_b:
            return -1 if ascending else 1
        if val_a > val_b:
            return 1 if ascending else -1

    # 所有字段都相等
    return 0


# 示例使用
if __name__ == "__main__":
    data = [
        {"name": "Alice", "age": 25, "score": 90},
        {"name": "Bob", "age": 30, "score": 85},
        {"name": "Charlie", "age": 25, "score": 95},
        {"name": "David", "age": 30, "score": 80},
        {"name": "Eve", "age": 22, "score": 88}
    ]

    # 先按age升序，再按score降序
    sorted_data = multi_field_sort(data, [("age", True), ("score", False)])

    print("排序结果:")
    for item in sorted_data:
        print(item)
