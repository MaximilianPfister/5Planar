from scipy.optimize import minimize
# Code for Observation 19:
# var[0] = alpha
# var[1] = beta

# Objective is to maximize alpha <=> minimize -alpha
def objective(var):
    return -var[0]

# Constraints list
constraints = [

    # Relate beta to alpha
    {
        'type': 'eq',
        'fun': lambda var: var[1] - (30 - (8/ var[0]))
    },
    
    # 12/5 - 5*alpha > beta --> 12/5 - 5*alpha - beta > 0
    {
        'type': 'ineq',
        'fun': lambda var: 12/5 - 5*var[0] - (var[1]*var[0])
    },

    # 2 - 2*alpha >= beta  
    {
        'type': 'ineq',
        'fun': lambda var: 2 - 2*var[0] - (var[1]*var[0])
    },

    # 1 - alpha >= beta*alpha - 0.2  
    {
        'type': 'ineq',
        'fun': lambda var: 1 - var[0] - var[1]*var[0] + 0.2
    },

    # 3*(1 - alpha) >= 4/5 + 2*(beta - 0.2)
    {
        'type': 'ineq',
        'fun': lambda var: 3*(1 - var[0]) - (4/5 + 2*(var[1]*var[0] - 0.2))
    },

    # 4*(1 - alpha) >= 4/5 + 3*(beta - 0.2)
    {
        'type': 'ineq',
        'fun': lambda var: 4*(1 - var[0]) - (4/5 + 3*(var[1]*var[0] - 0.2))
    },

    # 4*(1 - alpha) >= 4/5 + 4*(alpha - 0.2)
    {
        'type': 'ineq',
        'fun': lambda var: 4*(1 - var[0]) - (4/5 + 4*(var[1]*var[0] - 0.2))
    }
    
]

# Initial guess
x0 = [0.3, 3.0]

# Bounds:
bounds = [(0, 0.5), (0, None)]  # alpha between 0 and 0.5, beta >= 0

# Solve
result = minimize(objective, x0, constraints=constraints, bounds=bounds)

# Output
print("Success:", result.success)
print("Status:", result.message)
print("alpha =", result.x[0])
print("beta =", result.x[1])
print("Result is epsilon-equal to 9/31: ",abs(-result.fun - 9/31) < 0.00000001)
