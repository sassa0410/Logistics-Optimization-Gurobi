\ Model knapsack problem
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  32 Y[0] + 23 Y[1] + 19 Y[2] + 17 Y[3] + 32 Y[4] + 11 Y[5] + 10 Y[6]
   + 27 Y[7] + 18 Y[8] + 34 Y[9]
Subject To
 weight_constraints[0]: 6 Y[0] + 9 Y[1] + 6 Y[2] + Y[3] + Y[4] + 2 Y[5]
   + 8 Y[6] + 7 Y[7] + 3 Y[8] + 5 Y[9] <= 30
 weight_constraints[1]: 6 Y[0] + 3 Y[1] + 5 Y[2] + 3 Y[3] + 5 Y[4] + 8 Y[5]
   + 8 Y[6] + 2 Y[7] + 8 Y[8] + Y[9] <= 25
 profit_constr: 32 Y[0] + 23 Y[1] + 19 Y[2] + 17 Y[3] + 32 Y[4] + 11 Y[5]
   + 10 Y[6] + 27 Y[7] + 18 Y[8] + 34 Y[9] >= 10
Bounds
Binaries
 Y[0] Y[1] Y[2] Y[3] Y[4] Y[5] Y[6] Y[7] Y[8] Y[9]
End
