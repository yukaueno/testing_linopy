from linopy import Model
import timeit
import pandas as pd
import numpy as np
import xarray as xr


########## Linopy ##########
def run_linopy(I, J, K, L, M, IJK, JKL, KLM, solve, repeats, number):
    setup = {
        "I": I,
        "J": J,
        "K": K,
        "L": L,
        "M": M,
        "IJK": IJK,
        "JKL": JKL,
        "KLM": KLM,
        "solve": solve,
        "model_function": linopy,
    }
    r = timeit.repeat(
        "model_function(I, J, K, L, M, IJK, JKL, KLM, solve)",
        repeat=repeats,
        number=number,
        globals=setup,
    )

    result = pd.DataFrame(
        {
            "I": [len(I)],
            "Language": ["Linopy"],
            "MinTime": [np.min(r)],
            "MeanTime": [np.mean(r)],
            "MedianTime": [np.median(r)],
        }
    )
    return result


def linopy(I, J, K, L, M, IJK, JKL, KLM, solve):

    x_indices = [I, J, K, L, M]  # (i, j, k, l, m)

    i_map = {char: idx for idx, char in enumerate(I)}
    j_map = {char: idx for idx, char in enumerate(J)}
    k_map = {char: idx for idx, char in enumerate(K)}
    l_map = {char: idx for idx, char in enumerate(L)}
    m_map = {char: idx for idx, char in enumerate(M)}

    x_list = [
        (i, j, k, l, m) for (i, j, k) in IJK for l in JKL[j, k] for m in KLM[k, l]
    ]

    x_indices = np.array(
        [(i_map[i], j_map[j], k_map[k], l_map[l], m_map[m]) for (i, j, k, l, m) in x_list]
    )
    mask = np.zeros((len(I), len(J), len(K), len(L), len(M)), dtype=bool)

    mask[tuple(x_indices.T)] = True

    # Inicializar o modelo
    model = Model()
    
    # Criar variáveis usando índices filtrados
    x = model.add_variables(lower=0, coords=[I, J, K, L, M], name="x", mask=mask)

    # Função objetivo
    cte = model.add_variables(lower=1, upper=1, name="cte")
    model.add_objective(1 * cte)

    # Adicionar restrições ao modelo
    for i in I:
        lhs_vars = ei_rule_linopy(x, i, IJK, JKL, KLM)
        if len(lhs_vars) > 1:
            model.add_constraints(sum(lhs_vars) >= 0, name=f"ei_rule_{i}")

    model.to_file("model_IJKLM_linopy.lp")
    # Resolver o modelo (opcional)
    if solve:
        model.solve(solver_name="gurobi", TimeLimit=2) # , OutputFlag=0

    # x_list = [
    #     (i, j, k, l, m)
    #     for (i, j, k) in IJK
    #     for (jj, kk, l) in JKL
    #     if (jj == j) and (kk == k)
    #     for (kkk, ll, m) in KLM
    #     if (kkk == k) and (ll == l)
    # ]

    # x = model.add_variables(coord=x_list, name="x")

    return model


# for (i, j, k) in IJK for l in JKL[j, k] for m in KLM[k, l]

def ei_rule_linopy(x, i, IJK, JKL, KLM):
    lhs_vars = []
    for (ii, j, k) in IJK:
        if ii == i:
            for l in JKL[j, k]:
                for m in KLM[k, l]:
                    lhs_vars.append(x.at[i, j, k, l, m])

    return lhs_vars
    


