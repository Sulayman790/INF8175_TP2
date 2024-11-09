import random
import math

def simulated_annealing(schedule):
    """
    Implements simulated annealing algorithm for academic schedule optimization
    :param schedule: object describing the input schedule
    :return: optimized schedule solution
    """
    initial_temperature = 1000.0
    alpha = 0.95  
    max_iterations = 1000
    
    current_solution = generate_initial_solution(schedule)
    best_solution = current_solution.copy()
    current_cost = calculate_conflicts_cost(current_solution, schedule)
    best_cost = current_cost
    
    temperature = initial_temperature
    
    for k in range(max_iterations):
        neighbor = generate_neighbor(current_solution.copy(), schedule)
        new_cost = calculate_conflicts_cost(neighbor, schedule)
        
        delta = new_cost - current_cost
        
        if delta <= 0 or random.random() < math.exp(-delta / temperature):
            current_solution = neighbor
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_solution = current_solution.copy()
                best_cost = current_cost
        
        temperature *= alpha
    
    return best_solution

def generate_neighbor(solution, schedule):
    """
    Generates a neighboring solution by making a random modification
    """
    course = random.choice(list(schedule.course_list))
    new_slot = random.randint(1, len(schedule.course_list))

    if all(solution.get(neighbor) != new_slot 
          for neighbor in schedule.get_node_conflicts(course)):
        solution[course] = new_slot
    
    return solution

def calculate_conflicts_cost(solution, schedule):
    conflicts = 0
    for course in schedule.course_list:
        for neighbor in schedule.get_node_conflicts(course):
            if solution.get(course) == solution.get(neighbor):
                conflicts += 1
    return conflicts


def generate_initial_solution(schedule):
    solution = {}
    for course in schedule.course_list:
        assigned = False
        for time_slot in range(1, len(schedule.course_list) + 1): 
            if all(solution.get(neighbor) != time_slot for neighbor in schedule.get_node_conflicts(course)):
                solution[course] = time_slot
                assigned = True
                break
        if not assigned:
            raise Exception(f"Unable to assign a slot for course {course}")
    return solution