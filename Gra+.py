
import os

# 你的成语文件路径
FILE_PATH = r"F:\tutorial\damoxing\RAG\成语大全.txt"


# 加载成语库
def load_idioms():
    if not os.path.exists(FILE_PATH):
        print(f"未找到文件：{FILE_PATH}，请确保文件存在")
        return []

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        idioms = [line.strip() for line in f if line.strip()]
    return idioms


idiom_list = load_idioms()


# 根据最后一个字查找下一个成语
def find_next_idiom(last_char, idioms):
    for idiom in idioms:
        if idiom.startswith(last_char):
            return idiom
    return None


# ====================== 第8章：成语接龙链 ======================
def idiom_chain(user_idiom):
    # 1. 检查是否在库中
    if user_idiom not in idiom_list:
        return f"❌ 成语【{user_idiom}】不在成语库中，游戏终止！", True

    # 2. 取最后一个字接龙
    last_char = user_idiom[-1]
    next_idiom = find_next_idiom(last_char, idiom_list)

    if not next_idiom:
        return f"❌ 没有以【{last_char}】开头的成语，游戏终止！", True

    # 3. 接龙成功
    return f"✅ {user_idiom} → {next_idiom}", False


# ====================== 交互运行 ======================
if __name__ == "__main__":
    if not idiom_list:
        exit()

    print("=== 成语接龙游戏（输入 exit 退出）===")
    print(f"已加载成语：{len(idiom_list)} 个")

    while True:
        user = input("\n请输入成语：").strip()
        if user.lower() == "exit":
            print("=== 退出游戏 ===")
            break

        res, stop = idiom_chain(user)
        print(res)

        if stop:
            print("=== 游戏结束 ===")
            break