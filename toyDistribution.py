import pulp

def readInput():
    factoriesCount, countriesCount, childrenCount = map(int, input().split())

    factories = {}
    for _ in range(factoriesCount):
        factoryID, countryID, factoryStock = map(int, input().split())
        factories[factoryID] = {"countryID": countryID, "factoryStock": factoryStock}

    countries = {}
    for _ in range(countriesCount):
        countryID, maxExported, minToys = map(int, input().split())
        countries[countryID] = {"maxExported": maxExported, "minToys": minToys}

    children = {}
    for _ in range(childrenCount):
        childrenInfo = list(map(int, input().split()))
        childrenID = childrenInfo[0]
        countryID = childrenInfo[1]
        factoriesRequested = childrenInfo[2:]
        children[childrenID] = {"countryID": countryID, "factoriesRequested": factoriesRequested}
    
    return factories, countries, children

def solve(factories, countries, children):
    prob = pulp.LpProblem("ToyDistribution", pulp.LpMaximize)

    # x[factory, child] = 1 if the factory provides a toy to the child, 0 otherwise
    x = pulp.LpVariable.dicts(
        "x", 
        ((factory, child) 
        for factory in factories 
        for child in children), 
        cat="Binary"
    )

    # y[child] = 1 if the child receives a toy, 0 otherwise
    y = pulp.LpVariable.dicts(
        "y", 
        (child 
        for child in children), 
        cat="Binary"
    )

    # Objective function (maximize the number of children that receive a requested toy)
    prob += pulp.lpSum(y[child] for child in children), "MaximizeRequests"

    # Restrictions:
    # 1. Each factory has a stock limit
    for factory in factories:
        prob += (
            pulp.lpSum(x[factory, child] for child in children) 
            <= factories[factory]["factoryStock"], 
            "factoryStock_{}".format(factory)
        )

    # 2. Each country has a limit of toys that can be exported
    for countryID, countryInfo in countries.items():
        prob += (
            pulp.lpSum(
                x[factory, child]
                for factory in factories
                for child in children
                if factories[factory]["countryID"] == countryID
            ) <= countryInfo["maxExported"], 
            "maxExported_{}".format(countryID)
        )

    # 3. Each country has a minimum number of toys that must be delivered
    for countryID, countryInfo in countries.items():
        prob += (
            pulp.lpSum(
                x[factory, child]
                for factory in factories
                for child in children
                if factories[factory]["countryID"] == countryID
            ) >= countryInfo["minToys"], 
            "minToys_{}".format(countryID)
        )

    # 4. Each child receives at most one toy
    for child in children:
        prob += (
            pulp.lpSum(
                x[factory, child] 
                for factory in children[child]["factoriesRequested"]
            ) == y[child], 
            "childToy_{}".format(child)
        )

    prob.solve(pulp.GLPK(msg=False))

    if pulp.LpStatus[prob.status] == "Optimal":
        return int(pulp.value(prob.objective))
    else:
        return -1



def main():
    factories, countries, children = readInput()
    print(solve(factories, countries, children))



if __name__ == "__main__":
    main()