# Style notes: quantization / compression papers

Corpus: LLM.int8() (Dettmers et al., NeurIPS 2022), GPTQ (Frantar et al., ICLR 2023), AWQ (Lin et al., MLSys 2024, Best Paper), Deep Compression (Han et al., ICLR 2016). These notes cover how the papers write, not what they found. Every quoted string appears in `.claude/skills/academic-writing/references/corpus/txt/` (whitespace and line-break hyphenation normalized).

---

## 1. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale

**Title.** Method name, then a plain description of the operation, then the regime ("at Scale"). No adjectives.

**Abstract (~230 words). Moves in order:**
1. Problem in one clause: "Large language models have been widely adopted but require significant GPU memory for inference."
2. What was built, with the headline result right away: "cut the memory needed for inference by half while retaining full precision performance."
3. A concrete use case: "a 175B parameter 16/32-bit checkpoint can be loaded, converted to Int8, and used immediately".
4. The mechanism behind it: "This is made possible by understanding and working around properties of highly systematic emergent features".
5. A two-part method, given in sequence: "We first use vector-wise quantization"; "However, for the emergent outliers, we also include a new mixed-precision decomposition scheme".
6. One number: "more than 99.9% of values are multiplied in 8-bit."
7. Implication framed as access: "making it possible to use OPT-175B/BLOOM on a single server with consumer GPUs."
8. Artifact: "We open source our software."

**Introduction.**
- The first sentence names the field, cites four papers, and states the cost: "Large pretrained language models are widely adopted in NLP ... but require significant memory for inference."
- The gap comes in three stacked limitations of prior work: "While these methods reduce memory use, they degrade performance, usually require tuning quantization further after training, and have only been studied for models with less than 350M parameters." Then a one-line open problem: "multi-billion parameter quantization remains an open challenge."
- Contribution as a "first": "we present the first multi-billion-scale Int8 quantization procedure for transformers that does not incur any performance degradation."
- Difficulty framed as "two key challenges", then each answered in turn.
- The observation drives the method, and the intro already carries dense numbers: "These outliers are highly systematic: at the 6.7B scale, 150,000 outliers occur per sequence, but they are concentrated in only 6 feature dimensions". It includes a control: "In contrast, removing the same amount of random features decreases the probability by a maximum of 0.3%".
- The secondary result is scoped modestly: "provide modest matrix multiplication speedups".
- No bulleted contribution list and no roadmap sentence.

**Claims and evidence.** Results prose reads trends off the table: "We see that absmax, row-wise, and zeropoint quantization fail as we scale". Exclusivity is claimed plainly: "LLM.int8(), is the only method that preserves perplexity." Negative results are reported next to the positive ones: "The quantization overhead can slow inference for models with less than 6.7B parameters". Analysis findings are numbered: "Our main quantitative results can be summarized as four main points." Thresholds come with reasons: "Our reasoning for these thresholds is as follows." Robustness checks are spelled out: "To make sure that the observed phenomena are not due to bugs in software, we evaluate transformers that were trained in three different software frameworks."

**Hedging.** Facts about the method are stated flatly. Interpretation is hedged with "suggests", "indicates", and "We hypothesize", as in "We hypothesize that model size is only one important covariate among many". A speculative aside is marked as such: "We hypothesize that besides Int8 inference, regular 16-bit floating point training becomes unstable".

**Related work** comes near the end, under bold run-in headings ("8-bit Data Types.", "Outlier Features in Language Models.", "Multi-billion Scale Transformer Quantization."). Concurrent work is named with exact numbers: "The largest models that nuQmm and ZeroQuant evaluate are 2.7B and 20B parameter transformers". Positioning is generous: "These methods are complementary with LLM.int8()." and "Jin et al. (2022) provide an excellent analysis".

**Limitations** are enumerated by ordinal: "The main limitation of our work is", "Another limitation", "A third limitation", "A final limitation". Each one gives a reason and a future-work pointer. Broader impact names a downside of the authors' own work: "which might increase the disparities between resource-rich and poor organizations."

**Things not to copy:** "incredibly sparse", "Luckily,", and a few typos and dropped words ("In this work, push quantization techniques").

---

## 2. GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers

**Title.** Acronym, then two qualifiers (Accurate, Post-Training), then the target model class. A footnote explains the name: "This merges the name of the OPT model family with the abbreviation for post-training quantization (PTQ)."

**Abstract (~240 words).** The moves follow the canonical order:
1. Context and cost: "set themselves apart through breakthrough performance ... but also by their extremely high computational and storage costs."
2. Gap: "the applicability and performance of existing compression techniques is limited by the scale and complexity of GPT models."
3. Method in one phrase: "a new one-shot weight quantization method based on approximate second-order information".
4. Numbers: "175 billion parameters in approximately four GPU hours", "3 or 4 bits per weight", "with negligible accuracy degradation".
5. Relative claim: "more than doubles the compression gains relative to previously-proposed one-shot quantization methods".
6. Secondary regime: "reasonable accuracy in the extreme quantization regime".
7. Speedups tied to named hardware: "around 3.25x when using high-end GPUs (NVIDIA A100) and 4.5x when using more cost-effective ones (NVIDIA A6000)."

**Introduction.**
- The cost is made concrete with a number: "the parameters of GPT3-175B occupy 326GB (counting in multiples of 1024) of memory".
- The gap is a chain of reasoning: retraining is too expensive, post-training would be appealing, but accurate post-training methods don't scale, and RTN fails at high compression. It ends as an open question: "It therefore remains open whether one-shot post-training quantization to higher compression rates is generally-feasible."
- A bold run-in "Contribution." paragraph follows, in prose rather than bullets. The method is defined by two properties: "efficient enough to execute on models with hundreds of billions of parameters in at most a few hours, and precise enough to compress such models to 3 or 4 bits".
- The novelty claim is hedged: "To our knowledge, we are the first to show".
- The intro anticipates the objection that the result is obvious: "This high degree of compression may appear natural, as these networks are overparametrized; yet ...".
- Limitations already appear in the intro: "In terms of limitations, our method currently does not provide speedups for the actual multiplications".

**Method.** The method is built in numbered steps, each a bold run-in heading that names the idea: "Step 1: Arbitrary Order Insight.", "Step 2: Lazy Batch-Updates.", "Step 3: Cholesky Reformulation." Each step has the same shape: problem, then observation, then fix, then quantified effect. Examples:
- Observation: "Interestingly, we find that, while this quite natural strategy does indeed seem to perform very well, its improvement over quantizing the weights in arbitrary order is generally small".
- Hedged causal explanation: "Most likely, this is because ...".
- Complexity result: "This reduces the overall runtime from O(drow · d3col ) to O(max {drow · d2col , d3col })".
- Honest scoping: "Although this strategy does not reduce the theoretical amount of compute, it effectively addresses the memory-throughput bottleneck."

Background summarizes the prior method (OBQ) before modifying it: "To aid understanding, we first briefly summarize the original OBQ method." Its weakness is stated with a complexity bound, not an adjective: "cubic input dependency O(drow · d3col )". The final section header is honest: Summary and Limitations.

**Evaluation.** Opens with an "Overview." paragraph that serves as a roadmap ("We begin ... Next ... Then ... Finally"). The baseline is defined carefully so the comparison is fair: "exactly the same asymmetric per-row grid that is also used for GPTQ". Comparisons are precise: "GPTQ loses only 0.03 perplexity at 4-bit on the 175B model, while RTN drops 2.2 points, performing worse than the 10× smaller full-precision 13B model." Weaker results get the same matter-of-fact wording: "GPTQ performs on par at 4-bit, and slightly worse than the most accurate methods at 3-bit." An anomaly is footnoted rather than hidden ("with the exception of OPT-66B"). Speedup credit is attributed: "almost all of the speedup is due to our kernels".

**Hedging.** "appear", "might", "We suspect", and "To our knowledge" are used heavily. Even favorable surprises are hedged: "GPTQ surprisingly performs slightly better. We suspect that ...".

**Conclusion** is about 100 words: a one-line recap, the usability result, a hope, then "we emphasize some significant limitations".

**Things not to copy:** "truly large language models", "two largest (and interesting)", and the "breakthrough performance" opener.

---

## 3. AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration

**Title.** Acronym, then the mechanism ("Activation-aware"), then the target ("On-Device LLM"), then the two goals.

**Abstract (~250 words).** Its distinctive feature is short declarative sentences that walk through the insight one step at a time:
- "AWQ finds that not all weights in an LLM are equally important."
- "Protecting only 1% salient weights can greatly reduce quantization error."
- "To identify salient weight channels, we should refer to the activation distribution, not weights."

Then come the design constraint, the derivation, the generalization argument ("AWQ does not rely on any backpropagation or reconstruction, so it generalizes"), the system, and the speedup ("more than 3× speedup over the Huggingface FP16 implementation").

**Introduction.**
- The motivation is application-driven ("Deploying large language models (LLMs) directly on edge devices is crucial.") and grounded in hardware numbers: "GPT-3 has 175B parameters, which is 350GB in FP16, while the latest B200 GPU only has 192GB memory, let alone edge devices."
- The gap is stated against the single closest work, by name: "The closest work is GPTQ", followed by "However, it may overfit the calibration set during reconstruction".
- The method paragraph starts from the observation: "Our method is based on the observation that weights are not equally important for LLMs' performance." It uses "the insight is that" framing and points to the evidence ("(Table 1)", "(Equation 2)") inside the intro.
- No contribution bullets.

**Method: from observation to method, step by step.** This is the clearest example in the set.
1. Pilot experiment: "To verify the idea, we benchmark the performance of quantized LLMs when skipping part of the weight channels in Table 1."
2. Contrast with the obvious heuristic: "But we find skipping the weight channels with large norm ... does not significantly improve the quantized performance".
3. Hypothesis: "We hypothesize that the input features with larger magnitudes are generally more important."
4. A bold "Limitations:" run-in on the authors' own interim idea: "such a mixed-precision data type will make the system implementation difficult."
5. Error analysis with numbered empirical facts ("(1) ... (2) ... (3)"), then the scaling equation, then verification ("To verify the idea, we multiply the 1% salient channels with s > 1"). The diminishing return is reported: "Nonetheless, the best PPL actually appears at s = 2."
6. The search objective is stated formally, and simplicity is defended: "we simply use a very simple search space".

The systems section is motivated by profiling, using bold run-ins that are themselves claims: "Generation stage is memory-bound.", "Weight access dominates memory traffic." Hardware is named with specs: "The 4090 GPU has a peak computation throughput of 165 TFLOPS and a memory bandwidth of 1TB/s."

**Evaluation.** Bold run-in headings ("Results on LLaMA models.", "Better data-efficiency for the calibration set.", "Robust to the calibration set distributions."). Many figure and table captions contain the claim itself, e.g. Table 9: "Our method is orthogonal to GPTQ". The exclusion of a model family is justified in a single sentence: "There are other open LLMs like BLOOM ..., but they are generally worse in quality, so we do not include them".

**Hedging.** Weak overall. "to the best of our knowledge" appears once. Most claims are flat and evaluative ("consistently outperforms", "lossless", "exceptional extensibility").

**Conclusion** (~100 words) is a recap only, with no limitations section.

**Things not to copy:** "democratizes" (used three times), "astronomical model size", "nimble system", "boasts", "push-the-button solution", "turn-key solution", the adoption list of companies in the intro, the invented word "generability", typos ("Microsfot", "quantiztion"), and "despite we are doing".

---

## 4. Deep Compression (Han, Mao, Dally, ICLR 2016)

**Title.** Coined name, then a colon, then the three techniques listed: "Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding". Readers get the whole pipeline from the title.

**Abstract (~200 words).** The problem sentence is tied to a deployment target: "making them difficult to deploy on embedded systems with limited hardware resources." The pipeline is enumerated, then the numbers are given per stage ("Pruning, reduces the number of connections by 9× to 13×"), then per model with before/after sizes ("by 35×, from 240MB to 6.9MB, without loss of accuracy"). The hardware implication comes next ("fitting the model into on-chip SRAM cache rather than off-chip DRAM memory"), followed by speed and energy ranges.

**Introduction.**
- Motivation comes as two numbered issues ("First, ...", "The second issue is energy consumption.").
- The concrete constraints are memorable: "apps above 100 MB will not download until you connect to Wi-Fi".
- Physical numbers do the persuading: "a 32bit DRAM memory access takes 640pJ, which is 3 orders of magnitude of an add operation." A back-of-envelope calculation is worked inline: "(20Hz)(1G)(640pJ) = 12.8W just for DRAM access".
- The goal is stated: "Our goal is to reduce the storage and energy required". Then the "Our main insight is that" framing.

**Method.** Each stage gets its own section. Equations are introduced with a worked toy example: "There are 4 × 4 = 16 weights originally but there are only 4 shared weights". The compression ratio is computed by hand (16 ∗ 32/(4 ∗ 32 + 2 ∗ 16) = 3.2). Design choices are compared explicitly (three centroid initializations) and justified with a mechanism: "Larger weights play a more important role than smaller weights ... but there are fewer of these large weights."

**Evaluation and discussion.** The benchmark choice is justified by the application: "So when benchmarking the performance and energy efficiency, we consider the case when batch size = 1." The paper is honest about what it did not measure: "we didn't benchmark the quantized model." It also reports where the advantage vanishes: "In this scenario, pruned network no longer shows its advantage." Overheads are counted: "The compression rate includes the overhead of the codebook and sparse indexes."

Related work comes late and is chronological/thematic; its differences from prior work are stated in a single line each ("Different from HashNet ..."). A separate Future Work section describes what the hardware could do. The conclusion (~120 words) repeats the headline numbers and the SRAM/DRAM energy argument.

**Things not to copy:** frequent grammar slips ("prune the networking", "we the zero padding solution"), "surprisingly high compression rate", and "potentially makes ... more energy efficient" (it is vague; the paper's own numbers are better).

---

## Cross-paper patterns (transferable rules)

1. **Put the headline number in the abstract's method sentence, tied to its unit and its cost.** Use "x" for compression or speedup, "bits per weight" for precision, absolute sizes (MB/GB) for memory, and named hardware for speed. Evidence: "35×, from 240MB to 6.9MB, without loss of accuracy"; "175 billion parameters in approximately four GPU hours"; "around 3.25x when using high-end GPUs (NVIDIA A100)".

2. **Make the problem concrete with a physical or hardware number in the first paragraph.** Evidence: "occupy 326GB (counting in multiples of 1024) of memory"; "the latest B200 GPU only has 192GB memory, let alone edge devices"; "a 32bit DRAM memory access takes 640pJ".

3. **State the gap as specific limitations of named prior work, ending in an open problem or question.** Evidence: "have only been studied for models with less than 350M parameters"; "It therefore remains open whether one-shot post-training quantization to higher compression rates is generally-feasible."; "The closest work is GPTQ".

4. **Use observation, then method: report a pilot measurement, then derive the method from it.** Name it "observation" or "insight" once and keep the name. Evidence: "Our method is based on the observation that weights are not equally important"; "Our main insight is that, pruning and trained quantization are able to compress the network without interfering each other"; "Step 1: Arbitrary Order Insight."

5. **Pair every analytic finding with a control or the naive alternative.** Evidence: "As a control, we apply the same procedure for random non-outlier feature dimensions"; "leading to a similar marginal improvement as random selection".

6. **Break the method into named, numbered steps, each following problem, observation, fix, quantified effect.** Evidence: "Step 2: Lazy Batch-Updates."; "This provides an order of magnitude speedup for very large models in practice".

7. **Quantify comparisons with both deltas and an anchor reference point.** Evidence: "GPTQ loses only 0.03 perplexity at 4-bit on the 175B model, while RTN drops 2.2 points"; "performing worse than the 10× smaller full-precision 13B model"; "AWQ only increases the perplexity by 0.5-0.6, while GPTQ has 2.3-4.9 worse perplexity."

8. **Define baselines so the comparison is visibly fair, and justify any exclusions.** Evidence: "exactly the same asymmetric per-row grid that is also used for GPTQ"; "they also do not outperform GPTQ (Frantar et al., 2022), thus not included for study."

9. **Separate what the method does and does not speed up, and say what you did not measure.** Evidence: "Although this strategy does not reduce the theoretical amount of compute"; "we didn't benchmark the quantized model."; "our method obtains speedups from reduced memory movement, and does not lead to computational reductions."

10. **Report regimes where the method loses, in the same flat tone as the wins.** Evidence: "The quantization overhead can slow inference for models with less than 6.7B parameters"; "slightly worse than the most accurate methods at 3-bit"; "pruned network no longer shows its advantage."

11. **Hedge interpretations, not measurements.** Use "We hypothesize", "We suspect", "Most likely", "appears" for causes, and plain past/present tense for numbers. Evidence: "We hypothesize that model size is only one important covariate among many"; "We suspect that this is because"; "To our knowledge, we are the first to show".

12. **Use bold run-in paragraph headings that name the idea, or even state the claim.** Evidence: "Generation stage is memory-bound."; "Weight access dominates memory traffic."; "Contribution."; "Baselines."

13. **Enumerate limitations with reasons and future-work pointers, and say why each was out of scope.** Evidence: "A third limitation is that we do not use Int8 multiplication for the attention function."; "Since current GPUs and TPUs do not support this data type, we believe this is best left for future work."

14. **Credit concurrent work precisely: give its scale and call it complementary when it is.** Evidence: "There are two methods that were developed in parallel to ours"; "These methods are complementary with LLM.int8()."; "Our method is orthogonal to GPTQ."

15. **Make captions carry the takeaway, not just the content.** Evidence: "Pruning doesn't hurt quantization."; "We can see once systematic outliers occur at a scale of 6.7B parameters, regular quantization methods fail".

**Sentence-level habits across the set.** Sentences run mostly 15–30 words. "We" is active throughout ("We find", "We observe", "We measure"). Topic sentences state the finding first and give the numbers second. Terminology is held fixed: "salient weights", "outlier features", "RTN", "W4A16", "INT3-g128". None of the papers bullets its contributions; contributions sit in prose, sometimes under a bold "Contribution." heading. Roadmaps appear only in GPTQ's evaluation "Overview."

**Avoid** (copied from the weaker spots in these papers): "democratizes", "astronomical", "breakthrough performance", "truly large", "incredibly", "Luckily", "boasts", "push-the-button", "turn-key", "surprisingly high". Also avoid "first" claims without a to-our-knowledge qualifier, and adoption lists placed in the intro.
