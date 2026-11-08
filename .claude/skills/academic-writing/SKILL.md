---
name: academic-writing
description: Write, structure, and revise academic and technical-research prose in English (papers, theses, reports), with most weight on Method and Results sections. Use when asked to draft or edit scholarly text, write or restructure a method or results section, describe experiments, tighten an argument, keep terminology consistent, calibrate hedging, or prepare a manuscript in NLP, ML systems, or edge-AI hardware. Does not invent citations or numbers.
---

# Academic Writing

Write precise, evidence-backed scholarly English that is easy to read. Every claim is either supported, scoped, or removed. Every sentence has a job, or it is cut. The paper keeps one line of argument from the first sentence to the last, and it keeps the same words for the same things the whole way.

## References

All paths below are relative to this skill's base directory. Load these when drafting or revising more than a paragraph:

- `references/own/voice-profile.md`: the author's own voice, derived from two papers they are satisfied with. **This is the target style.** When it conflicts with a corpus pattern, the voice profile wins.
- `references/own/*.txt`: the two papers in full, for checking how the author handles a specific move.
- `references/corpus/notes/{nlp,mlsys_a,compression,edge}.md`: writing patterns from 20 well-regarded papers in NLP, ML systems, quantization, and edge accelerators, with verbatim quotes. Use the file matching the paper's field. `edge.md` covers hardware normalization and units.
- `references/corpus/txt/`: full text of those papers, for looking up how a strong paper phrases a particular move.
- `references/examples.md`: before-and-after revisions of the author's own paragraphs. Read it before revising; it shows what "fixed" looks like in this voice.
- `scripts/check.py`: mechanical checks for a LaTeX paper (see Mechanical check).

## Hard rules

1. **Never fabricate.** No invented citations, DOIs, numbers, results, quotes, or author names. If a source is needed and not provided, insert `[CITATION NEEDED: <what the claim requires>]`. If a number is needed and not provided, insert `[NUMBER NEEDED: <what>]`. Never guess.
2. **Do not add facts.** Revise what the author gave you. Anything new must be flagged as a suggestion, not written as fact.
3. **Preserve technical content.** Terms of art, units, equations, symbols, code, labels, and citation keys stay exactly as written.
4. **One word per concept, for the whole paper.** Once a term is chosen, it is the only term for that thing (see Terminology). This applies to every noun the reader tracks: the models, the datasets, the method's components, the metrics, the conditions.
5. **Ask once, early** if venue, audience, or citation style is unknown and it changes the output. Otherwise state your assumption in one line and proceed.
6. **Never commit, push, or pull** in the paper repository unless the author asks. The paper is an Overleaf clone; a push changes the document every coauthor is editing.

## When rules conflict

Apply them in this order:

1. **Correctness and meaning.** Never change a claim, number, hedge, or scope to satisfy a style rule.
2. **The author's voice** (`references/own/voice-profile.md`, `references/examples.md`).
3. **Readability.**
4. **Style rules** (avoid list, connectives, length limits).

A revision normally makes the text shorter, not longer. If a fix would add words, prefer restructuring the sentence. Do not apply a rule mechanically where it makes the sentence worse; for example, replacing every *but* with a sentence-initial *However,* produces stiff prose, and *whereas*, *while*, or a split sentence often reads better.

## Working in a research repository

The paper is usually a LaTeX project cloned from Overleaf, inside the code repository of the research project. Use both: the paper says what was done, and the code shows what was actually done.

### Before editing anything

1. **Find the paper.** Locate the main `.tex` file (the one with `\documentclass`), follow its `\input`/`\include` tree, and find the `.bib` file and the macro definitions (`\newcommand`).
2. **Read the whole paper,** even when asked to edit one section. Method, Results, terminology, and "Say it once" cannot be checked from one section. If only part of the paper is available, say which checks could not be done.
3. **Build a paper map** (working notes; do not write it into the paper): the main claim; where each term, symbol, abbreviation, assumption, and design choice is defined (file and line); every figure and table with its label and where the text discusses it; and the macros that encode terms (for example `\ours`).
4. **Run the mechanical check** (below) and keep the output as the baseline.

### Checking the paper against the code

Read the code, configs, and result files that the paper describes. Do not edit them.

- **Method against code.** Hyperparameters, thresholds, default settings, filtering and selection rules, dataset and model names, and the order of operations stated in Method must match the code and configs. Report every mismatch with both locations (`method.tex:42` says ρ = 0.85; `configs/audit.yaml:12` sets 0.80).
- **Results against outputs.** Numbers in tables, text, and captions must match the result files, logs, or notebooks that produced them. Report mismatches; do not silently change either side.
- **Filling gaps from the repository.** A `[NUMBER NEEDED]` may be filled from a result file only when the file clearly holds that quantity. Cite the path in the report and ask the author to confirm. If the provenance is unclear, leave the placeholder.
- **Names.** The paper's terms do not have to match variable names in the code (`del_on` vs DEL-ON), though the paper must be consistent with itself.

### LaTeX rules

- **Cross-references use labels.** Write `\Cref{sec:method}` (or `Section~\ref{sec:method}` if cleveref is not loaded); never hard-code "Section 3.2", "Table 1", or "Equation 2". Use the existing label prefixes.
- **Never change** labels, `\cite` keys, macro names, `\newcommand` definitions, file names, or the `\input` structure. Do not add packages without asking.
- **Use the author's macros for terms.** If a term is defined as a macro (`\ours`, `\delon`), write the macro, not the expanded text.
- **Keep the diff small.** Edit in place, preserve the existing line-breaking convention (one sentence per line, one paragraph per line, or hard-wrapped), and do not reformat lines you did not change. Coauthors review these diffs in Overleaf.
- **Leave comments alone.** `%` comments and `\todo{}` notes belong to the authors; do not delete or rewrite them.
- **Use non-breaking spaces** before references and citations (`Table~\ref{...}`, `model~\citep{...}`) when the source already does.
- **Compile if possible.** If `latexmk` or `pdflatex` is available, compile after editing and report any new errors or warnings (undefined references, overfull boxes caused by the edit). Remove build artifacts you created.

### Mechanical check

Run `python3 <skill-dir>/scripts/check.py <paper-dir-or-main.tex>` before and after revising, where `<skill-dir>` is this skill's base directory (for example `.claude/skills/academic-writing` in a project, or `~/.claude/skills/academic-writing` for a user-level install). It reports, with file and line:

- informal words and connectives (*so*, *but*, *a lot*, *get*, contractions, sentence-initial *And*), hype words, dashes, and vague back-references ("as mentioned above")
- hard-coded cross-references, figures and tables never referenced in the text, floats without a label, and references to undefined labels
- sentences over 30 words
- terminology drift groups (dataset / benchmark / prompt set, model / network, ...) and spelling variants (fine-tuning / finetuning, Co-LMLM / CoLMLM)
- abbreviations used before their definition or defined twice
- numbers in the abstract, introduction, or conclusion that appear nowhere else in the paper

Every hit is a candidate. Fix it, or keep it with a reason (for example, *just* in "just outside the boundary", or a long sentence that is an enumeration). Machines cannot judge meaning; you still read every changed sentence.

## Workflow

1. **Frame.** Identify document type, venue/audience, citation style (IEEE, APA, Vancouver, ACM, author-year), and the single main claim or question. In a repository, do the steps in "Before editing anything" first.
2. **Outline.** Use the structure for the document type (below). Write the outline first for anything longer than a paragraph. For Results, outline the chain of experiments and what each one varies relative to the previous one.
3. **Draft.** One paragraph = one point. Open with the point, support it, close by linking to the next idea. Choose each term at first use and keep it.
4. **Revise** in passes, not all at once:
   - Argument: is every claim supported or scoped?
   - Readability: run the cut test; split long sentences; remove stray details (see Readability).
   - Method ↔ Results: does Method define everything Results uses, and does Results use everything Method sets up?
   - Structure: does each paragraph earn its place and order?
   - Sentences: concision, clarity, active voice where the actor matters.
   - Repetition: is anything explained twice? Replace the second explanation with a reference (see Say it once).
   - Terminology: for an existing paper, run the terminology check below.
5. **Verify.** Run the mechanical check again and resolve or justify every remaining hit. Re-read each changed sentence against the original and confirm that no claim, number, hedge, or scope changed. Go through the checklist at the end.
6. **Report** to the author, briefly:
   - what changed, by section (not a full diff)
   - **possible meaning changes**: every sentence where a claim, hedge, or scope may have shifted, with before and after, so the author can confirm
   - terminology variants found and what was unified
   - paper-versus-code mismatches, with both locations
   - open items: `[CITATION NEEDED]`, `[NUMBER NEEDED]`, and checks that could not be run

## Structure by document type

- **Research paper (IMRaD):** Abstract; Introduction (context, gap, contribution, outline); Related Work; Method; Results (setup, experiments); Discussion (interpretation, limitations, implications), often merged into Results; Conclusion; References.
- **Abstract:** problem, approach, key result with a number if one exists, implication. 150-250 words unless the venue says otherwise. No citations, no undefined abbreviations.
- **Introduction:** funnel from broad context to the specific gap, then state contributions explicitly (a short list is fine).
- **Related work:** organize by theme, not by paper. End each theme by stating how this work differs.
- **Method:** see the Method section below.
- **Results:** see the Results section below.
- **Technical report / thesis chapter:** put the question and conclusion up front; keep methods reproducible.

## Method

The Method section gives the reader everything they need to know before the experiments, and nothing more. Test: a reader who has read only Method can follow every experiment in Results without meeting a new concept, rule, or choice there.

### What it must contain

- **Every object the experiments use**, defined: the system or setting, the inputs, the conditions compared, and the metrics, with formal definitions where the paper uses them.
- **Every choice the results depend on**: default settings, selection or filtering criteria, which variant is "standard", hyperparameters fixed in advance. Give each choice its reason in the same sentence ("We choose ρ = 0.85 as a middle ground within the range we later sweep.").
- **Every assumption**, stated as an assumption, with when it can fail ("We assume that the controller... is Markovian"; "KDE performs well in moderate dimensions, whereas it might suffer from the curse of dimensionality").
- **The consequences of those choices for interpretation**, said here rather than discovered in Results ("This may exclude facts the backbone has fully memorized... Our estimates of backbone recitation for NULLs are therefore conservative.").
- **What the comparison is not**, if a reader could over-read it ("We therefore treat them as two applications of the same audit rather than as a controlled comparison between architectures.").

Experimental logistics (datasets, decoding, hardware, answer matching) go in the Results setup unless a method definition depends on them.

### How to order it

1. **General before specific.** Define the framework independent of any one system, then show how it instantiates for each system or setting (a subsection such as "Applying X to A and B"). The reader learns the idea once and sees it applied.
2. **Dependency order.** Each concept is defined before anything that uses it. Use run-in headings that name the concept being defined ("Facts and recitation.", "Deletion rules and deletion sets.", "Three memory conditions."), one concept per paragraph.
3. **Intuition next to formalism.** Before or after a formula, give the plain reading ("Intuitively, traces generated from primitive scenarios are weighted according to their likelihood under the target composite scenario."). A motivating example or an overview figure can carry this for the whole section.

### How to write each definition

- Introduce terms with "We say that...", "We call each m a memory unit.", "henceforth referred to as the deletion set". Then use exactly that term.
- After each formal quantity, say what it means and what it depends on and does not depend on ("Only recDEL-ON depends on the deletion rule. recDEL-OFF is a property of the backbone alone.").
- Give each metric a short name and a gloss, and say which observation it explains ("PDR is what a standard before-and-after evaluation observes. The other quantities explain why that outcome occurred.").
- Say plainly when something is not new ("Equation (3) is not intended as a novel derivation").
- For design choices, name the alternative and why it was rejected, in one or two sentences. For hardware and systems designs, state the cost of the choice in the design section, not later (see `references/corpus/notes/edge.md`, `mlsys_a.md`).
- Move full formal definitions, proofs, and per-variant details to the appendix and point to them ("Appendix D.1 gives the formal definitions."). The main text keeps what is needed to follow Results.
- Tests that only apply to one system are announced in Method with what each one asks, so Results can refer to them by name.

## Results

### Experimental setup

Open Results with a setup subsection in run-in paragraphs (for example: Datasets. Metrics or Answer matching. Selection of examples. Baselines or Reference models. Hardware and decoding.). Each paragraph says what and **why** ("To put backbone recitation in context, we also evaluate conventional language models without separable memory."). Give the numbers a reader needs to judge the evidence: dataset and cohort sizes, seeds or run counts, hardware, versions, budgets. For hardware results, state the technology node, clock, batch size, and normalization basis once, and flag any change (see `references/corpus/notes/edge.md`). Exact checkpoints and remaining settings go to an appendix with a pointer.

### The experiment loop

Every experiment follows the same loop, and the loop is what gives Results its flow:

1. **Motivate.** Say why this experiment comes now. The motivation can be a question ("Our first experiment asks why a fact is still recited after deletion."), the variable the previous experiment held fixed ("The previous experiment uses one standard deletion rule for each system. We next ask whether..."), a concern a reader would raise ("A natural concern is whether the advantage is genuine or merely a consequence of sample count."), or a claim from Method to verify. It does not have to be phrased as a question.
2. **Say what is done**, briefly, in terms already defined in Method ("For each system, we apply its standard deletion rule and compare DEL-ON with DEL-OFF.").
3. **Point to the figure or table** ("Table 1 reports these outcomes."). Every figure and table in the paper is referenced in the text and analyzed there. A figure that is never discussed is a defect.
4. **Report the numbers first.** Give both sides of a comparison, with units and the condition ("8.3% of facts under DEL-ON (PDR), but only 1.5%... (SMS)"; "a mean deviation of 0.029 versus 0.039"; "14.6× more traces on average (ranging from 5.2× to 32.3×)").
5. **Interpret.** One sentence that says what the numbers mean, usually opening with "Therefore" or "In short" and naming a mechanism, not a slogan.
6. **Handle the turn.** The cost, the opposite effect, or the exception, each in its own short opening sentence ("Deletion can also produce the opposite effect."; "This reduction comes at a cost."). Explain exceptions with a mechanism, and point back to Method when an assumption made there is what causes it ("This gap arises from MDP initial-state correlation discussed in Section 3.1"). Decline to interpret samples that are too small ("(n = 35) is too small to draw conclusions").
7. **Close and send the rest away.** Summarize secondary datasets or settings in one sentence with an appendix pointer ("For space, Appendix G reports PopQA and ZsRE. ...").

### Ordering experiments

- Order experiments so each one relaxes one thing the previous one held fixed: the standard setting first, then vary the rule, then vary its strength or breadth, then the implementation choices the results depend on (robustness), then tests specific to one system.
- The transition sentence names what was fixed and what now varies ("We now hold the geometric rule fixed and vary its breadth."). Avoid bare "Next, we..." transitions that give no reason.
- When a reader could attribute the result to a confound, add the controlled experiment and report it even if the result is a tie ("With the sample-count advantage removed, the two approaches are essentially tied"). A tie that isolates the cause is evidence.
- Losses, exceptions, and regimes where the method does not help are reported in the same flat tone as the wins.

### Claims in Results

- Measured results are stated flatly. Interpretations are hedged with *suggests* or *is consistent with*. Mechanism guesses are labeled (*we hypothesize*, *we suspect*). Do not hedge a measurement.
- Name baselines as systems ("Orca", "the monolithic SMC baseline"), never "existing methods".
- Label percentage-point differences as such. Keep every number identical across abstract, text, tables, and captions.
- Captions say what the figure shows and define every symbol in it. A caption may state the takeaway.

## Terminology

The paper keeps one thread, and the words carry it. Once the author says "five models", it stays "models"; it never becomes "networks", "systems", or "LMs" later.

- **One term per concept.** This holds for every concept the reader tracks: the method and its parts, the models, the datasets, the conditions, the metrics, the sets being evaluated.
- **Pick the term at first use and define it there.** If two terms are both reasonable, choose one and do not alternate.
- **Hierarchies are allowed when defined.** A general term with named subtypes is not drift: "memory unit" for the general concept, and "entry" (Co-LMLM) and "source" (NULLs) as defined instances of it. Drift is two words for the same thing, not a word for a defined subtype.
- **Typical drift to catch:** dataset / benchmark / prompt set / task; model / network / system / LM; cohort / evaluation set / subset; baseline / reference / comparison; accuracy / correctness / performance; method / approach / framework / technique when they all mean the paper's own contribution.
- **Abbreviations and symbols** are defined once and then never re-expanded or swapped. The name of the method is spelled and capitalized the same way everywhere.

**Terminology check (when revising an existing paper):** build a glossary from the text: each concept the reader tracks, every surface form used for it, and its count. For each concept with more than one form, decide whether the variation makes sense. Keep it when the forms are defined subtypes or genuinely different things. Otherwise, pick the one to keep (usually the most frequent or the one defined first) and replace the others. Include the variants found and the changes made in the final report.

## Say it once

Each piece of information is stated once, at the place where the reader first needs it. Later sections refer back to it instead of repeating it.

- **Refer, do not re-explain.** When Results uses a definition, rule, assumption, or setting from Method, name it and point to where it is defined. Do not restate the definition.
- **Make the reference natural and specific.** Point to a section, equation, figure, table, or appendix. Phrase it so it reads as part of the sentence:
  - "As described in Section 3.2, the standard deletion rule..."
  - "As defined in Equation 2, ..."
  - "This gap arises from the MDP initial-state correlation discussed in Section 3.1."
  - "the pre-deletion check (Section 3.2)"
  - "Under the same fixed-trace budget as in Section 4.1, ..."
  - "As shown in Table 1, ..."
  - "Recall that DEL-OFF disables the separable memory entirely." (sparingly, for a one-clause reminder the reader needs right there)
- **Never point vaguely.** "As mentioned before", "as stated above", and "as discussed earlier" do not tell the reader where to look. Name the location.
- **A short reminder is allowed** when the reader needs it to follow the sentence: one clause plus the reference, not the full explanation again.
- **Exceptions.** The abstract, introduction, and conclusion restate the main claim and findings by design. Captions repeat what is needed to read the figure on its own. Even there, restate the result, not the derivation.

## Readability

The reader is a researcher from a neighboring field reading the paper once, in order. Each paragraph must make sense to that reader on the first read. Short and simple is the default; length needs a reason.

- **Every sentence has one job.** It defines, motivates, reports, interprets, or links. If a sentence does none of these, cut it. If it tries to do two, split it.
- **No stray details.** Every fact, number, or design detail must connect to the argument where it appears. If the reader cannot tell why it is there, say why in a clause, move it to the appendix, or cut it.
- **One new idea per sentence.** Most sentences fall between 15 and 25 words. Split anything that runs past about 30 words or holds two new ideas.
- **Known before new.** Start a sentence with what the reader already has (a defined term, the previous result) and end with the new information. This also makes paragraphs flow without extra connectives.
- **Subject and verb early and close together.** Do not make the reader hold a long clause before they learn what the sentence is about.
- **Verbs, not nominalizations.** "We evaluate" over "we perform an evaluation of"; "to" over "in order to"; "because" over "due to the fact that".
- **Plain words.** *Use* over *utilize*, *show* over *demonstrate* when nothing is being proven, *about* over *approximately* in prose. Technical terms stay; decorative ones go.
- **Introduce only what is used again.** Do not define a symbol, abbreviation, or term that appears once. Do not mention a variant, dataset, or setting that the paper never comes back to.
- **Topic sentences carry the argument.** A reader who reads only the first sentence of each paragraph should get the paper's line of reasoning.
- **Cut test.** For each sentence, ask whether the paragraph loses anything without it. For each paragraph, ask whether the section does. If not, delete it.

## Style

- **Precision over ornament.** Prefer the concrete verb and the specific number. "Reduces sleep current by 38%" beats "significantly improves power efficiency".
- **Hedging is calibrated, not reflexive.** Use *may/suggests* only where the evidence is genuinely uncertain. State measured results plainly. Do not hedge the same claim twice.
- **Tense.** Present for established facts, for what the system does, and for the paper's own structure ("Section 3 describes..."). Past for what was done and observed ("We measured..."). Be consistent within a section.
- **Voice.** First person plural ("we") is acceptable where the venue allows. Use passive only when the actor is irrelevant.
- **Sentence length.** Vary it. Break any sentence that carries more than one new idea. Use a short sentence for each turn in the argument.
- **Claims of novelty and importance.** Show, do not announce. Delete "novel", "state-of-the-art", "significant" unless quantified or supported. Scope any "first" claim ("to our knowledge").
- **Avoid:** filler openers ("It is worth noting that"), vague quantifiers ("a lot", "various"), unsupported superlatives, and hype words ("revolutionary", "democratizes", "breakthrough").

## Register and connectives

The text is formal academic English, and the logic between sentences is made explicit with connectives.

### Words to avoid

Replace these whenever they appear in the author's prose. Leave them alone inside quotations, titles, code, and the names of things.

| Avoid | Use instead |
|---|---|
| *so* linking clauses ("..., so we audit...") | *therefore*, *thus*, *hence*, *which means that*, *as a result*; or restructure ("Because..., we audit...") |
| *but* ("..., but only 1.5%...") | *however*, *whereas*, *while*, *although*, *in contrast*, *nevertheless*; in definitions, "X and not Y" or "X; Y does not hold" |
| sentence-initial *And*, *Also*, *Plus* | *In addition*, *Furthermore*, or merge into the previous sentence |
| *a lot of*, *lots of*, *tons of* | *many*, *much*, *a large number of*, or the number |
| *big*, *huge* | *large*, *substantial*, or the number |
| *get*, *got*, *gets* | *obtain*, *achieve*, *become*, *receive*, or a specific verb |
| *really*, *pretty*, *quite*, *basically*, *actually*, *just* (as filler) | delete, or give the number |
| *like* (for examples) | *such as* |
| *thing(s)*, *stuff*, *kind of*, *sort of* | the specific noun, or delete |
| *okay*, *anyway*, *of course* | delete |
| contractions (*don't*, *it's*, *can't*) | full forms |
| *less so*, *even more so* | state the comparison explicitly |

*So that* expressing purpose ("so that PDR, BBR, SMS, and SMI denote rates") is acceptable. *Such that* is the more formal alternative in definitions.

### Connectives

Use a connective wherever the logical relation between two sentences or clauses is not already obvious from their content. Choose it by the relation it expresses:

| Relation | Connectives |
|---|---|
| Consequence | *therefore*, *thus*, *hence*, *as a result*, *consequently*, *it follows that* |
| Cause | *because*, *since*, *as*, *due to*, *owing to* |
| Contrast | *however*, *whereas*, *while*, *in contrast*, *conversely*, *instead* |
| Concession | *although*, *even though*, *nevertheless*, *despite* |
| Addition | *also*, *in addition*, *furthermore*, *moreover* |
| Sequence | *first*, *second*, *then*, *next*, *finally* |
| Example | *for example*, *for instance*, *such as*, *e.g.* |
| Restatement or summary | *that is*, *i.e.*, *in other words*, *in short*, *together* |
| Comparison | *similarly*, *likewise*, *in the same way*, *correspondingly* |
| Condition | *if*, *unless*, *provided that*, *when* |

Rules for using them:

- **The connective must match the logic.** *Therefore* only follows a reason; *however* only marks a real contrast. Check each one against the two sentences it joins.
- **Do not start every sentence with one.** A connective earns its place when it tells the reader something the content does not. Two sentences in sequence often need none.
- **Do not stack them** ("However, therefore, ...") or repeat the same one in consecutive sentences. Vary within a paragraph, and keep the most precise one.
- **Prefer the lighter forms for addition.** *Also* and *in addition* over *moreover* and *furthermore*, which become heavy when repeated. Avoid *additionally*, which reads as machine-generated.
- **Place them where they read naturally.** Sentence-initial with a comma ("Therefore, most of the facts...") or after the subject ("Externalizing factual text therefore reduces..."). The second form is often smoother in a run of results.
- **Paragraph transitions** link back to the previous paragraph's point, not only to its last sentence ("The previous experiment uses one standard deletion rule for each system. We next ask whether...").

## Citations

- Cite for: specific claims, methods borrowed, data used, and prior results compared against. Not for common knowledge.
- Match the requested style exactly and keep it uniform.
- Citation sits at the claim it supports, not at paragraph end by default.
- Report any claim you believe needs a source but lacks one. Do not fill the gap yourself.

## Final checklist

- [ ] Main claim or question is stated early and every section serves it
- [ ] Every sentence has one job; no stray details; nothing a reader cannot place on first read
- [ ] Topic sentences alone give the line of argument
- [ ] Method defines every concept, choice, and assumption that Results uses; Results introduces nothing new
- [ ] Results opens with a setup that says what and why
- [ ] Every experiment is motivated, points to its figure or table, reports numbers, and interprets them
- [ ] Every transition says why the next experiment follows
- [ ] Every figure and table is referenced and analyzed in the text
- [ ] Exceptions and losses are reported and explained; small samples are not over-read
- [ ] Nothing is explained twice; later mentions refer back to a named section, equation, figure, or table
- [ ] One term per concept; for an existing paper, terminology check run and variants fixed where it makes sense
- [ ] No informal words from the avoid list (*so*, *but*, *a lot*, *get*, contractions...)
- [ ] Logical relations between sentences are marked with a fitting connective; no stacked or repeated connectives
- [ ] Numbers carry units and agree across abstract, text, tables, and captions
- [ ] Every non-obvious claim is cited, measured, or scoped; gaps marked `[CITATION NEEDED]` or `[NUMBER NEEDED]`
- [ ] Limitations are stated, each with its consequence
- [ ] Tense and voice consistent per section
- [ ] Mechanical check run after the last edit; every remaining hit fixed or justified
- [ ] Method and Results checked against the code, configs, and result files; mismatches reported
- [ ] Cross-references use labels; no labels, cite keys, macros, or comments changed; diff limited to edited lines
- [ ] Nothing committed or pushed

After the draft, if the text reads as machine-generated (stock phrases, uniform rhythm), run the `humanizer` skill in academic mode.
