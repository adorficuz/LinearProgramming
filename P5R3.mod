param m >= 0, integer;
param n >= 0, integer;


set R := 1..m;
set C := 1..n;

var x{C} integer;
param c{C};
param a{R,C};
param b{R};

maximize cost : sum {i in C} c[i]*x[i];

subject to const1:
  sum {j in C} a[1,j]*x[j] <= b[1];

subject to const2:
  sum {j in C} a[2,j]*x[j] <= b[2];

subject to const3:
  sum {j in C} a[3,j]*x[j] <= b[3];

subject to const4:
  sum {j in C} a[4,j]*x[j] <= b[4];

subject to const5 {j in C} :
  x[j] <= 0;
