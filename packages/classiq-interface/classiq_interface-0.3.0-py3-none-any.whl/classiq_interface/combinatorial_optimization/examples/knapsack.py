from typing import List, Optional

import numpy as np
import pyomo.core as pyo


def knapsack(
    values: List[int], upper_bounds: List[int], max_weight: Optional[int] = None
) -> pyo.ConcreteModel:
    assert len(values) == len(
        upper_bounds
    ), "values and upper_bounds must be with the same length"
    model = pyo.ConcreteModel()

    def bounds(model, i):
        return 0, upper_bounds[i]

    model.x = pyo.Var(range(len(values)), domain=pyo.NonNegativeIntegers, bounds=bounds)

    if max_weight is not None:
        model.weight_constraint = pyo.Constraint(
            expr=sum(model.x.values()) <= max_weight
        )

    model.cost = pyo.Objective(
        expr=values @ np.array(model.x.values()), sense=pyo.maximize
    )

    return model
