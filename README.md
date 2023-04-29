# LinearProgramming
Linear Programming Auxiliary Funcs both for visualization and computation
#Plz Insert the Constraints' Matrix A
# as an array of its rows, where each row is itself an array of its cols,
#ie A = [row1,..,rowm], where rowi = [Ai1,...,Ain].
#Then insert the resources', costs' and ineqs arrays b,c and ineqs, where
#each elem of ineqs is either '<=', '=' or '>='
#It'll create in the project's directory both the ampl files necessary for computing the solution and
#the wolfram notebook displaying the feasible region and the gradient of the objective map.
#In order to get the wolfram's code right, just remove the gaps between lines.
#Run the run ampl file and substitute the optimal dot into the wolfram code.
#Seek either for "ListPlot" or "ListPointPlot3D" and switch the first 2 inputs {0,0} and (0,0) to
#such optimal dot.
#I've included an example inside this repository for
#A = [[1,-2],[-3,1],[4,1],[-1,1]]
#b = [1,1,13,3]
#c = [-1,1]
#ineqs = ['<=', '<=', '<=', '<=']
#name = P5R3
