from __future__ import annotations

from typing import Dict, List, Tuple

from polyreduce.core.reduction import Reduction
from polyreduce.graph.hamiltonian_cycle_instance import HamiltonianCycleInstance
from polyreduce.sat.three_sat import ThreeSATInstance

# Hamiltonian Cycle gadget construction for a single clause
# k is the number of clauses
# n is the number of variables
def _variable_gadget_edges(k: int, entry_node: int) -> Tuple[int, int, List[Tuple[int, int]], Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]]:
    edges: List[Tuple[int, int]] = []

    entry_node = entry_node
    exit_node =  entry_node + 3 * k + 3

    breach_node_entry = entry_node + 1
    breach_node_exit = entry_node + 3 * k + 2
    
    top_nodes = [entry_node + 2 + i*3 for i in range(k+1)]
    middle_nodes = [entry_node + 3 + i*3 for i in range(k+1)]
    bottom_nodes = [entry_node + 4 + i*3 for i in range(k+1)]
    
    # Connect entry to first clause gadget
    edges.append((entry_node, breach_node_entry))
    edges.append((breach_node_entry, top_nodes[0]))
    edges.append((breach_node_entry, bottom_nodes[0]))
    
    # Connect clause gadgets
    
    # Vertical connections within each clause gadget
    for i in range(k):
        edges.append((top_nodes[i], middle_nodes[i]))
        edges.append((middle_nodes[i], bottom_nodes[i]))
        
    # Horizontal connections between clause gadgets
    
    # True path connections
    true_path_edges = []
    
    for i in range(k):
        if i % 2 == 0:
            edges.append((top_nodes[i], bottom_nodes[i + 1]))
            true_path_edges.append((top_nodes[i], bottom_nodes[i + 1]))
        else:
            edges.append((bottom_nodes[i], top_nodes[i + 1]))
            true_path_edges.append((bottom_nodes[i], top_nodes[i + 1]))
    
    # False path connections
    false_path_edges = []
    for i in range(k):
        if i % 2 == 0:
            edges.append((bottom_nodes[i], top_nodes[i + 1]))
            false_path_edges.append((bottom_nodes[i], top_nodes[i + 1]))
        else:
            edges.append((top_nodes[i], bottom_nodes[i + 1]))
            false_path_edges.append((top_nodes[i], bottom_nodes[i + 1]))
    
    # Connect last clause gadget to exit
    edges.append((top_nodes[-1], breach_node_exit))
    edges.append((bottom_nodes[-1], breach_node_exit))
    edges.append((breach_node_exit, exit_node))
    
    # Map k clauses to their corresponding true and false path edges
    clause_edge_map: Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]] = {}
    for i in range(k):
        clause_edge_map[i] = (true_path_edges[i], false_path_edges[i])
        
    print(clause_edge_map)
    

    return entry_node, exit_node, edges, clause_edge_map


class ThreeSATToHamiltonianCycle(Reduction[ThreeSATInstance, HamiltonianCycleInstance]):
    def __init__(self):
        super().__init__("3SAT", "HAM-CYCLE")

    def reduce(self, instance: ThreeSATInstance) -> HamiltonianCycleInstance:
        k = len(instance.clauses)
        vars_set = sorted({abs(lit) for clause in instance.clauses for lit in clause})
        
        gadgets = []
        edges = []
        for var in vars_set:
            if (len(gadgets) == 0):
                entry_node = 1
            else:
                entry_node = gadgets[-1][1]
            gadget = _variable_gadget_edges(k, entry_node)
            gadgets.append(gadget)
            edges.extend(gadget[2])
        
        entry_node = gadgets[0][0]
        exit_node = gadgets[-1][1]
        
        # Create vertex for each clause and connect to the corresponding gadget edges
        for clause_index, clause in enumerate(instance.clauses):
            clause_satisfied_edges = []
            new_vertex = exit_node + 1 + clause_index
            for literal in clause:
                var_index = vars_set.index(abs(literal))
                gadget = gadgets[var_index]
                clause_edge_map = gadget[3]
                true_edge, false_edge = clause_edge_map[clause_index]
                if literal > 0:
                    clause_satisfied_edges.append((true_edge[0], new_vertex))
                    clause_satisfied_edges.append((new_vertex, true_edge[1]))
                else:
                    clause_satisfied_edges.append((false_edge[0], new_vertex))
                    clause_satisfied_edges.append((new_vertex, false_edge[1]))
            edges.extend(clause_satisfied_edges)
            
        # Close the cycle
        edges.append((exit_node, entry_node))
        
            
        return HamiltonianCycleInstance(
            name=f"HAM-CYCLE_from_{instance.name}",
            num_vertices=exit_node + len(instance.clauses),
            edges=edges,
        )
        
        
        