from .abstract_solver import AbstractSolver
import numpy as np
import gurobipy as gp
from gurobipy import GRB

class solver_321750(AbstractSolver):
    def __init__(self, env):
        super().__init__(env)
        self.name = 'solver_321750'
    
    def solve(self):
        N_deposits = self.env.inst.service.shape[0]
        N_supermarkets = self.env.inst.service.shape[1]
        N_nodes =N_deposits+1
        
        m = gp.Model()
        
        # variabili binarie
        X = m.addVars(N_deposits, vtype=GRB.BINARY, name='X')
        Y = m.addVars(N_nodes, N_nodes, vtype=GRB.BINARY, name='Y')
        Z = m.addVars(N_supermarkets, vtype=GRB.BINARY, name='Z')
        
        # variabile binaria che indica se il tour è attivo
        T = m.addVar(vtype=GRB.BINARY, name='T')
        
        # variabile ausiliare
        u = m.addVars(range(1,N_nodes), vtype=GRB.CONTINUOUS, lb=1, ub=N_deposits, name='u')
        
        # funzione obiettivo
        m.setObjective(
            gp.quicksum(self.env.inst.weights['construction'] * X[i] for i in range(N_deposits)) +
            gp.quicksum(self.env.inst.weights['missed_supermarket'] * Z[k] for k in range(N_supermarkets)) +
            gp.quicksum(self.env.inst.weights['travel'] * Y[i,j] * self.env.inst.distances[i][j] for i in range(N_nodes) for j in range(N_nodes) if i!=j),
            GRB.MINIMIZE
        )
        
        # vincoli per supermercati coperti
        for j in range(N_supermarkets):
            m.addConstr(
                gp.quicksum(self.env.inst.service[i][j]*X[i]for i in range(N_deposits))+ Z[j]>= 1
            )
    
        # vincoli per gli archi tra i depositi
        for i in range(1,N_nodes):
            m.addConstr(gp.quicksum(Y[i, j] for j in range(N_nodes) if j != i) == X[i-1])
            m.addConstr(gp.quicksum(Y[j, i] for j in range(N_nodes) if j != i) == X[i-1])
        
        # vincoli per il tour attivo o no
        m.addConstr(gp.quicksum(X) <= T*N_deposits) # se sum(X)>0 allora vi è un Tour
        m.addConstrs(X[i] <= T for i in range(N_deposits)) # vincolo se T = 0, allora nessun magazzino costruito
        
        # vincoli a partire dall'azienda ossia nodo 0
        m.addConstr(gp.quicksum(Y[0, j] for j in range(1, N_nodes)) == T)
        m.addConstr(gp.quicksum(Y[j, 0] for j in range(1, N_nodes)) == T)
        
        # vincoli MTZ per evitare i subtours
        m.addConstrs(
            (u[i] - u[j] + N_nodes*Y[i,j] <= N_nodes - 1 for i in range(1,N_nodes)
            for j in range(1,N_nodes)
            if i!=j)
        )
        
        m.optimize()
        
        if m.status == GRB.OPTIMAL:
            X_f = [int(round(X[i].X)) for i in range(N_deposits)]
            Y_f = np.array([[int(round(Y[i, j].X)) for j in range(N_nodes)] for i in range(N_nodes)])
            return X_f, Y_f

        else:
            return None, None
        