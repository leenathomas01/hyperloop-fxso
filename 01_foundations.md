# 01 — Foundations: Hyperloop Transformers

**Source:** [arXiv:2604.21254](https://arxiv.org/abs/2604.21254) — Zeitoun, Torroba-Hennigen, Kim (MIT, 2026)

---

## What the paper claims

Hyperloop Transformers achieve **lower perplexity than depth-matched standard Transformers while using ~50% fewer parameters**, across model scales from 135M to 1B parameters. This holds through post-training INT4 quantization.

The architecture is motivated by edge and on-device deployment, where memory footprint — not just compute — is the primary constraint.

---

## What it actually changes (beyond the headline)

### 1. Breaks the depth = parameters assumption

Standard Transformers: more depth → more layers → more parameters. These are inseparable.

Hyperloop: the middle block is reused across passes (loops). Depth becomes **time-like iteration**, not stacked structure. A 16-layer effective depth can be achieved with far fewer unique parameters.

### 2. Three-block organization

```
[Begin Block] → [Middle Block × L loops] → [End Block]
```

- Begin and end blocks: standard, non-recurrent Transformer layers
- Middle block: same weights reused across L loop iterations (default: 3)
- Parameter split: ~25% begin, ~50% middle, ~25% end

### 3. Hyper-connections at loop level

Instead of vector-valued residual streams, Hyperloop expands to **n parallel residual streams** (matrix-valued). Crucially, hyper-connections are applied **only after each full loop**, not after every attention/MLP layer.

This means:
- Minimal additional parameters (150–300K over vanilla looped)
- Minimal compute overhead (training throughput within ~5% of baseline)
- Each loop can evolve representations differently via loop-specific modulation parameters

### 4. Loop position embeddings

A learned embedding `e_l` is added after each loop iteration, acting as input at each time step — analogous to the input signal in a depth-wise RNN.

---

## Key empirical results

| Model | Params | PPL (BF16) | PPL (INT4) | Task Acc |
|-------|--------|-----------|-----------|---------|
| Transformer (1B) | 990M | 10.19 | 10.27 | 48.0% |
| Hyperloop (1B effective) | 580M | 9.65 | 9.81 | 49.8% |

The ~50% parameter reduction holds across scales, and the gains **persist through quantization** — which is non-trivial, since looped layers see more inputs and would naively be harder to quantize.

---

## What the paper does NOT claim

- It does not claim test-time adaptive compute (loops are fixed at 3)
- It does not claim cross-session continuity or persistent state
- It does not address reasoning scaling beyond brief mentions
- It is tested only up to ~2B parameters — frontier-scale behavior unknown

---

## The architectural shift that matters most

> **Depth becomes an iteration count, not a parameter count.**

This separates two things that were previously fused: how many unique computations a model can perform (parameters) vs. how many times it applies them (depth/loops). Intelligence becomes partly a function of **process**, not just **capacity**.

This is the seed of everything that follows in the derivation chain.
