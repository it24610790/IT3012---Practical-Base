# agent.py
from collections import deque
import heapq
import math
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
        self.plan = []
        self.active_algo = 'AStar'  # Default to AStar for Lab 04

    def manhattan_distance(self, pos, goal):
        """Step 1.1: Manhattan distance formula h(n) = |x1 - x2| + |y1 - y2|"""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        """Step 1.1: Euclidean distance formula h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)"""
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

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
        frontier = []
        heapq.heappush(frontier, (0, id(start), start, []))
        reached = {start: 0}
        while frontier:
            cost, _, current_pos, path = heapq.heappop(frontier)
            if current_pos == goal:
                return path
            if cost > reached.get(current_pos, float('inf')):
                continue
            for action, next_pos in self._get_neighbors(current_pos, walls, grid_size):
                new_cost = cost + 1
                if next_pos not in reached or new_cost < reached[next_pos]:
                    reached[next_pos] = new_cost
                    heapq.heappush(frontier, (new_cost, id(next_pos), next_pos, path + [action]))
        return None

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        """Step 1.2: A* Search evaluating f(n) = g(n) + h(n)"""
        # Calculate initial h(n)
        if heuristic_type == 'euclidean':
            h_start = self.euclidean_distance(start_pos, goal_pos)
        else:
            h_start = self.manhattan_distance(start_pos, goal_pos)

        # Priority Queue tuple: (f_cost, g_cost, unique_id, current_pos, path_taken)
        frontier = []
        heapq.heappush(frontier, (h_start, 0, id(start_pos), start_pos, []))
        reached_states = {start_pos: 0}

        while frontier:
            f_cost, g_cost, _, current_pos, path_taken = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path_taken

            if g_cost > reached_states.get(current_pos, float('inf')):
                continue

            for action, next_pos in self._get_neighbors(current_pos, walls, grid_size):
                new_g = g_cost + 1

                if next_pos not in reached_states or new_g < reached_states[next_pos]:
                    reached_states[next_pos] = new_g
                    
                    if heuristic_type == 'euclidean':
                        h_new = self.euclidean_distance(next_pos, goal_pos)
                    else:
                        h_new = self.manhattan_distance(next_pos, goal_pos)

                    new_f = new_g + h_new
                    heapq.heappush(frontier, (new_f, new_g, id(next_pos), next_pos, path_taken + [action]))

        return None

    def sense_and_act(self, percept: dict) -> str:
        """Step 1.3: Decision Loop using A* or other algorithms"""
        if not self.plan:
            start = tuple(percept.get('agent_pos', (0, 0)))
            all_food = percept.get('all_food', percept.get('remaining_food', []))
            walls = set(tuple(w) for w in percept.get('walls', []))
            grid_size = percept.get('grid_size', (4, 4))

            if not all_food:
                return 'suck'

            closest_food = min(
                all_food,
                key=lambda f: self.manhattan_distance(start, f)
            )
            goal = tuple(closest_food)

            if self.active_algo == 'AStar':
                self.plan = self.astar_search(start, goal, walls, grid_size, heuristic_type='manhattan') or []
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, goal, walls, grid_size) or []
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, goal, walls, grid_size) or []
            else:
                self.plan = self.bfs_search(start, goal, walls, grid_size) or []

        if self.plan:
            return self.plan.pop(0)
        return 'suck'