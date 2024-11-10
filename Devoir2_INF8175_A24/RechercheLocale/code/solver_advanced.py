# BEN_OTHMAN(1934245)
# Hosna(2132223)

import random
import math

def solve(schedule):
    # Simulated annealing - algorithme 
    initial_temperature = 1000.0
    alpha = 0.95  
    max_iterations = 1000
    
    current_solution = generate_initial_solution(schedule)
    best_solution = current_solution.copy() # La meilleur solution est la solution initiale au début
    current_cost = calculate_conflicts_cost(current_solution, schedule) # Évaluation de la solution initiale
    best_cost = current_cost # Le meilleur coût est le coût de la solution initiale au début
    
    temperature = initial_temperature
    
    for k in range(max_iterations):
        # Une Deep copie permet de préserver l'état précédant
        neighbor = generate_neighbor(current_solution.copy(), schedule)
        new_cost = calculate_conflicts_cost(neighbor, schedule)
        
        delta = new_cost - current_cost
        
        # Fonction de sélection de la solution
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
    Fonction de voisinage
    """
    course = random.choice(list(schedule.course_list))
    new_slot = random.randint(1, len(schedule.course_list))

    if all(solution.get(neighbor) != new_slot 
          for neighbor in schedule.get_node_conflicts(course)):
        solution[course] = new_slot
    
    return solution

def calculate_conflicts_cost(solution, schedule):
    """ Fonction d'évaluation"""
    conflicts = 0
    for course in schedule.course_list:
        for neighbor in schedule.get_node_conflicts(course):
            if solution.get(course) == solution.get(neighbor):
                conflicts += 1
    return conflicts


def generate_initial_solution(schedule):
    """ Fonction de génération d'une solution initiale"""
    solution = {}
    for course in schedule.course_list:
        for time_slot in range(1, len(schedule.course_list) + 1): 
            if all(solution.get(neighbor) != time_slot for neighbor in schedule.get_node_conflicts(course)):
                solution[course] = time_slot
                break
    return solution