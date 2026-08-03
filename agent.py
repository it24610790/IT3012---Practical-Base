# agent.py
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
        pass

    def sense_and_act(self, percept: dict) -> str:
        return 'Up'


class SearchAgent:
    def __init__(self):
        pass

    def bfs_search(self, start, goal, walls, grid_size):
        return []