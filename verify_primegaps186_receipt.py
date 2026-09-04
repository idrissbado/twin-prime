#!/usr/bin/env python3
"""
Independent exact receipt checker for openai/PrimeGaps186.

Input:
    prime_gap_186_fresh.json
produced by the repository's prime_gap_186_certificate.py.

What this checker proves about such a receipt:
  1. the fresh cap enclosures imply the three fixed cap inequalities in
     PrimeGap186.physical_integral_bounds;
  2. every one of the 149 fresh raw source enclosures implies the corresponding
     fixed table inequality in PrimeGap186.physical_integral_bounds;
  3. the fixed table budgets reassemble exactly and give a rational final
     quotient > 1 + 1/50000.

Only Python standard-library exact rational arithmetic is used here.
The expensive numerical enclosure computation must have been performed by
prime_gap_186_certificate.py; this program checks its receipt against the
FIXED Lean axiom, rather than trusting the receipt's own final "passed" flag.
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

FIXED_DEN = F(23685317816, 10**24)
FIXED_I_UPPER = F(23685317890, 10**24)
FIXED_J_LOWER = F(90248755123, 10**24)
RHO_STAR = F(2624989, 10**7)
TARGET = F(50001, 50000)

# Each outer tuple is (root raw bound, face raw bound, rounded loss budget).
OUTER_H2 = [
(11,10,1),(2285,577,1),(11432060,2670744,12),(3056104728,915663654,3346),
(37877639997,12045112668,42720),(300901046806,102336788484,350961),
(2682803914309,980771899210,3244207),(3338737765461,1286194297547,4144522),
(7260461043003,2875471614189,9138326),(1211995036896,489032601185,1539747),
(8286469691008,3147682021553,10214338),(4616001082128,1627937050440,5482540),
(2353287968619,775291485464,2701470),(1146587714775,350863740368,1268537),
(529511465762,149562603056,562833),(229315416929,59379253693,233381),
(631278927,133008010,580),
]
OUTER_H25 = [
(27,1426,1),(1,821,1),(1,1392,1),(1,1765,1),(1,3334,1),(1,5753,1),(1,10303,1),
(1,18815,1),(1,2089,1),(1,11427,1),(16,16011,1),(14362,24579,1),
(7065761,1054524,6),(17914115,2503735,14),(260216687,37159538,197),
(3305952377,490372043,2547),(38054077523,5937779759,30064),
(352112119115,57993623042,285799),(3006707964277,529135146833,2522662),
(19352692647427,3611707956032,16720799),(14498518468563,2872865686933,12907719),
(28197429960534,5897287451435,25790569),(57148020076132,15810035599715,60116961),
(69886316496332,18805329967080,72504766),(69366993102523,18409874222209,71471327),
(62684551010344,16455348517458,64233828),(53862830801099,13997130877252,54915393),
(44981355032435,11577030541299,45639918),(36911787941323,9411611503675,37277308),
(29975466544992,7572139370727,30131606),(50573740961589,12808689167903,50903176),
(32438336646873,8046407139897,32311736),(20308616081603,4920425453752,19992702),
(12358345921158,2916712121993,12007621),(15056954296612,2833062492447,13062511),
]
# Each inner tuple is (raw bound, rounded loss budget).
OLD_INNER_H2 = [
(25777,1),(1511410893,14),(18120016651,161),(903601038105,8027),
(425243194887,3778),(4871216699917,43272),(23946432,1),
]
OLD_INNER_H25 = [
(1,1),(3229104,1),(29825526,1),(77797373079,692),(131978724894,1173),
(292684783730,2600),(5548294545493,49286),(30283518217418,269010),
(12009121688668,106678),(686922192553,6102),
]
NEW_INNER_H2 = [
(467789,1),(381747797,383),(386210860,387),(99885644276,99970),
(247732013063,247941),(381057139991,381379),(266162792752,266388),
(337097314828,337382),(34427294106,34457),(36820947233,36852),(18106118,19),
]
NEW_INNER_H25 = [
(2,1),(107126908277,107218),(1,1),(61,1),(137,1),(177471603,178),
(327802576,329),(50667881720,50711),(143104919759,143226),
(1323952422879,1325069),(697854132745,698443),(4234127556194,4237698),
(11632061739670,11641870),(3641610451935,3644681),(6136054632765,6141229),
(3690866567521,3693979),(737132501820,737755),
]

GROUPS = [
    ("outer_h2", "outer", OUTER_H2, 10, 6),
    ("outer_h25", "outer", OUTER_H25, 22, 12),
    ("old_inner_h2", "inner", OLD_INNER_H2, 5, 1),
    ("old_inner_h25", "inner", OLD_INNER_H25, 7, 2),
    ("new_inner_h2", "inner", NEW_INNER_H2, 6, 4),
    ("new_inner_h25", "inner", NEW_INNER_H25, 11, 5),
]

def frac(x):
    return F(str(x))

def upper_of(interval):
    return frac(interval["upper"])

def lower_of(interval):
    return frac(interval["lower"])

def expected_task_pattern(nlow, nrank):
    return (
        [("low", j) for j in range(nlow)]
        + [("rank_two", j) for j in range(nrank)]
        + [("high", 0)]
    )

def fail(msg):
    raise AssertionError(msg)

def check_cap(cap):
    norm = cap["normalized_forms"]["denominator"]
    i_lo = lower_of(norm)
    i_hi = upper_of(norm)
    j_lo = lower_of(cap["hybrid_numerator"])
    if i_lo < FIXED_DEN:
        fail(f"fresh I lower {i_lo} is below fixed Lean lower {FIXED_DEN}")
    if i_hi > FIXED_I_UPPER:
        fail(f"fresh I upper {i_hi} exceeds fixed Lean upper {FIXED_I_UPPER}")
    if j_lo < FIXED_J_LOWER:
        fail(f"fresh J lower {j_lo} is below fixed Lean lower {FIXED_J_LOWER}")
    return i_lo, i_hi, j_lo

def check_sources(components):
    if len(components) != 97:
        fail(f"expected 97 source components, got {len(components)}")
    pos = 0
    raw_count = 0
    group_budgets = []
    for gid, role, table, nlow, nrank in GROUPS:
        pattern = expected_task_pattern(nlow, nrank)
        if len(pattern) != len(table):
            fail(f"internal checker schedule mismatch for {gid}")
        group_budget = 0
        for row_index, (kind, local_index) in enumerate(pattern):
            row = components[pos]
            pos += 1
            task = row["task"]
            if task.get("group") != gid:
                fail(f"component {pos-1}: expected group {gid}, got {task.get('group')}")
            if task.get("kind") != kind or int(task.get("index")) != local_index:
                fail(
                    f"{gid} row {row_index}: expected {(kind,local_index)}, "
                    f"got {(task.get('kind'),task.get('index'))}"
                )

            raw = row["raw_forms"]
            if role == "outer":
                root_bound, face_bound, budget = table[row_index]
                expected_keys = {"root_square", "outer_face_square"}
                if set(raw) != expected_keys:
                    fail(f"{gid} row {row_index}: wrong raw-form keys {set(raw)}")
                root_upper = upper_of(raw["root_square"])
                face_upper = upper_of(raw["outer_face_square"])
                # Directly check the FIXED Lean denominator, not the receipt's
                # potentially different source normalization denominator.
                if root_upper > FIXED_DEN * F(root_bound, 10**18):
                    fail(f"{gid} row {row_index}: root bound fails fixed Lean table")
                if face_upper > FIXED_DEN * F(face_bound, 10**18):
                    fail(f"{gid} row {row_index}: face bound fails fixed Lean table")
                raw_count += 2
            else:
                raw_bound, budget = table[row_index]
                if set(raw) != {"inner_face"}:
                    fail(f"{gid} row {row_index}: wrong raw-form keys {set(raw)}")
                inner_upper = upper_of(raw["inner_face"])
                if inner_upper > FIXED_DEN * F(raw_bound, 10**18):
                    fail(f"{gid} row {row_index}: inner bound fails fixed Lean table")
                raw_count += 1
            group_budget += budget
        group_budgets.append(group_budget)

    if pos != 97 or raw_count != 149:
        fail(f"inventory mismatch: components={pos}, raw forms={raw_count}")
    return group_budgets

def check_exact_final(group_budgets):
    expected_groups = [38927522, 622829241, 55254, 435544, 1405159, 32422390]
    if group_budgets != expected_groups:
        fail(f"group budgets differ: {group_budgets}")
    total = sum(group_budgets)
    if total != 696075110:
        fail(f"wrong total source budget {total}")

    q = RHO_STAR * (FIXED_J_LOWER - FIXED_DEN * F(total, 10**12)) / FIXED_I_UPPER
    margin = q - TARGET
    exact_margin = F(
        9949172613708766984467,
        2960664736250000000000000000,
    )
    if margin != exact_margin or margin <= 0:
        fail(f"final exact margin failed: {margin}")
    return total, q, margin

def main(path):
    receipt = json.loads(Path(path).read_text(encoding="utf-8"))
    check_cap(receipt["cap"])
    groups = check_sources(receipt["components"])
    total, q, margin = check_exact_final(groups)

    # The producer's flag is informative only; all decisive inequalities above
    # were checked independently against the fixed Lean tables.
    producer_status = receipt.get("status")
    producer_passed = receipt.get("passed")

    print("PASS: fresh receipt implies the fixed PrimeGap186 physical-integral axiom")
    print("producer status:", producer_status, "producer passed:", producer_passed)
    print("raw inequalities checked: 149")
    print("cap/global inequalities checked: 3")
    print("group budgets:", groups)
    print("total source budget:", total)
    print("exact final quotient:", q)
    print("exact margin over 1+1/50000:", margin)
    print("decimal margin:", float(margin))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python verify_primegaps186_receipt.py prime_gap_186_fresh.json")
    main(sys.argv[1])
