"""Lifted-product codes over the group algebra F_2[G] of a non-abelian group G.

The construction is the lifted product of two base matrices A (m_a x n_a)
and B (m_b x n_b) whose entries are elements of F_2[G], each stored as a
list of group-element indices (its support; ``[]`` is the zero entry). An
entry of A acts by the left regular representation and an entry of B by
the right regular representation:

    L(g)[g h, h] = 1        R(g)[h, h g] = 1        (h ranges over G)

Left and right multiplication commute, so H_X H_Z^T = 0 for every finite
group, abelian or not. With four weight-3 entries in 1x2 bases this is the
weight-9 construction of arXiv:2607.28795 (mitten codes) and
arXiv:2607.27644 (ZSZ lifted products); lower entry weights give check
weight 6, 7 or 8, and other base shapes (1x3, 2x3 monomial) give other
rates.

Qubit layout, each block holding |G| qubits: sector 1 holds the blocks
(i, j) for i in cols(A), j in cols(B) at block index i n_b + j; sector 2
holds the blocks (r, s) for r in rows(A), s in rows(B) at block index
r m_b + s after sector 1. The checks are

    X-check (r, j):  L(A[r][i])   on block (i, j) for every i,
                     R(B[s][j])   on block (r, s) for every s;
    Z-check (i, s):  R(B[s][j])^T on block (i, j) for every j,
                     L(A[r][i])^T on block (r, s) for every r.

The convention R(g)[h, h g] = 1 for the right blocks (the transpose of
``group_algebra.R_rep``) is pinned by ``build_150_30_10``: with it, the
four trinomials of notes/150-30-10.md reproduce the X and Z check sets of
codes/150-30-10.json bit for bit, in the same qubit and check order (see
research/test_nonabelian_lp.py).

Parameters that follow from the shape alone (``lp_shape``):

    n = (n_a n_b + m_a m_b) |G|,   k >= (n_a - m_a)(n_b - m_b) |G|,
    w_X = max row weight of A + max column weight of B,
    w_Z = max column weight of A + max row weight of B,

where the weight of an entry is its support size.

``sample_nonabelian_lp`` yields ``(spec, HX, HZ)`` like the samplers in
``search.py``; ``rebuild(spec)`` turns a spec back into ``(HX, HZ)``.
"""

import numpy as np
from group_algebra import cyclic_product, direct_product, metacyclic, perm_group


# ----------------------------------------------------------------------
#  Groups
# ----------------------------------------------------------------------
def zsz(l1, l2, q):
    """Cayley table of Z_l1 x|_q Z_l2 with relation y x = x^q y.

    Element x^a y^b sits at index a*l2 + b, identity at 0. Requires
    q^l2 = 1 mod l1; the group is non-abelian iff q != 1 mod l1.
    """
    assert pow(q, l2, l1) == 1, f"q^l2 != 1 mod l1: {q}^{l2} mod {l1}"
    mul, _ = metacyclic(l1, l2, q)
    return mul


def zsz_index(l1, l2, a, b):
    """Index of x^a y^b in ``zsz(l1, l2, q)``."""
    return (a % l1) * l2 + (b % l2)


def zsz_params(n_min, n_max, *, l2_max=8, nonabelian_only=True):
    """All (l1, l2, q) with n_min <= l1*l2 <= n_max and q^l2 = 1 mod l1.

    q ranges over 1 < q < l1 (q = 1 is the abelian direct product and is
    included only with ``nonabelian_only=False``). Presentations of the same
    abstract group are not deduplicated.
    """
    out = []
    for l1 in range(3, n_max + 1):
        for l2 in range(2, l2_max + 1):
            order = l1 * l2
            if order < n_min or order > n_max:
                continue
            for q in range(2 if nonabelian_only else 1, l1):
                if pow(q, l2, l1) == 1:
                    out.append((l1, l2, q))
    return out


def element_orders(mul):
    """Order of every group element, from the Cayley table."""
    size = mul.shape[0]
    orders = np.zeros(size, dtype=int)
    for g in range(size):
        x, o = g, 1
        while x != 0:
            x = mul[x, g]
            o += 1
        orders[g] = o
    return orders


def inverses(mul):
    """Inverse of every group element, from the Cayley table."""
    size = mul.shape[0]
    inv = np.zeros(size, dtype=int)
    for g in range(size):
        inv[g] = int(np.where(mul[g] == 0)[0][0])
    return inv


def small_nonabelian_groups(n_min, n_max):
    """Non-metacyclic non-abelian groups from the kit's permutation machinery.

    Returns ``(name, mul)`` pairs with n_min <= |G| <= n_max: A4, S4, A5,
    C_m x A4, C_m x S4 (m = 2..12) and C_m x D_k (m = 2..12, k = 3..39).
    """
    cands = []
    a4 = perm_group([(1, 2, 0, 3), (1, 0, 3, 2)], 4)
    s4 = perm_group([(1, 0, 2, 3), (1, 2, 3, 0)], 4)
    a5 = perm_group([(1, 2, 0, 3, 4), (0, 1, 3, 4, 2)], 5)
    cands += [("A4", a4[0]), ("S4", s4[0]), ("A5", a5[0])]
    for m in range(2, 13):
        cm, _ = cyclic_product(m)
        for name, mul in (("A4", a4[0]), ("S4", s4[0])):
            dp, _ = direct_product(cm, mul)
            cands.append((f"C{m}x{name}", dp))
    for m in range(2, 13):
        for k in range(3, 40):
            if m * 2 * k > n_max:
                continue
            cm, _ = cyclic_product(m)
            dk, _ = metacyclic(k, 2, k - 1)
            dp, _ = direct_product(cm, dk)
            cands.append((f"C{m}xD{k}", dp))
    return [(nm, mul) for nm, mul in cands if n_min <= mul.shape[0] <= n_max]


def group_from_name(name, order=None):
    """Cayley table for a group named as in a sampler spec.

    ``"ZSZ(l1,l2,q)"`` builds ``zsz(l1, l2, q)``; any other name is looked up
    in ``small_nonabelian_groups`` (``order`` narrows the search).
    """
    if name.startswith("ZSZ("):
        l1, l2, q = (int(x) for x in name[4:-1].split(","))
        return zsz(l1, l2, q)
    lo, hi = (order, order) if order else (1, 10**6)
    return dict(small_nonabelian_groups(lo, hi))[name]


# ----------------------------------------------------------------------
#  Lifted product with the left and right regular representations
# ----------------------------------------------------------------------
def left_block(mul, supp):
    """Sum over g in ``supp`` of L(g), with L(g)[g h, h] = 1."""
    size = mul.shape[0]
    block = np.zeros((size, size), dtype=np.int8)
    ar = np.arange(size)
    for g in supp:
        block[mul[g, :], ar] ^= 1
    return block


def right_block(mul, supp):
    """Sum over g in ``supp`` of R(g), with R(g)[h, h g] = 1."""
    size = mul.shape[0]
    block = np.zeros((size, size), dtype=np.int8)
    ar = np.arange(size)
    for g in supp:
        block[ar, mul[:, g]] ^= 1
    return block


def lifted_product_base(mul, A, B):
    """Lifted product of base matrices A (m_a x n_a) and B (m_b x n_b).

    Entries are lists of group-element indices (supports in F_2[G]; ``[]``
    is the zero entry). Returns ``(HX, HZ)`` as int8 arrays in the layout
    described in the module docstring.
    """
    size = mul.shape[0]
    m_a, n_a = len(A), len(A[0])
    m_b, n_b = len(B), len(B[0])
    n1 = n_a * n_b * size
    n = n1 + m_a * m_b * size
    LA = {(r, i): left_block(mul, A[r][i]) for r in range(m_a) for i in range(n_a)}
    RB = {(s, j): right_block(mul, B[s][j]) for s in range(m_b) for j in range(n_b)}
    HX = np.zeros((m_a * n_b * size, n), dtype=np.int8)
    HZ = np.zeros((n_a * m_b * size, n), dtype=np.int8)
    for r in range(m_a):
        for j in range(n_b):
            row0 = (r * n_b + j) * size
            for i in range(n_a):
                col0 = (i * n_b + j) * size
                HX[row0 : row0 + size, col0 : col0 + size] = LA[(r, i)]
            for s in range(m_b):
                col0 = n1 + (r * m_b + s) * size
                HX[row0 : row0 + size, col0 : col0 + size] = RB[(s, j)]
    for i in range(n_a):
        for s in range(m_b):
            row0 = (i * m_b + s) * size
            for j in range(n_b):
                col0 = (i * n_b + j) * size
                HZ[row0 : row0 + size, col0 : col0 + size] = RB[(s, j)].T
            for r in range(m_a):
                col0 = n1 + (r * m_b + s) * size
                HZ[row0 : row0 + size, col0 : col0 + size] = LA[(r, i)].T
    return HX, HZ


def lp_shape(order, A_w, B_w):
    """Exact (n, k_min, wX, wZ) from the entry-weight profiles alone.

    ``A_w`` and ``B_w`` are matrices of entry weights (support sizes), so
    this needs no group and no build.
    """
    m_a, n_a = len(A_w), len(A_w[0])
    m_b, n_b = len(B_w), len(B_w[0])
    n = (n_a * n_b + m_a * m_b) * order
    k_min = (n_a - m_a) * (n_b - m_b) * order
    row_a = [sum(A_w[r]) for r in range(m_a)]
    col_a = [sum(A_w[r][i] for r in range(m_a)) for i in range(n_a)]
    row_b = [sum(B_w[s]) for s in range(m_b)]
    col_b = [sum(B_w[s][j] for s in range(m_b)) for j in range(n_b)]
    return n, k_min, max(row_a) + max(col_b), max(col_a) + max(row_b)


def rebuild(spec):
    """Rebuild ``(HX, HZ)`` from a spec yielded by ``sample_nonabelian_lp``."""
    mul = group_from_name(spec["group"], spec.get("N"))
    return lifted_product_base(mul, spec["A"], spec["B"])


# ----------------------------------------------------------------------
#  Sampler
# ----------------------------------------------------------------------
def _random_entry(rng, order, w, with_identity, min_order=None, orders=None):
    """Random support of size w; None when the pool is too small."""
    if w == 1:
        # A monomial entry is a random group element. Forcing the identity
        # here would make every monomial block identical.
        return [int(rng.integers(order))]
    pool = np.arange(1, order)
    if min_order is not None and orders is not None:
        pool = pool[orders[pool] >= min_order]
    if with_identity:
        if w - 1 > len(pool):
            return None
        rest = rng.choice(pool, size=w - 1, replace=False)
        return sorted([0] + [int(x) for x in rest])
    return sorted(int(x) for x in rng.choice(np.arange(order), size=w, replace=False))


def sample_nonabelian_lp(num, *, groups, A_w, B_w, seed=0, n_max=700, with_identity=True, min_order=None, audit=None):
    """Yield ``num`` random ``(spec, HX, HZ)`` lifted-product candidates.

    ``groups`` is a list of ``(name, mul)`` pairs (``zsz`` tables named
    ``"ZSZ(l1,l2,q)"``, or ``small_nonabelian_groups`` output). ``A_w`` and
    ``B_w`` are entry-weight profiles, e.g. ``A_w=[[3, 2]]``, ``B_w=[[3, 2]]``
    for the check-weight-8 shape. Entries of weight >= 2 contain the identity
    when ``with_identity`` is set (no loss of generality for one-row bases:
    multiplying an entry by a group element permutes qubits and checks);
    weight-1 entries are random group elements. ``min_order`` restricts the
    non-identity support elements to orders >= that value (a weight-2 entry
    1 + g gives a classical codeword of weight ord(g)). Pass ``audit`` as a
    dict to receive counts under ``sampled``, ``rejected_n`` and ``built``.

    The spec is ``{"family": "nonabelian-lp", "group", "N", "A", "B", "w"}``;
    ``rebuild(spec)`` returns the same ``(HX, HZ)``.
    """
    rng = np.random.default_rng(seed)
    tally = audit if audit is not None else {}
    for key in ("sampled", "rejected_n", "built"):
        tally.setdefault(key, 0)
    orders_cache = {}
    made = 0
    guard = 0
    while made < num and guard < 50 * num + 100:
        guard += 1
        name, mul = groups[int(rng.integers(len(groups)))]
        order = mul.shape[0]
        n, _k_min, wX, wZ = lp_shape(order, A_w, B_w)
        tally["sampled"] += 1
        if n > n_max:
            tally["rejected_n"] += 1
            continue
        if name not in orders_cache:
            orders_cache[name] = element_orders(mul)
        orders = orders_cache[name]
        A = [[_random_entry(rng, order, w, with_identity, min_order, orders) for w in row] for row in A_w]
        B = [[_random_entry(rng, order, w, with_identity, min_order, orders) for w in row] for row in B_w]
        if any(e is None for row in A + B for e in row):
            continue
        HX, HZ = lifted_product_base(mul, A, B)
        tally["built"] += 1
        made += 1
        yield (
            {"family": "nonabelian-lp", "group": name, "N": int(order), "A": A, "B": B, "w": int(max(wX, wZ))},
            HX,
            HZ,
        )


# ----------------------------------------------------------------------
#  The board's [[150,30,10]] (ZSZ(15,2,11), four trinomials)
# ----------------------------------------------------------------------
def build_150_30_10():
    """Rebuild codes/150-30-10.json from the trinomials of notes/150-30-10.md.

    ZSZ(15, 2, 11) with a = 1 + x^11 + x^12 y, b = 1 + y + x^6 y as the row
    of A and c = 1 + x^3 + x^11, d = 1 + x^6 + x^14 y as the row of B. The
    result matches the board file's X and Z check sets exactly, which is
    what fixes the R(g)[h, h g] = 1 convention used for the right blocks.
    """
    l1, l2, q = 15, 2, 11
    mul = zsz(l1, l2, q)

    def ix(a, b):
        return zsz_index(l1, l2, a, b)

    a = [ix(0, 0), ix(11, 0), ix(12, 1)]
    b = [ix(0, 0), ix(0, 1), ix(6, 1)]
    c = [ix(0, 0), ix(3, 0), ix(11, 0)]
    d = [ix(0, 0), ix(6, 0), ix(14, 1)]
    return lifted_product_base(mul, [[a, b]], [[c, d]])
