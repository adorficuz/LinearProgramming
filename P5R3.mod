param m >= 0, integer;
param n >= 0, integer;


set R := 1..m;
set C := 1..n;
set I := {1};
set J := {2};

var x{I} integer;
var y{J};
param c{C};
param a{R,C};
param b{R};

maximize cost : sum {i in I} c[i]*x[i] + sum {j in J} c[j]*y[j];

subject to const1:
  sum {j in I} a[1,j]*x[j] + sum {k in J} a[1,k]*y[k] <= b[1];

subject to const2:
  sum {j in I} a[2,j]*x[j] + sum {k in J} a[2,k]*y[k] <= b[2];

subject to const3:
  sum {j in I} a[3,j]*x[j] + sum {k in J} a[3,k]*y[k] <= b[3];

subject to const4:
  sum {j in I} a[4,j]*x[j] + sum {k in J} a[4,k]*y[k] <= b[4];

subject to const5 {i in I} :
  x[i] <= 0;

subject to const6 {j in J} :
  y[j] <= 0;