# THREE COIN JOINT INFERENCE (TABLE FORM)

def input_table():
    print("Rows represent A = first two coins (HH, HT, TH, TT)")
    print("Columns represent B = third coin (H, T)\n")

    r = 4   # HH, HT, TH, TT
    c = 2   # H, T

    table = []

    print("Enter joint probability values:")

    for i in range(r):
        row = []
        for j in range(c):
            val = float(input(f"P(A{i}, B{j}) = "))
            row.append(val)
        table.append(row)

    return table, r, c


def print_table(table):
    print("\nJoint Probability Table:")
    for row in table:
        print(row)


# Marginal P(A)
def marginal_A(table, r, c):
    print("\n--- Marginal P(A) ---")
    for i in range(r):
        s = sum(table[i][j] for j in range(c))
        print(f"P(A{i}) = {s}")


# Marginal P(B)
def marginal_B(table, r, c):
    print("\n--- Marginal P(B) ---")
    for j in range(c):
        s = sum(table[i][j] for i in range(r))
        print(f"P(B{j}) = {s}")


# Conditional P(A|B)
def conditional_A_given_B(table, r, c):
    i = int(input("Enter row index i (0-3): "))
    j = int(input("Enter column index j (0-1): "))

    joint = table[i][j]
    pb = sum(table[x][j] for x in range(r))

    print("\nStep 1: P(Ai, Bj) =", joint)
    print("Step 2: P(Bj) =", pb)

    if pb == 0:
        print("Cannot divide by zero")
        return

    print(f"Step 3: P(A{i} | B{j}) = {joint/pb}")


# Conditional P(B|A)
def conditional_B_given_A(table, r, c):
    i = int(input("Enter row index i (0-3): "))
    j = int(input("Enter column index j (0-1): "))

    joint = table[i][j]
    pa = sum(table[i][x] for x in range(c))

    print("\nStep 1: P(Ai, Bj) =", joint)
    print("Step 2: P(Ai) =", pa)

    if pa == 0:
        print("Cannot divide by zero")
        return

    print(f"Step 3: P(B{j} | A{i}) = {joint/pa}")


# MENU (SAME AS YOURS)
def menu():
    table, r, c = input_table()
    print_table(table)

    while True:
        print("\n===== MENU =====")
        print("1. Marginal P(A)")
        print("2. Marginal P(B)")
        print("3. Conditional P(A|B)")
        print("4. Conditional P(B|A)")
        print("5. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            marginal_A(table, r, c)
        elif choice == 2:
            marginal_B(table, r, c)
        elif choice == 3:
            conditional_A_given_B(table, r, c)
        elif choice == 4:
            conditional_B_given_A(table, r, c)
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice")


# RUN
menu()