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
        countries[countryID] = {"maxExported": maxExported, "minToys": minToys , "numChildren": 0}
    
    children = {}
    for _ in range(childrenCount):
        childrenInfo = list(map(int, input().split()))
        children[childrenInfo[0]] = {"countryID": childrenInfo[1], "factoriesRequested": childrenInfo[2:]}
        countries[childrenInfo[1]]["numChildren"] += 1
    return factories, countries, children

def solve(factories, countries, children):
    prob = pulp.LpProblem("ToyDistribution", pulp.LpMaximize)
    
    # x[factory, child] = 1 if the factory provides a toy to the child, 0 otherwise
    x = pulp.LpVariable.dicts(
        "x", 
        ((factory, child) 
        for child in children 
        for factory in children[child]["factoriesRequested"]
        if factories[factory]["factoryStock"] > 0),
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
    for factoryID, factoryData in factories.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for childID in children
                if (factoryID, childID) in x
            ) <= factoryData["factoryStock"],
            f"FactoryStock_{factoryID}",
        )

    # 2. Each country has a limit of toys that can be exported
    for countryID, countryData in countries.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for childID, childData in children.items()
                for factoryID in childData["factoriesRequested"]
                if (factoryID, childID) in x and factories[factoryID]["countryID"] == countryID
                and childData["countryID"] != countryID
            ) <= countryData["maxExported"],
            f"MaxExport_{countryID}",
        )

    # 3. Each country has a minimum number of toys that must be delivered
    for countryID, countryData in countries.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for childID, childData in children.items()
                for factoryID in childData["factoriesRequested"]
                if (factoryID, childID) in x and childData["countryID"] == countryID
            ) >= countryData["minToys"],
            f"MinToys_{countryID}",
        )

    # 4. Each child receives at most one toy
    for childID, childData in children.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for factoryID in childData["factoriesRequested"]
                if (factoryID, childID) in x
            ) == y[childID],
            f"OneToy_{childID}",
        )

    # Solve the problem
    prob.solve(pulp.GLPK_CMD(msg=False))

    if pulp.LpStatus[prob.status] == "Optimal":
        return int(pulp.value(prob.objective))
    else:
        return -1

def main():
    factories, countries, children = readInput()
    for country in countries:
        if(countries[country]["numChildren"] < countries[country]["minToys"]):
            print(-1)
            return

    print(solve(factories, countries, children))



if __name__ == "__main__":
    main()