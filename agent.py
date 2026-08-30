# agent.py
import heapq
from collections import deque
import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SimpleReflexAgent:
    def __init__(self):
        # No Memory
        pass

    def sense_and_act(self, percept: dict) -> str:
        """Simple Reflex Agent using strictly Condition-Action (IF-THEN) rules."""
        wall_ahead = percept.get('wall_ahead', False)
        food_here = percept.get('food_here', False)

        # Condition-Action Rules (IF-THEN Logic)
        if food_here:
            return 'suck'  # Food is available, then suck it up
        elif wall_ahead:
            return 'Left'  # test_suite is checking 'Left', 'Right', 'Up', 'Down'
        else:
            return 'Up'  # Forward going return 'Up'

class ModelBasedAgent:
    def __init__(self):
        # Internal State / keep the Memory
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        wall_ahead = percept.get('wall_ahead', False)
        food_here = percept.get('food_here', False)

        # Rule 1: Food is present -> Suck it up
        if food_here:
            action = 'suck'
        
        # Rule 2: Wall is ahead, use Memory (last_action) to determine next action
        elif wall_ahead:
            if self.last_action == 'Left':
                action = 'Down'
            elif self.last_action == 'Down':
                action = 'Right'
            elif self.last_action == 'Right':
                action = 'Up'
            else:
                action = 'Left'
        
        # Rule 3: there is no wall ahead and no food, just move forward (Up)
        else:
            action = 'Up'

        # Store Action in Memory
        self.last_action = action
        return action

class SearchAgent:
    def __init__(self):
        self.plan = []  # Step 1.3: Stores planned actions
        self.active_algo = 'BFS'  # Step 1.3: Default algorithm ('BFS', 'DFS', 'UCS')

    def _get_neighbors(self, pos, walls, grid_size):
        """Helper to get valid adjacent cells and actions."""
        x, y = pos
        width, height = grid_size
        moves = [
            ('Up', (x, y + 1)),
            ('Down', (x, y - 1)),
            ('Left', (x - 1, y)),
            ('Right', (x + 1, y))
        ]
        valid_moves = []
        for action, (nx, ny) in moves:
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                valid_moves.append((action, (nx, ny)))
        return valid_moves

    def bfs_search(self, start, goal, walls, grid_size):
        """Step 1.2: BFS using FIFO queue (deque)"""
        frontier = deque([(start, [])])
        reached = {start}

        while frontier:
            current_pos, path = frontier.popleft()
            if current_pos == goal:
                return path

            for action, next_pos in self._get_neighbors(current_pos, walls, grid_size):
                if next_pos not in reached:
                    reached.add(next_pos)
                    frontier.append((next_pos, path + [action]))
        return None

    def dfs_search(self, start, goal, walls, grid_size):
        """Step 1.2: DFS using LIFO stack (list)"""
        frontier = [(start, [])]
        reached = set()

        while frontier:
            current_pos, path = frontier.pop()
            if current_pos == goal:
                return path

            if current_pos not in reached:
                reached.add(current_pos)
                for action, next_pos in self._get_neighbors(current_pos, walls, grid_size):
                    if next_pos not in reached:
                        frontier.append((next_pos, path + [action]))
        return None

    def ucs_search(self, start, goal, walls, grid_size):
        """Step 1.2: UCS using Priority Queue (heapq) ordered by path cost"""
        frontier = []
        # (cost, counter, position, path)
        heapq.heappush(frontier, (0, id(start), start, []))
        reached = {start: 0}

        while frontier:
            cost, _, current_pos, path = heapq.heappop(frontier)
            if current_pos == goal:
                return path

            if cost > reached.get(current_pos, float('inf')):
                continue

            for action, next_pos in self._get_neighbors(current_pos, walls, grid_size):
                new_cost = cost + 1  # Uniform step cost of 1
                if next_pos not in reached or new_cost < reached[next_pos]:
                    reached[next_pos] = new_cost
                    heapq.heappush(frontier, (new_cost, id(next_pos), next_pos, path + [action]))
        return None

    def sense_and_act(self, percept: dict) -> str:
        """Step 1.3: Execute offline plan step-by-step"""
        if not self.plan:
            start = tuple(percept.get('agent_pos', (0, 0)))
            all_food = percept.get('all_food', [])
            walls = set(tuple(w) for w in percept.get('walls', []))
            grid_size = percept.get('grid_size', (4, 4))

            if not all_food:
                return 'suck'

            # Find the closest food using Manhattan distance
            closest_food = min(
                all_food,
                key=lambda f: abs(f[0] - start[0]) + abs(f[1] - start[1])
            )
            goal = tuple(closest_food)

            # Choose algorithm based on active_algo
            if self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, goal, walls, grid_size) or []
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, goal, walls, grid_size) or []
            else:
                self.plan = self.bfs_search(start, goal, walls, grid_size) or []

        if self.plan:
            return self.plan.pop(0)
        return 'suck'