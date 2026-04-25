import heapq
from bfs import Graph

class AStarGraph(Graph):
    def get_heuristic(self, goal):
        heuristic = {}
        print(f"\n--- Enter Heuristics (Goal: {goal}) ---")
        for node in self.graph:
            if node == goal:
                heuristic[node] = 0
            else:
                while True:
                    try:
                        val = input(f"Enter Heuristic value for node '{node}': ")
                        heuristic[node] = int(val)
                        break
                    except ValueError:
                        print("Invalid input! Please enter an integer.")
        return heuristic

    def astar(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or Goal node not in graph.")
            return

        h_table = self.get_heuristic(goal)
        frontier = []
        # (f, g, node, path)
        heapq.heappush(frontier, (h_table[start], 0, start, [start]))

        best_g = {start: 0}
        explored = []
        iteration = 1

        print("\nIter | Fringe (Node : f) | Explored")
        print("-" * 60)

        while frontier:
            # --- CLEAN FRINGE DISPLAY LOGIC ---
            # 1. Only show the best 'f' for nodes NOT yet explored
            # 2. Only show the path that matches our 'best_g' record
            current_fringe_items = {}
            for f, g, n, p in frontier:
                if n not in explored:
                    # If we find a better g for the same node in the heap, update display
                    if n not in current_fringe_items or g < current_fringe_items[n][1]:
                        current_fringe_items[n] = (f, g)

            # Sort by f-value (first element of the tuple) for the display
            fringe_view = sorted([(n, f) for n, (f, g) in current_fringe_items.items()], key=lambda x: x[1])

            print(f"{iteration:>4} | {str(fringe_view):<45} | {explored}")

            f, g, node, path = heapq.heappop(frontier)

            # If we already reached this node with a cheaper path, skip processing
            if g > best_g.get(node, float('inf')):
                continue

            if node not in explored:
                explored.append(node)

            if node == goal:
                print("-" * 60)
                print("Total Cost (g):", g)
                print("Optimized Path:", " -> ".join(map(str, path)))
                return

            for child, cost in self.graph[node]:
                new_g = g + cost

                # Check if this new path is better than any previously found path
                if child not in best_g or new_g < best_g[child]:
                    best_g[child] = new_g
                    new_f = new_g + h_table[child]
                    heapq.heappush(frontier, (new_f, new_g, child, path + [child]))

            iteration += 1
        print("Goal not reachable")

def setup_graph(g):
    nodes_input = input("Enter all nodes (separated by space): ").split()
    for n in nodes_input:
        g.add_node(n)

    print("\nEnter edges in format 'u v cost'. Type 'done' to finish.")
    while True:
        entry = input("Edge (u v cost): ").strip()
        if entry.lower() == 'done': break
        try:
            parts = entry.split()
            if len(parts) == 3:
                u, v, cost = parts
                if g.add_edge(u, v, int(cost)):
                    print(f"Edge {u}-{v} added.")
                else:
                    print("Error: Ensure nodes exist.")
            else:
                print("Invalid format!")
        except ValueError:
            print("Invalid cost!")

if __name__ == "__main__":
    g = AStarGraph()
    setup_graph(g)

    while True:
        print("\n--- MENU ---")
        print("1  Display Graph\n2  A* Search\n3  Reset Graph\n4.Delete node \n5.Delete edge\n6.Exit")
        ch = input("Enter choice: ")
        if ch == '1':
            g.display()
        elif ch == '2':
            g.astar(input("Start: "), input("Goal: "))
        elif ch == '3':
            g = AStarGraph()
            setup_graph(g)
        elif ch == '4':
            g.delete_node(input("Node: "))

        elif ch == '5':
            u = input("From: ")
            v = input("To: ")
            g.delete_edge(u, v)

        elif ch == '6':
            print("End")
            break
        else:
            print("Invalid choice")