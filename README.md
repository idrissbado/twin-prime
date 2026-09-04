# PrimeGaps186 — Independent Numerical Verification

**Author of this verification wrapper:** Idriss Olivier Bado  
**Upstream project:** `openai/PrimeGaps186`  
**Purpose:** independently recompute and check the numerical input used in the conditional Lean formalization of the prime-gap bound

\[
\boxed{\liminf_{n\to\infty}(p_{n+1}-p_n)\le 186.}
\]

This repository is a **reproducibility and audit wrapper** around the public
`openai/PrimeGaps186` project. It does not replace the Lean development and it
does not modify the upstream numerical algorithm. Instead, it rebuilds the
required arithmetic stack from pinned source snapshots, reruns the numerical
certificate from scratch, and then checks the fresh output with an independent
exact-rational post-processing verifier.

The central question is simple:

> Can the numerical inequalities assumed by the Lean theorem be reproduced
> independently, from fresh computation, with a corrected FLINT build and a
> separately written checker?

A successful workflow answers **yes** for the numerical part.

---

## 1. Mathematical objective

Let

\[
p_1<p_2<p_3<\cdots
\]

be the sequence of prime numbers, and define

\[
H_1:=\liminf_{n\to\infty}(p_{n+1}-p_n).
\]

The target statement is

\[
H_1\le 186.
\]

In words: **infinitely often, two consecutive primes occur at distance at most
186**.

The upstream Lean development does not prove this directly from the axioms of
Lean alone. Its logical structure is

\[
\text{finite-field estimates}
+\text{physical-integral bounds}
\Longrightarrow \mathrm{DHL}[40,2]
\Longrightarrow H_1\le 186.
\]

Here `DHL[40,2]` is the statement that every admissible set of 40 integer shifts
has infinitely many translates containing at least two primes.

---

## 2. Why the number 186 appears

The upstream project uses the explicit 40-tuple

\[
\begin{aligned}
\mathcal H=\{&0,2,6,12,20,26,30,32,36,42,48,50,56,60,68,72,78,86,90,92,\\
&98,102,110,116,120,126,132,138,140,146,152,156,158,162,168,170,176,180,182,186\}.
\end{aligned}
\]

Its diameter is

\[
\max \mathcal H-\min \mathcal H=186.
\]

If `DHL[40,2]` holds for this admissible tuple, then infinitely many translates

\[
n+\mathcal H
\]

contain at least two primes. Any two primes in the same translate differ by at
most 186. Standard passage to consecutive primes then gives

\[
H_1\le 186.
\]

Thus the numerical work is not trying to “search for a prime gap 186”. It is
certifying analytic inequalities that imply a distribution theorem strong
enough to force infinitely many such bounded gaps.

---

## 3. The three external inputs in the Lean development

The Lean development keeps three ingredients as explicit external assumptions.
Two are finite-field estimates from the literature; the third is a large finite
collection of numerical inequalities.

### 3.1 Rank-three Kloosterman estimate

For a prime \(p\) and \(c\in\mathbf F_p^\times\), the project uses the normalized
rank-three hyper-Kloosterman sum

\[
\mathrm{Kl}_3(c;p)
=\frac1p
\sum_{\substack{x_1x_2x_3=c\\x_i\in\mathbf F_p}}
 e_p(x_1+x_2+x_3),
\]

with

\[
e_p(x)=e^{2\pi i x/p}.
\]

The required estimate is

\[
\boxed{|\mathrm{Kl}_3(c;p)|\le 3.}
\]

This is a standard consequence of Deligne's theory, in the normalization used
by the project.

### 3.2 Rank-two Kloosterman correlation estimate

The project also uses

\[
K_2(c;p)=\sum_{u\in\mathbf F_p^\times}e_p(u+c/u)
\]

and the correlation estimate

\[
\boxed{
\left|
\sum_{t\in\mathbf F_p\setminus\{0,-1\}}
K_2(A/t;p)K_2(B/(t+1);p)
\right|
\le 8p\sqrt p.
}
\]

This is the normalization corresponding to the Fouvry--Kowalski--Michel bound
for normalized Kloosterman sums.

### 3.3 The physical-integral bounds

The numerical axiom in the Lean project is

```text
PrimeGap186.physical_integral_bounds
```

It consists of

- **104 outer inequalities**,
- **45 inner inequalities**,
- **3 global/cap inequalities**.

The 104 outer and 45 inner entries correspond to **149 raw physical-integral
enclosures**, and the 3 additional cap/global statements bring the fixed Lean
table to

\[
149+3=104+45+3=\boxed{152}
\]

inequalities in total.

The official Python producer computes the raw numerical enclosures from scratch.
Our independent checker then compares the fresh receipt to the fixed tables and
performs the final rational arithmetic again, without trusting the producer's
single Boolean field `passed: true`.

---

## 4. Where the integrals come from

The certificate is built around a Poisson--Dickman model. A convenient way to
understand the bridge is the following.

Let \(N_c\) be a Poisson point process on \((0,c]\) with intensity

\[
\frac{du}{u},
\]

and let

\[
S=\sum_{u\in N_c}u.
\]

Its Laplace transform is

\[
\mathbf E(e^{-sS})
=
\exp\!\left(
\int_0^c\frac{e^{-su}-1}{u}\,du
\right).
\]

After the standard normalization, this produces the Dickman density appearing
in the physical integrals. In particular, for appropriate test functions \(F\),

\[
e^\gamma c\,\mathbf E[F(S)]
=
\int_0^\infty F(x)\rho(x/c)\,dx,
\]

where \(\rho\) is the Dickman function.

Two identities are especially important for the rigorous reduction used by the
certificate.

### Cap/no-point identity

For \(0<z\le c\),

\[
\mathbf P\bigl(N_c((z,c])=0\bigr)
=
\exp\!\left(-\int_z^c\frac{du}{u}\right)
=
\frac zc.
\]

This allows the residual law under a “no large point” condition to be reduced
to a process with cap \(z\).

### Campbell--Mecke/Palm identity

For marked points \(u_1,\ldots,u_r\), the factorial moment expansion has the
schematic form

\[
\int\sum_{u_1,\ldots,u_r}^{\neq}
G(u_1,\ldots,u_r,N-\textstyle\sum_i\delta_{u_i})\,d\mu_c
=
\int\cdots\int
G(u_1,\ldots,u_r,N)\,d\mu_c
\prod_{i=1}^r\frac{du_i}{u_i}.
\]

This is the mechanism behind the rank-one/rank-two witness terms and the
factorial high-order tail used in the producer.

---

## 5. Rigorous Dickman discretization

For the scaled Dickman function \(f_c\),

\[
f_c(x)=1\qquad(0\le x\le c),
\]

and for \(x>c\),

\[
f_c'(x)=-\frac{f_c(x-c)}{x}.
\]

Useful deterministic bounds are

\[
0\le f_c\le 1,
\qquad
|f_c'|\le \frac1c,
\qquad
|f_c''|\le \frac1{c^2}.
\]

Therefore the trapezoid rule on a cell of width \(h\) admits the rigorous error
estimate

\[
\left|
T_h(f_c)-\int f_c
\right|
\le
\frac{h^3}{12c^2}.
\]

The implementation also has a discrete-renewal fallback. From

\[
x f_c(x)=\int_{x-c}^x f_c(t)\,dt
\]

one gets, on a grid \(x_n=nh\), \(c=Mh\),

\[
f_c(x_n)
\le
\frac1n
\sum_{j=n-M}^{n-1}f_c(x_j).
\]

Hence the recurrence used in the code is an actual upper majorant, not a
heuristic extrapolation.

---

## 6. High-order terms and Eulerian carry

The source decomposition eventually produces sums of cellwise fractional parts.
Under the dominating measure, the carry distribution is the classical Eulerian
distribution for sums of independent uniforms.

For the high-order tail, the code uses a positive coefficientwise majorant. If

\[
H(x)
\]

is the relevant generating polynomial, then the tail is controlled through

\[
\sum_{r\ge0}
\frac{H(x)^r}{r!}
(1+x+\cdots+x^{r+e})
=
\frac{e^{H(x)}-x^{e+1}e^{xH(x)}}{1-x}.
\]

The key point is that the omitted large-order terms are **majorized
positively**; they are not simply discarded.

---

## 7. Directed binary64 reduction

The producer combines very large arrays of interval endpoints using a directed
binary64 reduction. It checks the IEEE-754 environment, including
round-to-nearest and gradual underflow, and compensates ordinary floating-point
summation by a standard \(\gamma_n\)-type error term before applying
`nextafter` outward.

The certificate also verifies that its reduction length stays inside the range
for which the correction inequality is proved.

This matters because a numerical proof is only useful if every transition from
floating-point arithmetic to an enclosing interval is itself justified.

---

## 8. The signed-FFT issue and why FLINT is pinned

The official producer begins with a mandatory signed polynomial-convolution
regression test.

A rare signed FFT conversion defect in FLINT was corrected upstream. This
wrapper therefore builds FLINT exactly at

```text
7ad753d51c82fdec115cb179b41d0e581f1cb0ec
```

rather than relying on an arbitrary system package or wheel.

Before any expensive integral computation, the workflow executes

```text
PASS_SIGNED_FFT_REGRESSION
```

or aborts.

This is essential: a numerical certificate is not meaningful if the underlying
integer-polynomial convolution can silently return an incorrect signed result.

---

## 9. Exact post-processing already checked independently

The post-processing stage is deliberately simple enough to redo using Python's
standard-library `fractions.Fraction`.

The fixed cap/global quantities are

\[
I_-=\frac{23685317816}{10^{24}},
\qquad
I_+=\frac{23685317890}{10^{24}},
\]

\[
J_-=\frac{90248755123}{10^{24}},
\qquad
\rho_\star=\frac{2624989}{10^7}.
\]

The six source-budget group totals are

| group | units of \(10^{-12}\) |
|---|---:|
| outer order 2 | 38,927,522 |
| outer order \(5/2\) | 622,829,241 |
| inner base order 2 | 55,254 |
| inner base order \(5/2\) | 435,544 |
| inner enlarged order 2 | 1,405,159 |
| inner enlarged order \(5/2\) | 32,422,390 |
| **total** | **696,075,110** |

Thus

\[
\boxed{B=696075110\times10^{-12}}.
\]

The resulting exact lower quotient is

\[
Q_-
=
\frac{2960733898717338708766984467}
{2960664736250000000000000000}
=
1.000023360452297\ldots
\]

while the required threshold is

\[
1+\frac1{50000}=1.00002.
\]

The exact margin is

\[
\boxed{
Q_- - \frac{50001}{50000}
=
\frac{9949172613708766984467}
{2960664736250000000000000000}
>0.
}
\]

Numerically,

\[
Q_- - 1.00002
\approx 3.360452297\times10^{-6}.
\]

So once the fresh raw interval bounds are independently confirmed, the final
strict inequality is not a floating-point judgement: it is an **exact rational
inequality**.

---

## 10. What this workflow actually verifies

The workflow has two logically separate numerical stages.

### Stage A — official producer

The pinned upstream script

```text
prime_gap_186_certificate.py
```

recomputes the numerical certificate from scratch and writes a fresh receipt

```text
prime_gap_186_fresh.json
```

A successful producer run reports

```text
PASS_FRESH_NUMERICAL_CERTIFICATE
```

but that marker alone is not accepted as the independent verification.

### Stage B — independent receipt checker

The local file

```text
verify_primegaps186_receipt.py
```

then reads the fresh JSON and independently checks the fixed numerical data. It
verifies the raw bounds corresponding to the 104 outer and 45 inner entries,
the 3 global/cap bounds, the source budgets, and the final exact-rational
comparison.

Only after this second stage succeeds do we print

```text
PASS: fresh receipt implies the fixed PrimeGap186 physical-integral axiom
```

---

## 11. Logical meaning of a successful run

A successful run gives independent computational evidence for

```text
PrimeGap186.physical_integral_bounds
```

at the pinned upstream snapshot.

It does **not** mean that all three external inputs have suddenly become Lean
proofs. The two Kloosterman estimates remain mathematical results imported from
the literature.

Accordingly, the honest conclusion is:

> The numerical physical-integral input has been independently reproduced and
> checked. Together with the cited classical finite-field estimates, the
> upstream Lean development yields the bound \(H_1\le186\).

That is stronger and more precise than merely saying “the Python script passed”.

---

## 12. Pinned reproducibility environment

The workflow uses exactly:

- **FLINT**: `7ad753d51c82fdec115cb179b41d0e581f1cb0ec`
- **python-flint**: `572c8a213a88c0f92feb1bdb938ce4622f4517fa`
- **PrimeGaps186**: `61340d0b74163003b32756bb16e91d9209a5e330`
- **Python**: `3.12.13`
- **NumPy**: `2.2.6`

The workflow downloads source archives through GitHub `codeload` rather than
using `git clone`. This avoids the TLS/`early EOF` failure encountered in the
local Docker attempt while still fixing the exact source snapshots.

---

## 13. Repository files

```text
.
├── README.md
├── verify_primegaps186_receipt.py
└── .github/
    └── workflows/
        └── primegaps186.yml
```

- `.github/workflows/primegaps186.yml` — complete reproducible GitHub Actions run.
- `verify_primegaps186_receipt.py` — independent exact receipt checker.
- `README.md` — mathematical and reproducibility description.

---

## 14. How to run on GitHub Actions

1. Make the repository public if you want to use standard public-repository
   GitHub Actions runners without consuming Codespaces quota.
2. Commit the files in this repository.
3. Open the **Actions** tab.
4. Select **PrimeGaps186 independent numerical verification**.
5. Click **Run workflow**.
6. Keep `workers = 4` for the normal run.
7. Start the workflow.

The job then performs

\[
\text{build corrected FLINT}
\to
\text{build python-flint}
\to
\text{FFT regression}
\to
\text{fresh certificate}
\to
\text{independent checker}
\to
\text{SHA-256 seal}.
\]

---

## 15. Required successful ending

The decisive final markers are

```text
PASS_SIGNED_FFT_REGRESSION
PASS_FRESH_NUMERICAL_CERTIFICATE
PASS: fresh receipt implies the fixed PrimeGap186 physical-integral axiom
CHALLENGE_COMPLETE
```

Do not call the numerical verification complete unless the fresh run reaches all
four markers and the JSON artefact is preserved.

---

## 16. Result artefact and provenance

The workflow uploads an artefact named approximately

```text
primegaps186-verification-<run-id>-<attempt>
```

containing at least

```text
prime_gap_186_fresh.json
prime_gap_186_fresh.json.sha256
VERIFICATION_SUMMARY.txt
certificate.log
independent-checker.log
signed-fft-regression.log
source-commits.txt
flint-source.sha256
python-flint-source.sha256
primegaps186-source.sha256
python-environment.txt
pip-freeze.txt
```

These files provide the chain of provenance needed for a scientific
reproducibility record.

The most important pair is

```text
prime_gap_186_fresh.json
prime_gap_186_fresh.json.sha256
```

because the SHA-256 uniquely identifies the exact fresh receipt that was
independently checked.

---

## 17. Status table

| Component | Status after a successful workflow |
|---|---|
| Corrected FLINT signed FFT | independently regression-tested |
| Upstream numerical producer | rerun from pinned source |
| 104 outer bounds | independently checked from fresh receipt |
| 45 inner bounds | independently checked from fresh receipt |
| 3 global/cap bounds | independently checked from fresh receipt |
| exact source-budget arithmetic | independently recomputed |
| final positive rational margin | independently recomputed |
| rank-3 Kloosterman estimate | external published mathematics |
| rank-2 correlation estimate | external published mathematics |
| Lean derivation from the three inputs | upstream formalization |

---

## 18. References

1. **OpenAI**, *PrimeGaps186: conditional Lean formalization and numerical
   certificate for prime gaps at most 186*, public GitHub repository, audited
   snapshot `61340d0b74163003b32756bb16e91d9209a5e330`.
2. **N. M. Katz**, *Gauss Sums, Kloosterman Sums, and Monodromy Groups*,
   Annals of Mathematics Studies 116, Princeton University Press, 1988.
3. **É. Fouvry, E. Kowalski, P. Michel**, *The Friedlander--Iwaniec character
   sum*, Proposition 2.
4. **FLINT project**, signed FFT correction snapshot
   `7ad753d51c82fdec115cb179b41d0e581f1cb0ec`.
5. **python-flint project**, snapshot
   `572c8a213a88c0f92feb1bdb938ce4622f4517fa`.

---

## 19. Current scientific status

Before a successful fresh workflow run, the correct statement is:

> The analytic architecture and exact post-processing have been independently
> audited, but the full set of fresh raw numerical enclosures has not yet been
> independently reproduced in this environment.

After a successful run reaching `CHALLENGE_COMPLETE`, replace that statement by:

> The numerical part of the PrimeGaps186 certificate has been independently
> reproduced from pinned sources. A fresh receipt was checked against all fixed
> physical-integral inequalities, and the final strict margin was recomputed in
> exact rational arithmetic.

The two finite-field estimates remain external published dependencies of the
Lean development.

---

## License and attribution

This repository is a verification wrapper. Upstream source code retains its own
licenses and attribution. The OpenAI PrimeGaps186 project and the FLINT/
python-flint projects remain separate upstream works.
