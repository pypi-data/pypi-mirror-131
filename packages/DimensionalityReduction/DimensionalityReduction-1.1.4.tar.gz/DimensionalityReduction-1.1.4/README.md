DimensionalityReduction aims to help the users to perfrom a chained dimensionality reduction techniques on a dataset automatically. 

This package is inspired by: 
PyData DC 2016 | A Practical Guide to Dimensionality Reduction 
Vishal Patel
October 8, 2016

Quick Start:
	!pip install DimensionalityReduction
	
	from DimensionalityReduction import DimensionalityReduction
	
	dr = DimensionalityReduction()
	
	dr.fit(<<dataset>>, <<target_name>>)
	
	dr.plot()
    
