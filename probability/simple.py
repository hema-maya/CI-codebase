def coin_probability(target_heads, condition):
    # 1. Generate all outcomes for 3 coins (2 * 2 * 2 = 8 total)
    # H = Head, T = Tail
    outcomes = []
    for c1 in ['H', 'T']:
        for c2 in ['H', 'T']:
            for c3 in ['H', 'T']:
                outcomes.append((c1, c2, c3))

    total = len(outcomes) # 8
    favorable = 0

    # 2. Check each outcome
    for combo in outcomes:
        # Count how many 'H' are in this specific combination
        heads_count = combo.count('H')

        if condition == "equal" and heads_count == target_heads:
            favorable += 1
        elif condition == "greater" and heads_count > target_heads:
            favorable += 1
        elif condition == "less" and heads_count < target_heads:
            favorable += 1

    probability = favorable / total

    # 3. Print Results
    print(f"\nAll possible outcomes: {outcomes}")
    print("Total outcomes:", total)
    print(f"Outcomes matching '{condition} {target_heads} heads':", favorable)
    print("Probability:", round(probability, 5))


# ---- USER INPUT ----
print("--- 3 Coin Flip Probability ---")
target = int(input("Enter target number of Heads: "))

print("Choose condition: equal / greater / less")
choice = input().lower()

coin_probability(target, choice)