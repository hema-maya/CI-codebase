import random

# ==============================
# ENVIRONMENT RENDERER
# ==============================

def display_status(world, pos, n, facing_dir, score, sensors):
    print(f"\n--- World Map ---")
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            cell = world[(i, j)]
            if (i, j) == pos:
                row.append("A") # A for Agent
            elif cell["wampus"]: row.append("W")
            elif cell["pit"]: row.append("P")
            elif cell["gold"]: row.append("G")
            else: row.append(".")
        print(" ".join(row))

    print(f"Pos: {pos} | Facing: {facing_dir} | Score: {score}")

    percepts = []
    if sensors[pos]["stench"]: percepts.append("STENCH")
    if sensors[pos]["breeze"]: percepts.append("BREEZE")
    if sensors[pos]["glitter"]: percepts.append("GLITTER")
    if percepts: print(f">> Perceptions: {', '.join(percepts)}")
    print("-" * 25)

# ==============================
# CORE LOGIC
# ==============================

def get_adjacent(r, c, n):
    adj = []
    if r > 1: adj.append((r-1, c))
    if r < n: adj.append((r+1, c))
    if c > 1: adj.append((r, c-1))
    if c < n: adj.append((r, c+1))
    return adj

def update_sensors(world, sensors, n):
    for pos in sensors:
        sensors[pos]["stench"] = False
        sensors[pos]["breeze"] = False
    for (r, c), props in world.items():
        if props["wampus"]:
            for adj in get_adjacent(r, c, n): sensors[adj]["stench"] = True
        if props["pit"]:
            for adj in get_adjacent(r, c, n): sensors[adj]["breeze"] = True

def create_world():
    try:
        n = int(input("Enter grid size (min 4): "))
    except: n = 4
    n = max(4, n)

    world = {(i, j): {"wampus": False, "pit": False, "gold": False} for i in range(1, n+1) for j in range(1, n+1)}
    sensors = {(i, j): {"stench": False, "breeze": False, "glitter": False} for i in range(1, n+1) for j in range(1, n+1)}

    start = (1, 1)

    # Wumpus
    w_pos = (random.randint(1, n), random.randint(1, n))
    while w_pos == start: w_pos = (random.randint(1, n), random.randint(1, n))
    world[w_pos]["wampus"] = True

    # Gold
    g_pos = (random.randint(1, n), random.randint(1, n))
    while g_pos == start or world[g_pos]["wampus"]:
        g_pos = (random.randint(1, n), random.randint(1, n))
    world[g_pos]["gold"] = True
    sensors[g_pos]["glitter"] = True

    # Pits
    for pos in world:
        if pos != start and not world[pos]["wampus"] and not world[pos]["gold"]:
            if random.random() < 0.2: world[pos]["pit"] = True

    update_sensors(world, sensors, n)
    return n, world, sensors, start

def play_game():
    n, world, sensors, pos = create_world()
    dirs = ["UP", "RIGHT", "DOWN", "LEFT"]
    facing_idx = 1
    score = 100

    while True:
        display_status(world, pos, n, dirs[facing_idx], score, sensors)

        action = input("Action (f, l, r, g, s, q): ").lower()
        score -= 1 # Default action cost

        if action == 'f':
            r, c = pos
            offsets = {"UP":(-1,0), "DOWN":(1,0), "LEFT":(0,-1), "RIGHT":(0,1)}
            dr, dc = offsets[dirs[facing_idx]]
            new_r, new_c = r + dr, c + dc

            if 1 <= new_r <= n and 1 <= new_c <= n:
                pos = (new_r, new_c)
            else:
                print("\n** BUMP! -40 points **")
                score -= 40  # Penalty for hitting the wall

        elif action == 'l': facing_idx = (facing_idx - 1) % 4
        elif action == 'r': facing_idx = (facing_idx + 1) % 4
        elif action == 'g':
            if world[pos]["gold"]:
                print("\n*** GOLD RECOVERED! ***")
                score += 1000
                break
            else: print("\nNothing here.")
        elif action == 's':
            print(f"\nArrow fired {dirs[facing_idx]}!")
            score -= 10
            r, c = pos
            dr, dc = {"UP":(-1,0), "DOWN":(1,0), "LEFT":(0,-1), "RIGHT":(0,1)}[dirs[facing_idx]]
            curr = (r + dr, c + dc)
            hit = False
            while 1 <= curr[0] <= n and 1 <= curr[1] <= n:
                if world[curr]["wampus"]:
                    print("!!! SCREAM !!!")
                    world[curr]["wampus"] = False
                    update_sensors(world, sensors, n)
                    hit = True
                    break
                curr = (curr[0] + dr, curr[1] + dc)
            if not hit: print("Miss.")
        elif action == 'q': break

        # Death Checks
        if world[pos]["wampus"]:
            display_status(world, pos, n, dirs[facing_idx], score, sensors)
            print("\nGAME OVER: Eaten!")
            score -= 1000
            break
        if world[pos]["pit"]:
            display_status(world, pos, n, dirs[facing_idx], score, sensors)
            print("\nGAME OVER: Pit!")
            score -= 1000
            break
        if score <= 0:
            print("\nGAME OVER: Out of energy!")
            break

    print(f"\nFINAL SCORE: {score}")

if __name__ == "__main__":
    play_game()