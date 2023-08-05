How to use NoLOAD ?
===================

NoLOAD syntax
-------------

To solve an optimization problem problem on Noload (for example a single-objective one), you must respect the following syntax :

First, the specifications of your model must be written with class Spec of module Specifications :

```from noload.optimization.specifications import Spec```      

```spec = Spec(variables, bounds, objectives,  eq_cstr, ineq_cstr, freeOutputs)```

with :

–	variables : a dictionary (dict) including names of the variables as dict keys and their initial values (to initialize algorithm) as dict values.

–	bounds : a dictionary including names of the variables as dict keys and their bounds as dict values, represented as a list : [min,max].

–	objectives : a list including the names of the objective(s) function(s) to minimize.

–	eq_cstr (optional): a dictionary including names of the equality constraints as dict keys and the values to respect as dict values.

–   ineq_cstr (optional):  a dictionary including names of the inequality constraints as dict keys and their bounds to respect as dict values, represented as lists : [min,max].

-   freeOutputs (optional) : a list including the names of freeOutputs, which are model variables you want to see the values without constraining them.

Then you must call the OptimProblem class to define the optimization problem :

```from noload.optimization.OptimProblem import OptimProblem```

```optim = OptimProblem(model, specifications, parameters)```

with :

–	model : the function of the python file that describes your model. It must return « return locals().items() ».

–	specifications : the spec object that you define before.

–	parameters (optional): a dictionary corresponding to constant variables, including their names as dict keys and their values as dict values.

Finally, you can run the optimization with the following command :

```result=optim.run(method, ftol, maxiter)```

with :

–	method : the method used to solve the optimization problem, which can be ‘SLSQP’ for Sequential Least Square Quadratic Programming (default) or ‘LeastSquare’.

–	ftol : the tolerance of the objective function (by default it is 1e-5).

–	maxiter is the maximal number of iterations allowed to the algorithm (by default it is 500). If your problem didn’t converge in 500 iterations, indicate a higher value for this parameter.

If you want to display the results, you can use :

```result.printResults()``` to display the inputs and outputs in a dictionnary

```result.plotResults()``` to display the inputs and outputs in a graph

```result.getLastInputs()``` to return the inputs in a dictionary

```result.getLastOutputs()``` to return the outputs in a dictionary

```result.printResults()``` to display the inputs and outputs in a dictionnary

```result.printAllResults()``` to display the inputs and outputs in a dictionnary for each iteration of the optimization

```result.getIteration(iternum)``` to return the inputs and outputs in dictionnaries at the number of iteration 'iternum' given in parameter.


To compute model with some inputs values, you may use computeOnce fonction :

```from noload.analyse.simulation import computeOnce```

```result = computeOnce(model, inputs, outputs)```

with :

–	model : the function of the python file that describes your model. It must return « return locals().items() ».

–	inputs : a dictionary corresponding to constant variables, including their names as dict keys and their values as dict values.

–	outputs : a list including the names of the outputs you want to calculate.


If you want to compute model with a varying input, you must use computeParametric fonction :

```from noload.analyse.simulation import computeParametric```

```result = computeParametric(model, variable, range, inputs, outputs)```

with :

–	model : the function of the python file that describes your model. It must return « return locals().items() ».

–	variable : a character string including the names of the varying input.

–	range : a list including the different values that the varying input must take. 

–	inputs : a dictionary corresponding to constant variables, including their names as dict keys and their values as dict values.

–	outputs : a list including the names of the outputs you want to calculate.

To display the results, use :

```result.print()``` to print them numerically

```result.plotXY()``` to print them in a graph.


The case of vectorial constraints or variables :
------------------------------------------------

If you have in your problem vectorial variables or constraints, you have to respect a certain syntax :

Variables and equality constraints values must be put as follows : [coordinate1, coordinate2, ... , coordinateN].

Inequality constraints and bounds values must be put as follows : [ [min coordinate1, max coordinate1] ,  [min coordinate2, max coordinate2], ... , [min coordinateN, max coordinateN] ].


Plot Pareto for multi-objective problems :
------------------------------------------

If you optimize a multi-objective problem with 2 objective functions f1 and f2, you need to write the commands below to display it in a graph.

``` import noload.gui.plotPareto as pp```

``` pp.plot([result.resultsHandler],['f1','f2'],['legend_of_the_curve'])```
