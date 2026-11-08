# Worked examples from the author's own papers

Each example takes real text from `own/auditing_fact_deletion.txt` (ICLR) or `own/rv26.txt` (RV), names what to fix, and gives a revised version. Use them to calibrate what "fixed" means in this author's voice: the revision changes as little as needed, keeps every number and claim, and does not get longer.

Placeholders like `[NUMBER NEEDED: ...]` mark information the source text does not contain. Never fill them with a guess.

---

## 1. Replacing *so* and *but* with connectives

**Before (ICLR, Section 3.1):**
> Disabling more units might make the target harder to recite, but it might also affect other facts, so we measure both effects.

**After:**
> Disabling more units may make the target harder to recite while also affecting other facts. We therefore measure both effects.

**Before (ICLR, Section 3.1):**
> A deletion is only meaningful for a fact that the system recites to begin with, so we audit facts with recFULL(f) = 1.

**After:**
> Since a deletion is only meaningful for a fact that the system recites to begin with, we audit facts with recFULL(f) = 1.

**Before (ICLR, Section 4.2):**
> On T-REx, Co-LMLM recites 8.3% of facts under DEL-ON (PDR), but only 1.5% are recited because of surviving memory (SMS).

**After:**
> On T-REx, Co-LMLM recites 8.3% of facts under DEL-ON (PDR), whereas only 1.5% are recited because of surviving memory (SMS).

**Before (ICLR, Section 3.1, a definition):**
> If it recites f under DEL-ON but not under DEL-OFF, the fact is separable, but it is retained through units outside R(f), which means the deletion set is incomplete.

**After:**
> If it recites f under DEL-ON and not under DEL-OFF, the fact is separable and retained through units outside R(f). The deletion set is therefore incomplete.

What changed: each *so* became a cause-first sentence or *therefore*; each *but* became *whereas*, *while*, or *and not*, chosen by the actual relation. No sentence got longer than needed, and no connective was added where the relation was already clear.

---

## 2. Re-explaining a definition instead of referring to it

**Before (ICLR, Section 4.2):**
> Our first experiment asks why a fact is still recited after deletion. For each system, we apply its standard deletion rule and compare DEL-ON with DEL-OFF. If a fact is recited only under DEL-ON, it depends on memory that survived (SMS). If it is also recited under DEL-OFF, the backbone recites it without that memory. Table 1 reports these outcomes.

The third and fourth sentences restate the audit outcomes already defined in Section 3.1 (Equation 3).

**After (LaTeX source):**
```latex
Our first experiment asks why a fact is still recited after deletion. For each
system, we apply its standard deletion rule (\Cref{sec:applying}) and compare
DEL-ON with DEL-OFF using the outcomes defined in \Cref{eq:outcomes}.
\Cref{tab:main} reports these outcomes.
```

What changed: two sentences replaced by one reference. The reader who needs the definition knows exactly where it is. Label names are illustrative; use the labels that exist in the source.

---

## 3. A results subsection that skips the loop

**Before (ICLR, Section 4.4, complete):**
> We now hold the geometric rule (Rgeo) fixed and vary its breadth. This asks whether disabling more memory units makes the target fact less likely to be recited, and whether doing so also affects nearby facts. For Co-LMLM, lowering the cosine threshold ρ broadens geometric deletion. For NULLs, increasing k adds more neighboring sources to the deletion set. Since ρ and k control different operations, we examine the trend within each system rather than compare their values directly.
>
> Although ρ and k are not comparable, the two systems respond to breadth in opposite ways. In Co-LMLM, broader deletion removes more targets at little cost to nearby facts, whereas in NULLs it costs nearby facts without removing more targets. This reflects where the audited facts mainly reside, in separable memory for Co-LMLM and in the shared backbone for NULLs.

The motivation and setup are good. However, Figure 2 is never referenced, and the claim "removes more targets at little cost" has no numbers. The reader cannot check the conclusion.

**After:**
> We now hold the geometric rule (Rgeo) fixed and vary its breadth. This tests whether disabling more memory units makes the target fact less likely to be recited, and whether it also affects nearby facts. For Co-LMLM, lowering the cosine threshold ρ broadens deletion; for NULLs, increasing k adds more neighboring sources to the deletion set. Since ρ and k control different operations, we compare trends within each system and not their values across systems. Figure 2 reports target removal E and collateral damage X (Equation 5) as breadth increases.
>
> The two systems respond to breadth in opposite ways. In Co-LMLM, lowering ρ from 0.95 to 0.70 raises target removal from [NUMBER NEEDED: E at ρ = 0.95] to [NUMBER NEEDED: E at ρ = 0.70] on T-REx, while collateral damage stays below [NUMBER NEEDED: max X]. In NULLs, increasing k from 1 to 16 leaves target removal near [NUMBER NEEDED: E] and raises collateral damage to up to 13%. Broader deletion therefore helps only where the audited facts reside in separable memory, as in Co-LMLM, and harms nearby facts where they reside in the shared backbone, as in NULLs.

What changed: the figure is referenced and the metrics are named with a pointer to their definition; the claim now carries numbers (13% comes from the abstract and conclusion; the rest must be read from the figure data or the results files in the code repository, and are marked until then); the interpretation sentence opens with the evidence and uses *therefore*.

---

## 4. Terminology drift: decide what is drift and what is a hierarchy

The ICLR paper refers to T-REx, PopQA, Google-RE, CounterFact, and ZsRE as **datasets** (3 times), **prompt sets** (7), and **benchmarks** (5). It refers to the facts being evaluated as the **audited cohort** (6), **cohort** (10), and **evaluation set** (3).

Judgment:

- *Dataset* vs *prompt set* can be a defined hierarchy: the dataset is the source, and the prompt set is what Appendix B constructs from it. Keep both only if the paper says so once ("From each dataset, we construct a prompt set (Appendix B).") and then uses each term only in its own sense. Otherwise pick one.
- *Benchmark* is drift. Replace it with whichever of the two terms above the sentence means ("on five factual-recall datasets").
- *Evaluation set* is defined in Section 4.1 as all facts that pass the pre-deletion check, and the *audited cohort* is the subset also recited under FULL. These are different sets, so both terms can stay. However, Section 4.5 says "especially on the smallest evaluation sets" where the context is cohort sizes. Check what is meant and use the matching term. *Cohort* alone is a shortening of *audited cohort*; it is acceptable once the full term is established, but do not alternate within a paragraph.

**Before (ICLR, Section 4.5):**
> NULLs is more sensitive to the choice of DEL-OFF, especially on the smallest evaluation sets, so we treat its exact rates of surviving-memory support and interference more cautiously.

**After:**
> NULLs is more sensitive to the choice of DEL-OFF, especially on the smallest audited cohorts. We therefore treat its exact rates of surviving-memory support and interference with more caution.

---

## 5. A results paragraph that already follows the loop (keep this shape)

**RV, Section 4.1, unchanged:**
> Table 1 presents results for the Tollgate specification as an example. The compositional estimates closely track the values reported by the monolithic baseline, demonstrating the accuracy of our compositional framework. We observe similar agreement for nearly all remaining scenario–specification pairs, as reported in Table 2 of Appendix B. One notable exception is the Sustained specification for the S → shuffle (C, X, O) scenario, for which ∆ reaches +0.1162. This gap arises from MDP initial-state correlation discussed in Section 3.1: [...]

Why it works: table first, then the observation, then where the rest of the evidence lives, then the exception with its number, then the mechanism with a pointer back to the assumption in Method. Use it as the template for the loop in SKILL.md. (In a LaTeX source, "Section 3.1" and "Table 2" would be `\Cref{...}` references.)

---

## 6. Method sentences that carry their own reason (keep this shape)

**ICLR, Section 3.2, unchanged:**
> We choose ρ = 0.85 as a middle ground within the range we later sweep.

> This may exclude facts the backbone has fully memorized, which would make deletion look more effective than it is. Our estimates of backbone recitation for NULLs are therefore conservative.

> Co-LMLM and NULLs differ in model size, training data, objective, and memory implementation. We therefore treat them as two applications of the same audit rather than as a controlled comparison between architectures.

Why they work: each choice or limitation is stated together with its consequence for how Results should be read, so Results never has to stop and explain it.
