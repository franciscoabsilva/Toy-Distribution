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
        children[childrenInfo[0]] = {"countryID": childrenInfo[1], "factoriesRequested": childrenInfo[2:]}
        #countries[childrenInfo[1]]["numChildren"] += 1
    return factories, countries, children

def solve(factories, countries, children):
    prob = pulp.LpProblem("ToyDistribution", pulp.LpMaximize)
    """
    # x[factory, child] = 1 if the factory provides a toy to the child, 0 otherwise
    x = {}
    for childID, childData in children.items():
        for factoryID in childData["factoriesRequested"]:
            if factoryID in factories:
                x[factoryID, childID] = pulp.LpVariable(f"x_{factoryID}_{childID}", cat="Binary")

    # y[child] = 1 if the child receives a toy, 0 otherwise
    y = {childID: pulp.LpVariable(f"y_{childID}", cat="Binary") for childID in children}
    """
    
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
    
    """
    # Restrição 1: Limite de stock por fábrica
    for factoryID, factoryData in factories.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for childID in children
                if (factoryID, childID) in x
            ) <= factoryData["factoryStock"],
            f"FactoryStock_{factoryID}",
        )

    # Restrição 2: Limite de exportação por país
    for countryID, countryData in countries.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for childID, childData in children.items()
                for factoryID in childData["factoriesRequested"]
                if (factoryID, childID) in x and factories[factoryID]["countryID"] == countryID
            ) <= countryData["maxExported"],
            f"MaxExport_{countryID}",
        )

    # Restrição 3: Mínimo de brinquedos por país
    for countryID, countryData in countries.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for childID, childData in children.items()
                for factoryID in childData["factoriesRequested"]
                if (factoryID, childID) in x and factories[factoryID]["countryID"] == countryID
            ) >= countryData["minToys"],
            f"MinToys_{countryID}",
        )

    # Restrição 4: Cada criança pode receber no máximo 1 brinquedo
    for childID, childData in children.items():
        prob += (
            pulp.lpSum(
                x[factoryID, childID]
                for factoryID in childData["factoriesRequested"]
                if (factoryID, childID) in x
            ) == y[childID],
            f"OneToy_{childID}",
        )

    # Resolver problema
    prob.solve(pulp.GLPK_CMD(msg=False))

    if pulp.LpStatus[prob.status] == "Optimal":
        return int(pulp.value(prob.objective))
    else:
        return -1
    """
    # Restrictions:
    # 0. the num of children in a contry is more or equal to the minToys 

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

    prob.solve(pulp.GLPK_CMD(msg=False))

    if pulp.LpStatus[prob.status] == "Optimal":
        return int(pulp.value(prob.objective))
    else:
        return -1



def main():
    factories, countries, children = readInput()
    """for country in countries:
        if(countries[country]["numChildren"] < countries[country]["minToys"]):
            print(-1)"""
    print(solve(factories, countries, children))



if __name__ == "__main__":
    main()