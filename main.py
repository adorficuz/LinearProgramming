from wolframclient.evaluation import WolframCloudSession, SecuredAuthenticationKey
from wolframclient.language import wlexpr, wl
from PIL import Image
import io
import numpy as np
from amplpy import AMPL, tools
ampl = tools.ampl_notebook(
    modules=["gurobi"], # modules to install
    license_uuid="default", # license to use
    g=globals()) # instantiate AMPL object and register magics
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
    if optimoption == 'minimize' or optimoption == 'maximize' or (len(optimoption) == 2 and (optimoption[0] == 'minimize' or optimoption[0] == 'maximize') and optimoption[1] == 'integer') or (len(optimoption) == 3 and (optimoption[0] == 'minimize' or optimoption[0] == 'maximize') and optimoption[1] == 'integer' and len(optimoption[2]) != len(A[0])):
        m = len(A)
        n = len(A[0])
        wmath = open(f"{name}.nb", "w+")
        wampldata = open(f"{name}.dat", "w+")
        wamplmod = open(f"{name}.mod", "w+")
        wamplrun = open(f"{name}.run", "w+")
        if type(optimoption) == str:
            probtype = optimoption
            newInd = 'C'
            newIndSet = ''
            newIndSetList = list(range(1, n + 1))
            compInd = ''
            compIndSet = ''
            compIndSetList = list()
            soltype = ''
        elif type(optimoption) == list and len(optimoption) == 2:
            probtype = optimoption[0]
            newInd = 'C'
            newIndSet = ''
            newIndSetList = list(range(1,n+1))
            compInd  = ''
            compIndSet = ''
            compIndSetList = list()
            soltype = ', integer'
        else:
            probtype = optimoption[0]
            newInd = 'I'
            newIndSet = 'set I := {' + f'{optimoption[2][0]}'
            for i in range(1,len(optimoption[2])):
                newIndSet += f', {optimoption[2][i]}'
            newIndSet += '};'
            newIndSetList = optimoption[2]
            compInd = 'var y{J};'
            compIndSetList = [item for item in list(range(1,n+1)) if item not in newIndSetList]
            compIndSet = 'set J := {' + f'{compIndSetList[0]}'
            for i in range(1,len(compIndSetList)):
                compIndSet += f', {compIndSet[i]}'
            compIndSet += '};'
            soltype = ', integer'
        constsmod = list()
        for i in range(1,m+1):
            if len(compIndSetList) == 0:
                compconst = ''
            else:
                compconst = '+  sum {k in '+'J'+'}' + f' a[{i},k]*y[k]'
            constsmod.extend([''] + [f'subject to const{i}:'] + [
                '  sum {j in '+newInd+'}' + f' a[{i},j]*x[j] '+ compconst + f'{ineqs[i-1]} b[{i}];'])
        constsmod.extend([''] + [f'subject to const{m + 1}' + ' {i in '+ newInd +'} :'] + [f'  x[i] {solsgn} 0;'])
        if len(compIndSetList) == 0:
            compcost  = ''
            vardisp = ''
        else:
            compcost = '+ sum {j in '+'J'+'} c[j]*y[j]'
            vardisp = 'y'
            constsmod.extend([''] + [f'subject to const{m + 2}' + ' {j in ' + 'J' + '} :'] + [f'  y[j] {solsgn} 0;'])
        lineswmod = ['param m >= 0, integer;', 'param n >= 0, integer;', '', '', 'set R := 1..m;', 'set C := 1..n;', newIndSet, compIndSet ,'',
                     'var x{'+ newInd + '}' + soltype + ';', compInd  , 'param c{C};', 'param a{R,C};', 'param b{R};', '',
                     f'{probtype} cost' + ' : '+'sum {i in '+newInd+'} c[i]*x[i]'+ compcost + ';'] + constsmod
        lineswrun = ['reset;', f'model {name}.mod;', f'data {name}.dat;', 'option solver gurobi;', 'solve;',
                     'display x'+vardisp+';',
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
            xpd = ampl.get_variable("x").get_values().to_pandas().values
            x = list()
            for i in range(0,n):
                if (i+1) in newIndSetList:
                    x.append(xpd[0][0])
                    xpd = np.delete(xpd,0,0)
                else:
                    x.append(0)
            if len(compIndSetList) == 0:
                y = list()
                for _ in range(0,n):
                    y.append(0)
            else:
                ypd = ampl.get_variable("y").get_values().to_pandas().values
                y = list()
                for i in range(0, n):
                    if (i + 1) in compIndSetList:
                        y.append(ypd[0][0])
                        ypd = np.delete(ypd,0,0)
                    else:
                        y.append(0)
            sollist = list()
            for i in range(0,n):
                sollist.append(x[i]+y[i])
            soltuple = tuple(sollist)
            print(f'La solución es {soltuple}')
            R = max(list(map(lambda x: abs(x), soltuple))) + 1
        else:
            soltuple = None
            print('El problema no tiene solución')
            R = 10
        plotspan = ''
        if solsgn == '<=':
            plotspan += f'-{R}'+',0}'
        else:
            plotspan += f'0,{R}'+'}'
        sgngrad = ''
        if probtype == 'minimize':
            sgngrad = '-'
        else:
            sgngrad = ''
        if n == 2:
            if soltuple != None:
              Listplot2D = 'ListPlot[{{'+ f'{list(soltuple)[0]} , {list(soltuple)[1]}' +'}} -> {"'+f'{soltuple}'+'"}, PlotRange -> {{' + plotspan + ', {' + plotspan + '}, PlotStyle -> Directive[PointSize[Large], Red]],'
            else:
              Listplot2D = ''
            consts = f'({A[0][0]})*x + ({A[0][1]})*y {ineqs[0]} {b[0]}'
            for i in range(1, m):
                consts += f' && ({A[i][0]})*x + ({A[i][1]})*y {ineqs[i]} {b[i]}'
            lineswmath = ['Show[ContourPlot['+f'({c[0]}*x + {c[1]}*y)'+', {x,' + plotspan + ', {y,' + plotspan + ', ContourStyle -> Opacity[0.5], Contours -> 50],RegionPlot[' + consts + ',{x,' + plotspan + ', {y,' + plotspan + ', PlotPoints -> 100, PlotStyle -> Directive[Purple, Opacity[0.8]]],' + f'{Listplot2D}' + 'VectorPlot[Evaluate@Grad['+sgngrad+ f'({c[0]}*x + {c[1]}*y)'+', {x, y}], {x,' + plotspan +', {y,' + plotspan + ', VectorScale -> Small, VectorPoints -> Coarse, VectorStyle -> Green]]']
            wmath.writelines(line + '\n' for line in lineswmath)
            wmath.close()
            mathfile = open(f'{name}.nb', 'r').read()
            key = SecuredAuthenticationKey(
                'CHOGj5GchiB0tMPRNk8genB9IhpnrAMuR3iC39lSE4U=',
                'mmCL94BkmyACjNvMmmgQnept+D9VzCi0pus6+fBM13c=')
            session = WolframCloudSession(credentials=key)
            session.start()
            session.authorized()
            with session:
              plot = session.evaluate(wlexpr(lineswmath[0]))
              img_data = session.evaluate(wl.ExportByteArray(plot, 'PNG'))
              img = Image.open(io.BytesIO(img_data))
            return img
        elif n == 3:
            if soltuple != None:
              Listplot3D = ' ListPointPlot3D[{{'+ f'{list(soltuple)[0]} , {list(soltuple)[1]} , {list(soltuple)[2]}' +'}}, PlotRange -> {{' + plotspan + ', {' + plotspan + '}, PlotStyle -> Directive[PointSize[Large], Red]],'
            else:
              Listplot3D = ''
            consts = f'({A[0][0]})*x + ({A[0][1]})*y + ({A[0][2]})*z {ineqs[0]} {b[0]}'
            for i in range(1, m):
                consts += f' && ({A[i][0]})*x + ({A[i][1]})*y + ({A[i][2]})*z {ineqs[i]} {b[i]}'
            lineswmath = ['Show[ContourPlot3D['+f'({c[0]}*x + {c[1]}*y + {c[2]}*z)'+', {x,' + plotspan + ', {y,' + plotspan + ', {z,' + plotspan + ', ContourStyle -> Opacity[0.5], Contours -> 10],RegionPlot3D[' + consts + ',{x,' + plotspan + ', {y,' + plotspan + ', {z,' + plotspan + ', PlotPoints -> 100, PlotStyle -> Directive[Purple, Opacity[0.8]]],' + f'{Listplot3D}' + 'VectorPlot3D[Evaluate@Grad['+sgngrad+ f'({c[0]}*x + {c[1]}*y + {c[2]}*z)'+', {x, y, z}], {x,' + plotspan +', {y,' + plotspan + ', {z,' + plotspan + ', VectorScale -> Small, VectorPoints -> Coarse, VectorStyle -> Green], Axes-> true, AxesLabel -> {x,y,z}]']
            wmath.writelines(line + '\n' for line in lineswmath)
            wmath.close()
            mathfile = open(f'{name}.nb', 'r').read()
            key = SecuredAuthenticationKey(
                'CHOGj5GchiB0tMPRNk8genB9IhpnrAMuR3iC39lSE4U=',
                'mmCL94BkmyACjNvMmmgQnept+D9VzCi0pus6+fBM13c=')
            session = WolframCloudSession(credentials=key)
            session.start()
            session.authorized()
            with session:
              plot = session.evaluate(wlexpr(lineswmath[0]))
              img_data = session.evaluate(wl.ExportByteArray(plot, 'PNG'))
              img = Image.open(io.BytesIO(img_data))
            return img
        else:
            print("I cannot plot this data")
    else:
        print('Plz, enter a proper problem type: either minimize, maximize, [minimize, integer], [maximize, integer], [minimize, integer, list of int vars], [maximize, integer, list of int vars] ')