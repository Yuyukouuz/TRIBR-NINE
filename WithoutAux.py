def calculate_damage(atk, critic_rate, critic_multiplier, skill_multiplier):
    damage = atk * critic_rate * critic_multiplier * skill_multiplier + atk * (1 - critic_rate) * skill_multiplier
    damage /= 10000
    return damage

# 以雪谷为例，因为她攻击力最高，百分比攻击词条收益也最高
basic_atk = 358  # 攻击力
critic_rate = 0.05
critic_multiplier = 150    # 暴击倍率
# 技能倍率按2级斗争算
skill_multiplier = 9800

# 定义变量和增量
variables = ['TT_atk', 'TT_cri_r', 'TT_cri_m', 'TT_skill']
increments = [1] * 6 + [0.8] * 3  # 6次1，3次0.8

# 用于存储最大damage及其对应的组合
max_damage = 0
best_combination = None

# 递归函数遍历所有组合
def find_max_damage(current_combination, remaining_increments):
    global max_damage, best_combination

    if not remaining_increments:
        # 计算当前组合的damage
        TT_atk, TT_cri_r, TT_cri_m, TT_skill = current_combination

        # 计算属性值
        atk = basic_atk * (1 + 0.3334 * TT_atk) + 130 # 同调宝贝130攻击力为最终加算
        critic_rate_current = critic_rate + 0.32 + 0.15 * TT_cri_r # 全员到齐增加32%暴击率
        critic_multiplier_current = critic_multiplier + 50 * TT_cri_m #暴击率超过1时取1
        skill_multiplier_current = (skill_multiplier + 1400 * TT_skill)

        # 计算damage
        damage = calculate_damage(atk, critic_rate_current, critic_multiplier_current, skill_multiplier_current)

        # 更新最大damage和最佳组合
        if damage > max_damage:
            max_damage = damage
            best_combination = [round(x, 1) for x in current_combination]  # 保留一位小数
        return

    # 遍历所有变量分配增量
    for i, var in enumerate(variables):
        if current_combination[i] < 2.01:  # 每个变量最多增加3次
            current_combination[i] += remaining_increments[0]
            find_max_damage(current_combination, remaining_increments[1:])
            current_combination[i] -= remaining_increments[0]

# 初始化当前组合
initial_combination = [0, 0, 0, 0]  # 对应TT_atk, TT_cri_r, TT_cri_m, TT_skill

# 开始递归查找
find_max_damage(initial_combination, increments)

# 输出结果
print("最佳组合:", best_combination)
print("最大damage:", round(max_damage, 1))  # 保留一位小数
