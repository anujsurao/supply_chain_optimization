import pulp
from database import db, Factory, Warehouse, Store, Cost

def optimize_supply_chain():
    factories = Factory.query.all()
    warehouses = Warehouse.query.all()
    stores = Store.query.all()

    supply = {f.name: f.supply for f in factories}
    demand = {s.name: s.demand for s in stores}

    cost_factory_to_warehouse = {(c.from_id, c.to_id): c.cost for c in Cost.query.filter_by(type="factory_to_warehouse").all()}
    cost_warehouse_to_store = {(c.from_id, c.to_id): c.cost for c in Cost.query.filter_by(type="warehouse_to_store").all()}

    prob = pulp.LpProblem("Supply_Chain_Optimization", pulp.LpMinimize)

    factory_to_warehouse = pulp.LpVariable.dicts("Factory_to_Warehouse",
                                                 [(f.id, w.id) for f in factories for w in warehouses],
                                                 lowBound=0,
                                                 cat='Continuous')

    warehouse_to_store = pulp.LpVariable.dicts("Warehouse_to_Store",
                                               [(w.id, s.id) for w in warehouses for s in stores],
                                               lowBound=0,
                                               cat='Continuous')

    prob += pulp.lpSum([cost_factory_to_warehouse[(f.id, w.id)] * factory_to_warehouse[(f.id, w.id)] for f in factories for w in warehouses]) + \
            pulp.lpSum([cost_warehouse_to_store[(w.id, s.id)] * warehouse_to_store[(w.id, s.id)] for w in warehouses for s in stores])

    for f in factories:
        prob += pulp.lpSum([factory_to_warehouse[(f.id, w.id)] for w in warehouses]) <= supply[f.name], f"Supply_Constraint_{f.name}"

    for s in stores:
        prob += pulp.lpSum([warehouse_to_store[(w.id, s.id)] for w in warehouses]) >= demand[s.name], f"Demand_Constraint_{s.name}"

    for w in warehouses:
        prob += pulp.lpSum([factory_to_warehouse[(f.id, w.id)] for f in factories]) == pulp.lpSum([warehouse_to_store[(w.id, s.id)] for s in stores]), f"Flow_Balance_Constraint_{w.name}"

    prob.solve()

    results = {
        "factory_to_warehouse": {k: v.varValue for k, v in factory_to_warehouse.items()},
        "warehouse_to_store": {k: v.varValue for k, v in warehouse_to_store.items()},
        "total_cost": pulp.value(prob.objective)
    }
    
    return results
