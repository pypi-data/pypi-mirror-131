from sympy import *
import matplotlib.pyplot as plt

x = Symbol('x')
y = Symbol('y')

#-------------------------------------------------------------------------------------------------------------------
# Differential Equations

def euler(function,h,x0,y0):
	list_x = [x0]
	list_y = [y0]
	def f(x_value,y_value): 
		return function.subs({x:x_value,y:y_value})
	for i in range(5):
		y_value = y0
		x_value = x0
		y1 = y_value + h*f(x_value,y_value)
		x0 = x_value + h
		y0 = y1
		list_x.append(x0)
		list_y.append(y0)
	plt.plot(list_x,list_y,"-b",label="Euler's method")
	plt.legend()
	plt.show()

def improved_euler(function,h,x0,y0):
	list_x = [x0]
	list_y = [y0]
	def f(x_value,y_value): 
		return function.subs({x:x_value,y:y_value})
	for i in range(5):
		y_value = y0
		x_value = x0
		y1 = y_value + h/2*(f(x_value,y_value)+f(x_value+h,y_value+h*f(x_value,y_value)))
		x0 = x_value + h
		y0 = y1
		list_x.append(x0)
		list_y.append(y0)
	plt.plot(list_x,list_y,"-b",label="Improved Euler's method")
	plt.legend()
	plt.show()

def runge_kutta2(function,h,x0,y0):
	list_x = [x0]
	list_y = [y0]
	def f(x_value,y_value): 
		return function.subs({x:x_value,y:y_value})
	for i in range(5):
		y_value = y0
		x_value = x0
		k1 = f(x_value,y_value)
		k2 = f(x_value + h,y_value + k1*h)
		y1 = y_value + (k1/2+k2/2)*h
		x0 = x_value + h
		y0 = y1
		list_x.append(x0)
		list_y.append(y0)
	plt.plot(list_x,list_y,"-b",label="Runge-Kutta II method")
	plt.legend()
	plt.show()

def runge_kutta3(function,h,x0,y0):
	list_x = [x0]
	list_y = [y0]
	def f(x_value,y_value): 
		return function.subs({x:x_value,y:y_value})
	for i in range(5):
		y_value = y0
		x_value = x0
		k1 = f(x_value,y_value)
		k2 = f(x_value + (h/2),y_value + k1*h/2)
		k4 = f(x_value + h,y_value + k1*h) 
		k3 = f(x_value + h,y_value + k4*h)
		y1 = y_value + (h/6)*(k1 + 4*k2 + k3)
		x0 = x_value + h
		y0 = y1
		list_x.append(x0)
		list_y.append(y0)
	plt.plot(list_x,list_y,"-b",label="Runge-Kutta III method")
	plt.legend()
	plt.show()

def runge_kutta4(function,h,x0,y0):
	list_x = [x0]
	list_y = [y0]
	def f(x_value,y_value): 
		return function.subs({x:x_value,y:y_value})
	for i in range(5):
		y_value = y0
		x_value = x0
		k1 = f(x_value,y_value)
		k2 = f(x_value + (h/2),y_value + k1*h/2)
		k3 = f(x_value + (h/2),y_value + k2*h/2)
		k4 = f(x_value + h,y_value + k3*h) 
		y1 = y_value + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
		x0 = x_value + h
		y0 = y1
		list_x.append(x0)
		list_y.append(y0)
	plt.plot(list_x,list_y,"-b",label="Runge-Kutta IV method")
	plt.legend()
	plt.show()	

#-------------------------------------------------------------------------------------------------------------------
# Integrals

def delta(a,b,n):
	return (b-a)/n

def simpson_rule(function,a,b,n,rng=[],result=0):
	def f(t):
		return function.subs(x,t)
	for i in range(a,b):
		rng.append(i)
		rng.append(i+b/n)
	rng.append(b)
	result+=f(a)
	for i in range(1,len(rng)-1):
		if i%2!=0:
			result+=4*f(rng[i])
		if i%2==0:
			result+=2*f(rng[i])
	result+=f(b)
	return (delta(a,b,n)/3)*result

def trapezoidal_rule(function,a,b,n,rng=[],result=0):
	def f(t):
		return function.subs(x,t)
	for i in range(a,b):
		rng.append(i)
		rng.append(i+b/n)
	rng.append(b)
	result+=f(a)
	for i in range(1,len(rng)-1):
		result+=2*f(rng[i])
	result+=f(b)
	return (delta(a,b,n)/2)*result