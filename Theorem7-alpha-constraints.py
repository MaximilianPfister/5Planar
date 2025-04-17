from scipy.optimize import minimize

# Code for Theorem 7:
# var[0] = \alpha
# var[1] = \beta

# Define the objective: maximize alpha[0] <=> minimize -alpha[0]
def objective(var):
    return -var[0]
# Constraints list
constraints = [

    # Relate beta to alpha
    {
        'type': 'eq',
        'fun': lambda var: var[1] - (30 - (8/ var[0]))
    },

    # 2*(alpha - 0.2) <= 0.2 -> 0.2 - 2*(alpha-0.2) >= 0
    {
        'type': 'ineq',
        'fun': lambda var: 0.2 - 2 * (var[0] - 0.2)
    },
    # 1 >= 3alpha
    {
        'type': 'ineq',
        'fun': lambda var: 1 - 3*var[0]
    },

    # 9/5 - 6 * alpha >= 0
    {
        'type': 'ineq',
        'fun': lambda var: 9/5 - 6 * var[0]
    },

    # beta < 3  
    {
        'type': 'ineq',
        'fun': lambda var: 3 - var[1]
    },
    # alpha <= 9/31
    {
        'type': 'ineq',
        'fun': lambda var: (9/31)-var[0]
    },

    # 9/5 - 6*alpha >= beta - 2
    {
        'type': 'ineq',
        'fun': lambda var: 9/5 - 6*var[0] - (var[1] - 2)*var[0]
    },

    # 2 - 3*alpa >= (beta + (beta - 2))*alpha
    {
        'type': 'ineq',
        'fun': lambda var: 2 - 3*var[0] - (2*var[1] - 2)*var[0]
    },

    # 2 - 3*alpha >= (beta + 2*(beta - 2))*alpha
    {
        'type': 'ineq',
        'fun': lambda var: 2 - 3*var[0] - (var[1] + 2*(var[1] - 2))*var[0]
    },

    # (2 - (3 + (beta - 2))*alpha)/4 >= (2 - 3*alpha)/4
    {
        'type': 'ineq',
        'fun': lambda var: (2 - (3 + (var[1] - 2))*var[0])/4 - (2 - 3*var[0]) / 5
    },
        # 2 - 3alpha >= beta*alpha
    {
        'type': 'ineq',
        'fun': lambda var: (2 - 3*var[0]) - var[1]*var[0]
    },
        # alpha >= (2-3*alpha) / 5
    {
        'type': 'ineq',
        'fun': lambda var: var[0]- (2 - 3*var[0])/5 
    },
        # alpha >= 8/5 - 5*alpha
    {
        'type': 'ineq',
        'fun': lambda var: var[0] - (8/5 - 5*var[0])
    }

    
]

# Initial guess
x0 = [0.3, 3.0]

# Bounds: (optional) you can set them if needed
bounds = [(0, 1), (0, None)]  # alpha between 0 and 1, beta >= 0

# Solve
result = minimize(objective, x0, constraints=constraints, bounds=bounds)

# Output
print("Success:", result.success)
print("Status:", result.message)
print("var[0] =", result.x[0])
print("var[1] =", result.x[1])
print("Result is epsilon-equal to 49/170: ",abs(-result.fun - 49/170) < 0.00000001)

