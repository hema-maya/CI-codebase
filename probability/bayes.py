# Check condition for TOTAL HEADS
def check_total(count, cond_type, target):
    if cond_type == "equal":
        return count == target
    elif cond_type == "greater":
        return count > target
    elif cond_type == "less":
        return count < target
    return False

# Check specific coin (1st, 2nd, or 3rd)
def check_coin(value, target_side):
    # value is 'H' or 'T', target_side is 'h' or 't'
    return value.lower() == target_side.lower()

def bayes_coins():
    print("--- Bayes Rule: 3 Coins ---")

    print("\nDefine Event A (The outcome we want to find)")
    print("Type of A? (total / first / second / third): ")
    type_a = input().lower()
    print("Condition (If total: equal/greater/less | If coin: H/T): ")
    cond_a = input().lower()
    target_a = int(input("Enter target value (0-3 for total, 0 for specific coin): ")) if type_a == "total" else 0

    print("\nDefine Event B (The evidence/given condition)")
    print("Type of B? (total / first / second / third): ")
    type_b = input().lower()
    print("Condition (If total: equal/greater/less | If coin: H/T): ")
    cond_b = input().lower()
    target_b = int(input("Enter target value (0-3 for total, 0 for specific coin): ")) if type_b == "total" else 0

    count_B = 0
    count_A_and_B = 0

    # Generate all 8 outcomes for 3 coins
    sides = ['H', 'T']
    for c1 in sides:
        for c2 in sides:
            for c3 in sides:
                coins = (c1, c2, c3)
                total_heads = coins.count('H')

                # Evaluate A
                if type_a == "total":
                    A = check_total(total_heads, cond_a, target_a)
                elif type_a == "first": A = check_coin(c1, cond_a)
                elif type_a == "second": A = check_coin(c2, cond_a)
                else: A = check_coin(c3, cond_a)

                # Evaluate B
                if type_b == "total":
                    B = check_total(total_heads, cond_b, target_b)
                elif type_b == "first": B = check_coin(c1, cond_b)
                elif type_b == "second": B = check_coin(c2, cond_b)
                else: B = check_coin(c3, cond_b)

                if B:
                    count_B += 1
                    if A:
                        count_A_and_B += 1

    if count_B == 0:
        print("\nP(B) = 0 -> Bayes rule cannot be applied (Condition never happens)")
        return

    prob = count_A_and_B / count_B

    print("\n--- BAYES RESULT ---")
    print(f"Total possible outcomes: 8")
    print(f"Occurrences of Event B: {count_B}")
    print(f"Occurrences of A and B together: {count_A_and_B}")
    print(f"P(A | B) = {round(prob, 5)}")

bayes_coins()