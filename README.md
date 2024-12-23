# Toy Distribution
Final Project for Analysis and Synthesis of Algorithms

## Introduction
This project focuses on optimizing the distribution of Christmas toys produced by factories across multiple countries. The goal is to maximize the number of children who receive a toy they requested, while adhering to production limits, export restrictions, and fairness constraints imposed by each country. The solution is implemented in Python, utilizing the PuLP library to solve the linear programming model efficiently. The program processes input data about factories, countries, and children’s requests, then outputs the maximum number of satisfied requests or indicates if the constraints cannot be fulfilled.

## Input & Output
The input file should be a `.txt` file that contain the following:

- The first line contains three integers `factoriesCount`, `countriesCount` and `childrenCount`, representing the number of factories, countries and childs.
- The next `factoriesCount` lines each contain three integers `factoryID`, `countryID` and `factoryStock`, representing the identifier of the factory, the identifier of country where the factory is located and the stock of toys available in the factory.
- The next `countriesCount` lines each contain three integers `countryID`, `maxExported` and `minToys`, representing the identifier of the country, the maximum number of toys that can be exported from the country and  the minimum number of toys required to be delivered within the country.
- The next `childrenCount` lines each contain at least three integers `childrenID`, `countryID` representing the identifier of the child and the identifier of the country where the child lives. The rest of the integers `factoryID` in that line represent the identifiers of factories that produce the toys the child wants.
  
The output will be printed to stdout and will contain the follow:

- If it is impossible to satisfy the constraints, output `-1`.
- Otherwise the maximum number of children whose requests can be satisfied, while respecting all constraints.

### Example:
```bash
3 3 5
1 1 1
2 2 2
3 3 2
1 1 1
2 2 1
3 2 1
1 1 3
2 1 1
3 2 3
4 3 1 2
5 3 1
```
The output should be:
```bash
4
```
## Requirements and Execution

To run the program you'll need the following requirements:
```bash
# Python PuLP Library
python -m pip install pulp
```
```bash
# GLPK LP Solver
sudo apt-get install glpk-utils
```

When you meet all requirements, you can run the program with the following command:
```bash
python3 toyDistribution.py < filename.txt
```

