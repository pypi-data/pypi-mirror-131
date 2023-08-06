This is a library for the subject 'Differential Equations'

----------------------------------------------------------

Short documentation:

function - function, which we want to solve
h - step
x0, y0 - initial condition

----------------------------------------------------------

a,b - range
n - number of iterations

----------------------------------------------------------

- euler(function,h,x0,y0)

- improved_euler(function,h,x0,y0)

- runge_kutta2(function,h,x0,y0)

- runge_kutta3(function,h,x0,y0)

- runge_kutta4(function,h,x0,y0)

- simpson_rule(function,a,b,n,rng=[],result=0)

- trapezoidal_rule(function,a,b,n,rng=[],result=0)