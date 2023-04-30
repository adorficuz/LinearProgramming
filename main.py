from amplpy import AMPL as ampl
import pandas
#Plz Insert the Constraints' Matrix A
# as an array of its rows, where each row is itself an array of its cols,
#ie A = [row1,..,rowm], where rowi = [Ai1,...,Ain].
#Then insert the resources', costs' and ineqs arrays b,c and ineqs, where
#each elem of ineqs is either '<=', '=' or '>='.
#Finally, type the type of problem u wanna solve (either 'minimize' or 'maximize', always typed with lowercase letters),
# the sign of the solution (analog to ineqs) and the name u wanna assign to the summoned files.
#It'll create in the project's directory both the ampl files necessary for computing the solution and
#the wolfram notebook displaying the feasible region and the gradient of the objective map.
#In order to get the wolfram's code right, just remove the gaps between lines.
#Run the run ampl file and substitute the optimal dot into the wolfram code.
#Seek either for "ListPlot" or "ListPointPlot3D" and switch the first 2 inputs {0,0} and (0,0) to
#such optimal dot.
#Adjust the plot range as well by changing the R value.
#I've included an example inside this repository for
#A = [[1,-2],[-3,1],[4,1],[-1,1]]
#b = [1,1,13,3]
#c = [-1,-1]
#ineqs = ['<=', '<=', '<=', '<=']
#type = 'minimize'
#solsgn = '>='
#name = 'P5R3'
def LinProgProb(A, b, c, ineqs, optimoption, solsgn, name):
    if optimoption == 'minimize' or optimoption == 'maximize':
        m = len(A)
        n = len(A[0])
        wmath = open(f"{name}.nb", "w+")
        wampldata = open(f"{name}.dat", "w+")
        wamplmod = open(f"{name}.mod", "w+")
        wamplrun = open(f"{name}.run", "w+")
        plotspan = ''
        if solsgn == '<=':
            plotspan += '-R,0}'
        else:
            plotspan += '0,R}'
        sgngrad = ''
        if optimoption == 'minimize':
            sgngrad = '-'
        else:
            sgngrad = ''
        constsmod = list()
        for i in range(0, m):
            constsmod.extend([''] + [f'subject to const{i + 1}:'] + [
                '  sum {j in C}' + f' a[{i + 1},j]*x[j] {ineqs[i]} b[{i + 1}];'])
        constsmod.extend([''] + [f'subject to const{m + 1}' + ' {j in C} :'] + [f'  x[j] {solsgn} 0;'])
        lineswmod = ['param m >= 0, integer;', 'param n >= 0, integer;', '', '', 'set R := 1..m;', 'set C := 1..n;', '',
                     'var x{C};', 'param c{C};', 'param a{R,C};', 'param b{R};', '',
                     f'{optimoption} cost' + ' : sum {i in C} c[i]*x[i];'] + constsmod
        lineswrun = ['reset;', f'model {name}.mod;', f'data {name}.dat;', 'option solver gurobi;', 'solve;',
                     'display x;',
                     'display cost;']
        wamplmod.writelines(line + '\n' for line in lineswmod)
        wamplrun.writelines(line + '\n' for line in lineswrun)
        acols = ' '
        for i in range(0, n):
            acols += f'  {i + 1}'
        acols += ':='
        lineswdat = [f'param m := {m};', f'param n := {n};', '', 'param a :', acols]
        matrix = list()
        for i in range(0, m):
            row = ''
            for j in range(0, n):
                row += f'  {A[i][j]}'
            matrix.append(f'{i + 1}  {row}')
        matrix[-1] += ';'
        resources = list()
        for i in range(0, m):
            resources.append(f'{i + 1}  {b[i]}')
        resources[-1] += ';'
        costs = list()
        for i in range(0, n):
            costs.append(f'{i + 1}  {c[i]}')
        costs[-1] += ';'
        lineswdat.extend(matrix + ['', 'param c:='] + costs + ['', 'param b:='] + resources)
        wampldata.writelines(line + '\n' for line in lineswdat)
        wampldata.close()
        wamplmod.close()
        wamplrun.close()
        ampl.read(f"/content/{name}.mod")
        ampl.read_data(f"/content/{name}.dat")
        ampl.option["solver"] = "gurobi"
        ampl.solve()
        solve_result = ampl.get_value("solve_result")
        if solve_result == 'solved':
            x = ampl.get_variable("x").get_values().to_pandas().values
            sollist = list()
            for i in x:
                sollist.append(i[0])
            soltuple = tuple(sollist)
        else:
            soltuple = None
        print(f'La solución es {soltuple}')
        if n == 2:
            consts = f'({A[0][0]})*x + ({A[0][1]})*y {ineqs[0]} {b[0]}'
            for i in range(1, m):
                consts += f' && ({A[i][0]})*x + ({A[i][1]})*y {ineqs[i]} {b[i]}'
            lineswmath = [f'a = {c[0]};', f'b = {c[1]};', f'f[a_, b_, x_, y_] := (a*x + b*y) ;', f'R = 10;',
                          'VectorPlot[Evaluate@Grad['+sgngrad+'f[a, b, x, y], {x, y}], {x,' + plotspan +', {y,' + plotspan + ', VectorScale -> Small, VectorPoints -> Coarse, VectorStyle -> Green];'
                ,
                          'Show[ContourPlot[f[a, b, x, y], {x,' + plotspan + ', {y,' + plotspan + ', ContourStyle -> Opacity[0.5], Contours -> 50],RegionPlot[' + consts + ',{x,' + plotspan + ', {y,' + plotspan + ', PlotPoints -> 100, PlotStyle -> Directive[Purple, Opacity[0.8]]], ListPlot[{{'+ f'{list(soltuple)[0][0]} , {list(soltuple)[1][0]}' +'}} -> {"'+f'{soltuple}'+'"}, PlotRange -> {{' + plotspan + ', {' + plotspan + '}, PlotStyle -> Directive[PointSize[Large], Red]], %]']
            wmath.writelines(line + '\n' for line in lineswmath)
        elif n == 3:
            consts = f'({A[0][0]})*x + ({A[0][1]})*y + ({A[0][2]})*z {ineqs[0]} {b[0]}'
            for i in range(1, m):
                consts += f' && ({A[i][0]})*x + ({A[i][1]})*y + ({A[i][2]})*z {ineqs[i]} {b[i]}'
            lineswmath = [f'a = {c[0]};', f'b = {c[1]};', f'c = {c[2]}',
                          f'f[a_, b_, c_ , x_, y_ , z_] := (a*x + b*y +c*z) ;', f'R = 10;',
                          'VectorPlot3D[Evaluate@Grad['+sgngrad+'f[a, b, c, x, y ,z], {x, y, z}], {x,' + plotspan +', {y,' + plotspan +', {z,' + plotspan +', VectorScale -> Small, VectorPoints -> Coarse, VectorStyle -> Green];'
                ,
                          'Show[ContourPlot[f[a, b, c, x, y, z], {x,' + plotspan +', {y,' + plotspan +', {z,' + plotspan +', ContourStyle -> Opacity[0.5], Contours -> 10],RegionPlot[' + consts + ',{x,' + plotspan +', {y,' + plotspan +', {z,' + plotspan +', PlotPoints -> 100, PlotStyle -> Directive[Purple, Opacity[0.8]]], ListPointPlot3D[{{'+f'{list(soltuple)[0][0]}'+f'{list(soltuple)[1][0]}'+f'{list(soltuple)[2][0]}'+'}}, PlotRange -> {{' + plotspan + ', {' + plotspan + ', {' + plotspan + '}, PlotStyle -> Directive[PointSize[Large], Red]], %]']
            wmath.writelines(line + '\n' for line in lineswmath)
        else:
            print("I cannot plot this data")
    else:
        print('Plz, enter a proper problem type: either minimize or maximize')