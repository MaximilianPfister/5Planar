from pulp import *

#Check if two chords intersect each other
def doIntersect(a,b):
    if (a[0] not in b and a[1] not in b):
        return (a[0] < b[0] and b[0] < a[1] and b[1] > a[1]) or (b[0] < a[0] and a[0]< b[1] and a[1] > b[1])
    return False
    
def ChargingOfHBlocks():
    n = 12 #number of real + edge vertices
    nnn = n**3 # sufficiently large number
    edges = []
    # Even indices will correspond to original vertices
    # Odd indices will correspond to edge vertices
    alpha = 49/170 # we want to show that for our choice of alpha, we do not spent more than 8 charge
    unit_2_3 = alpha-0.2 # (alpha-0.2) is the amount that 2-3 faces transfer (or not) to a 1-3 face in the charging of a Q-block
    base_2_3 = 9/5 - 6*alpha # the remainder of 2-3 faces if they transfer to 4 side-neighbors
    # a single edge is not allowed to contribute more than what it would obtain from an H-block 
    charge_2_3_capped_at_alpha = (alpha-base_2_3)/unit_2_3 
    unit_3_3 = (2-3*alpha)/5 # charge H obtains from every edge that ends at a 3-3 according to Lemma 11

    #Construct the possible edges
    boundary_edges = [(0,2),(2,4),(4,6),(6,8),(8,10),(0,10)]
    interior_edges = [(0,4),(0,6),(0,8),(2,6),(2,8),(2,10),(4,8),(4,10),(6,10)]
    exterior_edges = [(0,3),(0,5),(0,7),(0,9),(2,5),(2,7),(2,9),(2,11),(1,4),(4,7),(4,9),(4,11),(1,6),(3,6),(6,9),(6,11),(1,8),(3,8),(5,8),(8,11),(1,10),(3,10),(5,10),(7,10)]
    edges = boundary_edges + interior_edges + exterior_edges
    
    # Edges can appear with multiplicity at most 5-2 = 3 (only if they end at an edge-node, otherwise multiplicity is one)
    x = pulp.LpVariable.dicts(
    "chords", edges, lowBound=0, upBound=3, cat=LpInteger)
    
    #Auxilliary variables (used for technical reasons to encode min/max stuff)
    
    at_least_one_boundary_crossing = pulp.LpVariable.dicts(
    "crossedboundary_atleast_once", range(1,12,2), lowBound=0, upBound=1, cat=LpInteger)
    is_2_triangle = pulp.LpVariable.dicts(
    "2_triangle", range(1,12,2), lowBound=0, upBound=1, cat=LpInteger)
    is_3_triangle = pulp.LpVariable.dicts(
    "3_triangle", range(1,12,2), lowBound=0, upBound=1, cat=LpInteger)
    
    charge_from_2_triangle = pulp.LpVariable.dicts(
    "charge_from_2_triangle", range(1,12,2), lowBound=0.0, upBound=4.0, cat=LpContinuous) #1,3,5,7,9,11
    charge_from_3_triangle = pulp.LpVariable.dicts(
    "charge_from_3_triangle", range(1,12,2), lowBound=0, upBound=5, cat=LpInteger) #at most five.

    #Auxilliary for 2-triangle case 
    # _inside means in interior or on boundary of H block
    four_crossings_inside = pulp.LpVariable.dicts(
    "four_crossings", exterior_edges, lowBound=0, upBound=1, cat=LpInteger)
    five_crossings_inside = pulp.LpVariable.dicts(
    "five_crossings", exterior_edges, lowBound=0, upBound=1, cat=LpInteger)
    
    upper_bound_of_two_for_2_triangle = pulp.LpVariable.dicts(
    "upper_bound_of_two_for_2_triangle", range(1,12,2), lowBound=0, upBound=1, cat=LpInteger)
    
    

    prob = pulp.LpProblem("SpentCharge",LpMaximize)
    #Goal function -> we want to simulate worst case, i.e. most charge spent.
    # for each boundary edge we spent 1*alpha
    # for each interior and exterior edge we spent 2*alpha initially
    prob += (pulp.lpSum([alpha*x[chord] for chord in boundary_edges]) + \
            pulp.lpSum([2*alpha*x[chord] for chord in interior_edges]) + \
            pulp.lpSum([2*alpha*x[chord] for chord in exterior_edges]) - \
            # now we obtain charge back according to the rules described in the paper
            #if the face is a 2-3, we always get base 
            pulp.lpSum([base_2_3*is_2_triangle[a] for a in range(1,12,2)])- \
            #additionally, we get charge_from_2_triangle
            pulp.lpSum([unit_2_3*charge_from_2_triangle[a] for a in range(1,12,2)]) - \
            # otherwise, we get charge from 3-3
            pulp.lpSum([unit_3_3*charge_from_3_triangle[a] for a in range(1,12,2)])) 
                    
    #boundary edges and interior edges occur at most once as G is simple
    for e in boundary_edges:
        prob+=x[e] <= 1
    for e in interior_edges:
        prob+=x[e] <= 1
    #5-planarity constraint
    for chord in edges:
        prob += (
            pulp.lpSum([x[otherChord] for otherChord in edges if doIntersect(chord,otherChord)]) + nnn*x[chord] <=5+nnn)

    
    #The three pairwise crossing edges that define H are always present
    prob+=(x[(0,6)] == 1)
    prob+=(x[(2,8)] == 1)
    prob+=(x[(4,10)] == 1)

    for e in exterior_edges:
        # For the exterior edges, set the auxilliary variables four/five crossings to true if they have the respective amount of crossings 
        prob+=(pulp.lpSum([x[otherChord] for otherChord in edges if doIntersect(e,otherChord)]) + nnn*x[e]<=nnn+3+(nnn*four_crossings_inside[e]))
        prob+=(pulp.lpSum([x[otherChord] for otherChord in edges if doIntersect(e,otherChord)]) + nnn*x[e]<=nnn+4+(nnn*five_crossings_inside[e]))

    
    for triag in range(1,12,2):
        prob+=pulp.lpSum([x[ext] for ext in exterior_edges if triag in ext]) <= nnn*at_least_one_boundary_crossing[triag]
        #if we have a crossing, then it is either a 2-triangle or a 3-triangle
        prob+= is_2_triangle[triag] + is_3_triangle[triag] <= at_least_one_boundary_crossing[triag]
        #Express charge of 3-triangle
        prob+=pulp.lpSum([x[ext] for ext in exterior_edges if triag in ext]) <= nnn*is_2_triangle[triag]+charge_from_3_triangle[triag]

        #Charging of 2-triangles
        #upper bound of 2 units has to hold due to #of edges crossing
        prob+=pulp.lpSum([x[ext] for ext in exterior_edges if triag in ext]) <= 2+(nnn*upper_bound_of_two_for_2_triangle[triag])

        #If there exists a highly crossed edge, we have 3 units
        for ext in exterior_edges:
            if triag in ext:
                #if there exists an exterior edge with at least four crossings which crosses boundary edge, then we have at least 3 additional units
                # here this is not 3 units, but at most alpha (due to H-block restrictions)
                prob+=charge_2_3_capped_at_alpha*four_crossings_inside[ext] <= nnn*is_3_triangle[triag] + charge_from_2_triangle[triag]
                # in this case, the other side is a Q-block, cannot be an H-block (as that would imply one additional crossing).
                prob+=4*five_crossings_inside[ext] <= nnn*is_3_triangle[triag] + charge_from_2_triangle[triag]
                
        #Express charge of 2-triangles
        prob+=pulp.lpSum([x[ext] for ext in exterior_edges if triag in ext])-nnn*upper_bound_of_two_for_2_triangle[triag] <= nnn*is_3_triangle[triag] + charge_from_2_triangle[triag]
        prob+=2*upper_bound_of_two_for_2_triangle[triag] <= nnn*is_3_triangle[triag] + charge_from_2_triangle[triag] 

    
    prob.solve()
    print("Objective Value smaller than 8 :", prob.objective.value() <= 8.0)
ChargingOfHBlocks()
