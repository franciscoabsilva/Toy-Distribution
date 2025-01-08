import pulp

def readInput():
    factoriesCount, countriesCount, childrenCount = map(int, input().split())
    x = {}

    factories = {}
    for _ in range(factoriesCount):
        factoryID, countryID, factoryStock = map(int, input().split())
        factories[factoryID] = {"countryID": countryID, "factoryStock": factoryStock, "kids": []}

    countries = {}
    for _ in range(countriesCount):
        countryID, maxExported, minToys = map(int, input().split())
        countries[countryID] = {"maxExported": maxExported, "minToys": minToys , "numChildren": 0,  "exportList": [], "importList": []}
    
    children = {}
    for _ in range(childrenCount):
        childrenInfo = list(map(int, input().split()))
        children[childrenInfo[0]] = {"countryID": childrenInfo[1], "factoriesRequested": childrenInfo[2:]}
        for factory in childrenInfo[2:]:
            x[factory, childrenInfo[0]] = pulp.LpVariable(f"x_{childrenInfo[0]}_{factory}", 0, 1, pulp.LpBinary)
            factories[factory]["kids"].append(x[factory, childrenInfo[0]])
            if factories[factory]["countryID"] == childrenInfo[1]:
                countries[childrenInfo[1]]["importList"].append(x[factory, childrenInfo[0]])
            else:
                countries[factories[factory]["countryID"]]["exportList"].append(x[factory, childrenInfo[0]])
        countries[childrenInfo[1]]["numChildren"] += 1
    return factories, countries, children, x

def solve(factories, countries, children, x):
    prob = pulp.LpProblem("ToyDistribution", pulp.LpMaximize)

    # Objective function (maximize the number of children that receive a requested toy)
    prob += pulp.lpSum(x[factory, child] for child in children for factory in children[child]["factoriesRequested"] if (factory, child) in x), "MaximizeRequests"
    
    # Restrictions:

    # 1. Each factory has a stock limit
    for factoryID, factoryData in factories.items():
        prob += (
            pulp.lpSum(
                kid for kid in factoryData["kids"]
            ) <= factoryData["factoryStock"],
            f"FactoryStock_{factoryID}",
        )

    # 2. Each country has a limit of toys that can be exported
    for countryID, countryData in countries.items():
        prob += (
            pulp.lpSum(
                toy for toy in countryData["exportList"]
            ) <= countryData["maxExported"],
            f"MaxExport_{countryID}",
        )

    # 3. Each country has a minimum number of toys that must be delivered
    for countryID, countryData in countries.items():
        prob += (
            pulp.lpSum(
                toy for toy in countryData["importList"]
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
            ) <= 1,
            f"OneToy_{childID}",
        )

    # Solve the problem
    prob.solve(pulp.GLPK_CMD(msg=False))

    if pulp.LpStatus[prob.status] == "Optimal":
        return int(pulp.value(prob.objective))
    else:
        return -1

def main():
    factories, countries, children, x = readInput()
    for country in countries:
        if(countries[country]["numChildren"] < countries[country]["minToys"]):
            print(-1)
            return

    print(solve(factories, countries, children, x))

if __name__ == "__main__":
    main()
