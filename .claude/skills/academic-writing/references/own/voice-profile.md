# Author voice profile

Derived from two papers the author is satisfied with:

- **ICLR 2027 submission**, "Auditing Fact Deletion in Language Models with Separable Memory" (`auditing_fact_deletion.txt`). Primary reference: most recent, closest to the target voice.
- **RV 2026**, "Scenario-Based Compositional Statistical Model Checking for Safety Specifications" (`rv26.txt`). Secondary: LNCS format, slightly more conventional framing.

All quotes below are verbatim.

## 1. Framing: a question, not a pitch

The paper is built around one question, stated plainly early on, and every section answers part of it.

- "The central question is whether disabling the units associated with a requested fact is enough to remove that fact from the system."
- Results subsections are titled as questions: "What supports an answer after deletion?", "Does the deletion rule matter?", "What happens when deletion is made broader?"
- Each experiment opens by restating its question: "Our first experiment asks why a fact is still recited after deletion." / "We next ask whether the outcome changes when the same fact is mapped to different deletion sets."

## 2. Abstract

Moves, in order: setting and the assumption people make, what is wrong with the standard evaluation, what we propose, where we apply it, findings with numbers, what the reader should do with it.

- States the naive view fairly before challenging it: "Unlearning then becomes relatively straightforward: simply delete the memory units associated with the targeted knowledge."
- Claim then proposal in one sentence: "We show that a naive comparison of model outputs is an unreliable measure of unlearnability, and propose a methodological audit..."
- Numbers are specific and bounded: "up to 81.1%", "37.9–83.0%", "up to 21.2%".
- Gives credit where a result is expected: "This is expected for NULLs by design, but less so for Co-LMLM, which aims to keep facts out of its weights."
- Ends with use, not hype: "We propose the audit as a protocol that future work on separable memory can use to support deletion claims."

## 3. Introduction

- **First sentence is concrete and plain.** "There are two common reasons to delete a fact from a language model." (Preferred over the RV opener "AI systems are increasingly deployed in safety-critical domains...", which is the generic version.)
- **Problem in two or three sentences, each with a citation.** "A model may stop producing a fact even though information about it remains internally encoded (Lynch et al., 2024), while removing it from the parameters may require retraining..."
- **Explains why the standard evaluation fails by naming the cases it cannot tell apart.** "It may be supported by memory units that were not removed, or the backbone may recite it without separable memory at all. The reverse can also happen..."
- **Method in one paragraph, procedural.** "For each fact, we evaluate the same prompt with the full memory available, with the deletion set disabled..., and with separable memory disabled entirely."
- **Contributions:** inline enumerations "(i) ... (ii) ... (iii)" in RV; in ICLR no list, the contribution is clear from the method paragraph plus a forward pointer: "Section 5 lists what such papers should report."
- Short. ICLR intro is about 350 words.

## 4. Related work

- Run-in bold headings per theme: "Separable memory.", "When retrieval hurts.", "Probing and attacks.", "Auditing deletion."
- Two to four sentences per theme. The last clause positions this work: "..., while we start from the fact to be deleted." / "We use both to test whether..." / "We adopt this three-condition design for Co-LMLM and NULLs... We also add..."
- Closest prior work gets one precise sentence on what it cannot do: "However, it is strictly restricted to Markovian, i.e., memoryless, specifications."

## 5. Method and definitions

- Run-in headings name the concept being defined: "Facts and recitation.", "Deletion rules and deletion sets.", "Three memory conditions.", "Separable facts.", "Audit outcomes."
- Definitions use "We say that...", "We call each m ∈ M a memory unit.", "henceforth referred to as the deletion set".
- Every formal quantity gets a plain-language gloss beside the equation ("post-deletion recitation", "surviving-memory interference") and an interpretive paragraph right after: "Post-deletion recitation (PDR) is what a standard before-and-after evaluation observes. The other quantities explain why that outcome occurred."
- Names are short and are reused exactly: FULL, DEL-ON, DEL-OFF; PDR, BBR, SMS, SMI, Φ; "audited cohort F". Core terms are held fixed (*recite* about 120×, *backbone* 62×, never *base model*).
- **Known lapses to fix, not copy:** the five datasets are called *datasets*, *prompt sets*, and *benchmarks* interchangeably, and *evaluation set* is used once where *audited cohort* is meant. See `examples.md` §4.
- States what a quantity depends on and what it does not: "Only recDEL-ON depends on the deletion rule. recDEL-OFF is a property of the backbone alone." / "Separability is a property of the system (θ, M) and the prompt xf, not of the deletion rule."
- Design choices are justified in one clause: "We choose ρ = 0.85 as a middle ground within the range we later sweep."
- Says when something is not new: "We emphasize that Equation (3) is not intended as a novel derivation; rather, it provides the empirical estimation needed..."
- "Intuitively," introduces the plain reading of a formula.

## 6. Scope and honesty

These are the most distinctive habits. Keep them.

- Says what the comparison is not: "We therefore treat them as two applications of the same audit rather than as a controlled comparison between architectures."
- Names the direction of a bias: "This may exclude facts the backbone has fully memorized, which would make deletion look more effective than it is. Our estimates of backbone recitation for NULLs are therefore conservative."
- Refuses to read small samples: "For NULLs, the Google-RE cohort (n = 35) is too small to draw conclusions."
- Explains anomalies instead of hiding them: "One notable exception is the Sustained specification for the S → shuffle (C, X, O) scenario, for which ∆ reaches +0.1162. This gap arises from..."
- Raises the reviewer's objection and answers it with an experiment: "A natural concern is whether the compositional method's advantage is genuine or merely a consequence of sample count... To control for this, we level the comparison..."
- Separates measured result from interpretation: "Together, these tests suggest that the evaluated facts are supported mainly by the shared backbone..., which is consistent with the intended design of NULLs."

## 7. Results paragraphs

Pattern: number first, then what it means, then "therefore" sentence.

- "On T-REx, Co-LMLM recites 8.3% of facts under DEL-ON (PDR), but only 1.5% are recited because of surviving memory (SMS). For NULLs, the corresponding rates are 80.7% and 8.1%. The same pattern appears on CounterFact. Therefore, most of the facts recited after deletion are answerable by the backbone alone."
- Short pivot sentences carry turns in the argument: "Deletion can also produce the opposite effect." / "This reduction comes at a cost." / "The reverse case is also important."
- "In short," summarizes a paragraph with a mechanism, not a slogan: "In short, explicitly using the answer text when constructing the deletion set identifies supporting entries that the other rules miss."
- Comparisons give both numbers: "with a mean deviation of 0.029 versus 0.039", "14.6× more traces on average (ranging from 5.2× to 32.3× more traces)".
- Ties every claim to a table, figure, or appendix: "Table 1 reports these outcomes.", "For space, Appendix G reports PopQA and ZsRE."

## 8. Conclusion and limitations

- Conclusion opens by restating the method in one sentence, then findings with numbers, then numbered recommendations, each with its reason: "First, they should define how a requested fact is mapped to memory units, since the choice of rule largely determines how much supporting memory survives. Second, ..."
- Then one concrete, hedged suggestion per system: "A learned check on retrieved entries could make what the backbone still recites visible rather than hidden."
- Limitations are a compact run-in paragraph. Each limitation states its consequence: "Recitation is measured with greedy decoding and answer matching, and backbone recitation is therefore a lower bound on what the backbone retains."
- Ethics statement scopes the claim: "They do not establish whether any system meets a legal standard for erasure."

## 9. Sentence level

- Active "we" throughout ("We introduce", "We apply", "We therefore test"). Passive only where the actor is irrelevant.
- Medium sentences (roughly 15–25 words), with a short sentence at each turn.
- Connectives that carry logic: *therefore* (very frequent), *instead*, *whereas*, *however*, *in contrast*, *since*, *thus*. Few additive connectives (*additionally*, *moreover* is rare).
- **Deliberate change from the source papers:** the ICLR paper uses *so* (20×) and *but* (24×) as connectives ("..., so we audit facts with..."; "..., but only 1.5%..."). The author now wants these replaced (see the avoid list in SKILL.md and `examples.md` §1). Do not copy them from the papers.
- Plain verbs: *recites*, *removes*, *holds*, *reports*, *gives*. Results "show", analyses "suggest", findings are "consistent with".
- Hedges are tied to evidence: *suggests*, *may*, *might*, *is consistent with*, *appear to*. Measured results are stated flatly.
- Precise numbers: one decimal for percentages, ranges with en dash (37.9–83.0%), "percentage points" for differences, n for cohort sizes, × for ratios.
- "i.e." to define in passing: "safety and co-safety specifications, i.e., specifications whose violation or satisfaction can be determined from finite executions."
- No em dashes as clause connectors. En dash only in ranges and compound names (key–value, scenario–specification).
- No bold or italics in running text except run-in headings.
- Almost no intensifiers. ICLR paper avoids *novel*, *significantly*, *crucial*. (RV still has "novel", "significantly reducing", "fundamental limitation"; treat these as habits to drop.)

## 10. What to avoid (by contrast with the author's best text)

- Generic "X is increasingly deployed" openers.
- "novel", "significantly" without a test, "fundamental", "principled" as decoration.
- Contribution lists that restate the abstract.
- Defining a term and then varying it.
- Interpreting a result in the same sentence as reporting it when the interpretation is uncertain.
- *so* and *but* as connectives (the author's new rule).
- A results subsection whose figure is never referenced or whose claim carries no numbers (ICLR §4.4; see `examples.md` §3).
- Re-explaining a Method definition in Results instead of referring to it (ICLR §4.2; see `examples.md` §2).
