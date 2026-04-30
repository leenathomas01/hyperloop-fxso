# 05 — Open Questions

These are the things that remain genuinely unresolved. Not gaps to be embarrassed about — the interesting territory for anyone who wants to pick this up.

---

## Architectural questions

**Q1: Do Hyperloop's internal loops actually produce coherent trajectory manifolds?**

The framework assumes that repeated loop passes create meaningfully evolving internal states rather than noisy oscillations around a fixed point. This is theoretically plausible but empirically unverified. The paper's representation similarity analysis (Figure 3) suggests loops do produce differentiated states, but whether these constitute coherent trajectories in the relevant sense is unknown.

**Q2: Does compatibility bandwidth actually correlate with generalization?**

The claim is that patterns surviving more diverse contexts are more likely to be genuinely useful. This is intuitively compelling but needs formal grounding. What is the information-theoretic relationship between context survival and semantic utility?

**Q3: How do fixed-depth loops interact with the diffusion regime model?**

The paper uses 3 fixed loops. The relay ↔ diffusion model assumes you can tune overlap density and coupling strength. With fixed loop counts, what actually controls regime selection? Is regime control even possible without adaptive loop depth?

---

## Framework questions

**Q4: Is the novelty-vs-noise discrimination problem actually solved?**

The two-speed enforcement model (exploration + exploitation zones) provides a lifecycle for novelty. But detecting "a pattern becoming more coherent" vs "noise temporarily spiking coherence" may require signals that the framework doesn't fully specify. Compatibility bandwidth helps, but the detection problem is not closed.

**Q5: What is the minimum viable constraint system?**

The framework describes rich constraint geometry, anisotropic dissipation, multi-scale consistency checks, cross-pruning, etc. In practice, how many of these are necessary vs sufficient? Is there a minimal version that preserves the key properties?

**Q6: Does co-evolution require many agents, or can it emerge in small systems?**

The ecosystem layer assumes enough agents and patterns that mutual optionality effects become significant. What are the minimum conditions for co-evolutionary dynamics to appear?

---

## Scale questions

**Q7: Does the 50% parameter efficiency hold at frontier scale?**

The Hyperloop paper tests up to ~2B parameters. The authors explicitly flag this as a limitation. Everything in this framework built on top of Hyperloop inherits this uncertainty.

**Q8: Would self-refining constraints destabilize at scale?**

The self-refinement layer requires slow, local, consensus-driven updates. At large scale with many interacting agents and patterns, do these conditions remain achievable? Or does the system become too complex for local repair?

---

## Fundamental questions

**Q9: Is this a theory of how intelligence works, or how we'd want it to work?**

Left deliberately open. A theory of how intelligence works makes falsifiable predictions about observed systems (biological or artificial). A design philosophy describes principles for building systems. This exploration may be the latter dressed as the former. Both are valuable. Only one is science.

**Q10: Can constraint updates be constrained to prevent drift?**

The self-refinement layer adapts constraints based on failure signals. But what prevents the meta-constraint update process from drifting in ways that corrupt the underlying physics? Is there a stable fixed point, or does the system require external anchoring?

---

## What would actually help

- **Formal dynamical systems analysis** of the attractor geometry claims
- **Empirical probing** of Hyperloop's internal representations across loop iterations
- **Toy model implementation** of the relay ↔ diffusion regime transition
- **Information-theoretic grounding** of compatibility bandwidth
- **Biological analogues** — do any of these mechanisms appear in neural systems?
