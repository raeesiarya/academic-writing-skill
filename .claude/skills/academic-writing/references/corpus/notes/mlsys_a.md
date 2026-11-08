# Style notes: ML-systems papers (set A)

Papers: FlashAttention (NeurIPS 2022, `mlsys_flashattention.txt`), vLLM / PagedAttention (SOSP 2023, `mlsys_vllm.txt`), ZeRO (SC 2020, `mlsys_zero.txt`), TVM (OSDI 2018, `mlsys_tvm.txt`).
These notes cover how the papers are written, not what they found. All quotes are verbatim; pdftotext hyphenation and column breaks are removed.

---

## 1. FlashAttention (NeurIPS)

**Title.** Name, colon, then a three-part claim: "Fast and Memory-Efficient Exact Attention with IO-Awareness". The title names the benefit (fast, memory-efficient), what is kept (exact), and the mechanism (IO-awareness).

**Abstract (~250 words, eight sentences).** The moves come in a strict order:
1. Problem with its cause, in one sentence: "Transformers are slow and memory-hungry on long sequences".
2. Prior work and its gap: approximate methods "often do not achieve wall-clock speedup".
3. The missing principle, stated as an argument: "We argue that a missing principle is making attention algorithms IO-aware".
4. Method with its mechanism ("uses tiling to reduce the number of memory reads/writes").
5. Theory ("optimal for a range of SRAM sizes").
6. Extension (block-sparse).
7. Numbers, each paired with its workload and baseline: "15% end-to-end wall-clock speedup on BERT-large (seq. length 512) compared to the MLPerf 1.1 training speed record", then 3× and 2.4×.
8. New capability with accuracy figures (Path-X 61.4%).

Every number carries its configuration in parentheses (seq. length), so no number appears without context.

**Introduction.** The first sentence gives broad context: "Transformer models [82] have emerged as the most widely used architecture in applications such as natural language processing and image classification." The paper then asks a research question: "An important question is whether making attention faster and more memory-efficient can help Transformer models address their runtime and memory challenges for long sequences." The gap is diagnosed by naming a cause, not just asserting that prior work falls short: "One main reason is that they focus on FLOP reduction (which may not correlate with wall-clock speed) and tend to ignore overheads from memory access (IO)."

The method paragraph is built as goal, requirements, and techniques:
- Goal: "Our main goal is to avoid reading and writing the attention matrix to and from HBM."
- Requirements, as inline (i)/(ii): "This requires (i) computing the softmax reduction without access to the whole input".
- Techniques, mirrored as (i)/(ii): "We apply two well-established techniques to address these challenges."

The paper admits its cost up front and then turns it into a win: "Even with the increased FLOPs due to recomputation, our algorithm both runs faster (up to 7.6x on GPT-2 [67], Figure 1 right)". Contributions are three bold run-in bullets (Faster Model Training / Higher Quality Models / Benchmarking Attention). Each bullet opens with a one-clause claim ("FlashAttention trains Transformer models faster in wall-clock time.") followed by numbers. There is no roadmap sentence. Related work goes to an appendix ("Related work is given in Appendix A.").

**Honest negatives in the intro.** "for sequence length beyond 1K, some approximate attention methods (e.g., Linformer) start to become faster." Claims of superiority are scoped: "faster than all existing approximate attention methods that we know of."

**Background.** Short and scoped ("We focus here on GPUs."). Bold run-in headings (GPU Memory Hierarchy. Execution Model. Kernel fusion.) and concrete hardware numbers: "As an example, the A100 GPU has 40-80GB of high bandwidth memory (HBM)". A numbered list defines compute-bound versus memory-bound.

**Method.** Each section opens with what it will show ("We show how to compute exact attention with fewer HBM reads/writes…"). The main idea comes in one plain-language sentence before the math: "The main idea is that we split the inputs Q, K, V into blocks, load them from slow HBM to fast SRAM". The prose points to algorithm lines ("Algorithm 1 line 3"). Theorems are followed by an intuitive proof sketch ("The main idea of the proof is…"). Each theoretical claim is tied to an experiment: "We validate that the number of HBM accesses is the main determining factor of attention run-time." Limits on the claim are stated precisely: "For large enough block size (beyond 256), the runtime is then bottlenecked by other factors (e.g., arithmetic operations)."

**Evaluation.** Opens by naming its claims: "We validate two claims about training time and model accuracy, and report attention runtime and memory benchmarks." It then repeats the three bullets with numbers before any subsection. Subsections use bold dataset or task run-ins (BERT. GPT-2. Long-range Arena.). Each paragraph starts with the takeaway, then the evidence: "Table 1 compares our training time to the implementation from Nvidia that set the training speed record for MLPerf 1.1 [58]. Our implementation is 15% faster." Captions state takeaways too: "HBM access is the primary factor affecting runtime." Variance and setup sit in captions: "Averaged over 10 runs on 8×A100 GPUs." A possible confound is ruled out with a reason: "FlashAttention achieves the same perplexity as the other two implementations, as we do not change the model definition." Fairness to baselines appears in a footnote: "Our reproduced baselines perform better than as reported in the original comparison [80]."

**Hedging.** Light, and confined to explanations: "The discrepancies may be due to subtle distribution shifts". Future work is framed as "exciting future work".

**Limitations.** A real section, "Limitations and Future Directions", with three bold run-ins. It opens with a concrete cost: "Our current approach to building IO-aware implementations of attention requires writing a new CUDA kernel for each new attention implementation." It closes on aspiration: "We hope our work inspires IO-aware implementations of additional modules."

---

## 2. vLLM / PagedAttention (SOSP)

**Title.** A descriptive problem plus mechanism: "Efficient Memory Management for Large Language Model Serving with PagedAttention".

**Abstract (~180 words).** Requirement, then why existing systems fail, then the cause, then the method with its analogy, then two numbered properties, then one headline number, then when the gain grows.
- Opens with a requirement, not a problem: "High throughput serving of large language models (LLMs) requires batching sufficiently many requests at a time."
- Gap with mechanism: the KV cache "memory for each request is huge and grows" and shrinks dynamically.
- Properties: "(1) near-zero waste in KV cache memory and (2) flexible sharing".
- One aggregate number: 2-4× throughput "with the same level of latency" against named systems (FasterTransformer, Orca).
- Where the gain grows: "The improvements are more pronounced with longer sequences, larger models, and more complex decoding algorithms (§4.3)." (This sentence appears in the intro; the abstract has a near-identical one.)

**Introduction.** Opens on applications and cost: "The emergence of large language models (LLMs) like GPT [5, 37] and PaLM [9] have enabled new applications such as programming assistants". It motivates with a cited number: "According to recent estimates, processing an LLM request can be 10× more expensive than a traditional keyword query [43]." The paper then quantifies the bottleneck with its own measurement from Fig. 1, with memory percentages for a 13B model on an A100.

The gap is announced as "we observe": "In this paper, we observe that existing LLM serving systems [31, 60] fall short of managing the KV cache memory efficiently." It is enumerated with an explicit count: "These characteristics make the existing systems' approach significantly inefficient in two ways:" followed by "First, the existing systems [31, 60] suffer from internal and external memory fragmentation." and "Second, the existing systems cannot exploit the opportunities for memory sharing." The gap is backed with profiling numbers: "only 20.4% - 38.2% of the KV cache memory is used to store the actual token states in the existing systems."

The key insight is an analogy, made explicit in a mapping: "one can think of blocks as pages, tokens as bytes, and requests as processes." Contributions follow "In summary, we make the following contributions:" with four bullets, each opening with a verb: identify / propose / design and implement / evaluate. The first bullet makes characterization a contribution of its own: "We identify the challenges in memory allocation in serving LLMs and quantify their impact on serving performance." Accuracy is reassured in passing: "without affecting the model accuracy at all".

**Challenges section (§3).** A dedicated "Memory Challenges in LLM Serving" section sits between background and design. It distills the issue into one line ("In other words, the serving system's throughput is memory-bound.") and then lists bold run-in challenges (Large KV cache. Complex decoding algorithms. Scheduling for unknown input & output lengths.). Each challenge is quantified with back-of-envelope arithmetic shown inline: "the KV cache of a single token demands 800 KB of space, calculated as 2 (key and value vectors) × 5120 (hidden state size) × 40 (number of layers) × 2 (bytes per FP16)." Predictions are hedged with "we believe": "Therefore, we believe the memory will become an increasingly significant bottleneck."

**Design (§4).** It opens with an architecture figure and a roadmap: "Next, We describe the PagedAttention algorithm in §4.1." Each component is introduced by its key idea: "The key idea behind vLLM's memory manager is analogous to the virtual memory [25] in operating systems." The system is walked through with a worked example and circled step numbers ①②③ tied to a figure ("Next, we walk through an example, as in Fig. 6, to demonstrate how vLLM executes PagedAttention…"). Running example text ("Four score and seven years ago") is reused across Figs. 5–9, so readers learn one example once. Tradeoffs are flagged and forwarded to an ablation: "However, a larger block size also increases memory fragmentation. We study the effect of block size in §7.2." Design questions are posed explicitly: "(1) Which blocks should it evict?" / "(2) How to recover evicted blocks if needed again?" Minor choices are justified honestly in footnotes: "The two designs have no performance difference and we choose the second one for easy implementation."

**Implementation.** Gives the system's size: "The vLLM engine is written in 8.5K lines of Python and 2K lines of C++/CUDA code." Kernel optimizations are numbered inline in italics: (1) Fused reshape and block write, (2)…, (3)…

**Evaluation.** Setup uses bold run-ins (Model and server configurations. Workloads. Baseline 1: FasterTransformer. Baseline 2: Orca. Key metrics.). Baselines are framed generously: the authors build an oracle variant, "This shows the upper-bound performance of Orca, which is infeasible to achieve in practice." Reimplementation is admitted: "Since Orca is not publicly available for use, we implement our own version of Orca." The metric is defined along with the behaviour that counts as good: "A high-throughput serving system should retain low normalized latency against high request rates." Cost-driven compromises are disclosed: "we use 15-minute traces for the OPT-175B model due to the cost limit."

Results are stated as ranges, each tied to a named baseline and an equal-latency condition: "vLLM can sustain 1.7×–2.7× higher request rates compared to Orca (Oracle) and 2.7×–8× compared to Orca (Max), while maintaining similar latencies." Each claim is followed by a mechanism ("This is because vLLM's PagedAttention can efficiently manage the memory usage"). Exceptions are named and explained: "One exception is Fig. 12 (f), where vLLM's advantage over Orca (Oracle) and Orca (Pow2) is less pronounced."

The ablations report overhead candidly ("this leads to 20–26% higher attention kernel latency") and then argue why it does not matter ("We believe the overhead is small as it only affects the attention operator"). The default parameter is justified from data: "In practice, we find that the block size 16 is large enough to efficiently utilize the GPU and small enough to avoid significant internal fragmentation in most workloads."

**Discussion.** The paper bounds where the idea applies: "However, this does not generally hold for every GPU workload." It even says the technique could hurt: "In such scenarios, introducing the vLLM's techniques may rather degrade the performance".

**Related work (end, §9).** Grouped by bold category. Each group ends on what the group misses: "However, these general systems fail to take into account the autoregressive property and token state of LLM inference". The closest competitor gets its own paragraph ("Among them, Orca [60] is most relevant to our approach."), framed as complementary: "The iteration-level scheduling in Orca [60] and PagedAttention in vLLM are complementary techniques".

**Conclusion.** Three sentences: what we propose, the insight, and one number. "Our experiments show that vLLM achieves 2-4× throughput improvements over the state-of-the-art systems."

---

## 3. ZeRO (SC)

**Title.** "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models". The title names an aspirational target scale.

**Abstract (~200 words, two paragraphs).** Paragraph 1: problem ("Large deep learning models offer significant accuracy gains, but training billions to trillions of parameters is challenging."), limitation of DP/MP, method, and an analytical claim ("has the potential to scale beyond 1 Trillion parameters"). Paragraph 2: measured results as x-factors against the state of the art: "This represents an 8x increase in model size and 10x increase in achievable performance over state-of-the-art." The abstract keeps two kinds of claim apart: analytical potential and measured results.

**"Extended Introduction" (~5 pages).** Opens with a trend sentence: "Deep Learning (DL) models are becoming larger, and the increase in model size offers significant accuracy gain." The gap is backed by a concrete limit, "runs out of memory for models with more than 1.4B parameters", and by the authors' own measurement of the baseline: "(less than 5% of hardware peak)". The paper pivots with a rhetorical question: "So, how can we overcome the limitations of existing solutions and train large models more efficiently?" It then classifies the problem into two parts (model states versus residual states), and that split organises the whole paper (ZeRO-DP / ZeRO-R, §5/§6, §7/§8).

Tradeoffs are compressed into one balanced sentence: "DP has good compute/communication efficiency but poor memory efficiency while MP can have poor compute/communication efficiency." Stages are listed with their cost and benefit together: "4x memory reduction, same communication volume as DP". Arithmetic sanity checks appear in prose: "16TB divided by 1024 is 16GB, which is well within a reasonable bound for a GPU". The paper anticipates reader questions: "it is natural to ask: Do we still need MP, and when?" Results are previewed under bold run-ins (Model Size / Speed / Scalability / Democratization / New SOTA Model).

**Insights section (§4 "ZeRO: Insights and Overview").** "ZeRO powered DP is based on three key insights:" followed by a)/b)/c), each insight one or two sentences. The constraint that rules out trivial solutions is stated explicitly: "Please note efficiency is a key here: without this constraint, trivial solutions like moving all the parameter states to the CPU memory, or increasing the MP degree arbitrarily can reduce memory footprint."

**Motivation/analysis section.** Its title is a question, "Where Did All the Memory Go?", with a conversational opener: "Let's take a step back to examine the memory consumption of the current training system." The memory accounting is derived from first principles (2Ψ + 2Ψ + KΨ = 16Ψ) and illustrated with GPT-2 1.5B.

**Design ("Deep Dive").** Subsections are named by symbol and function (P_os : Optimizer State Partitioning). Each ends with a bold "Memory Savings:" paragraph that gives a formula and then a worked example from Figure 1. Objections are pre-empted: "While this may seem to incur significant communication overhead at first glance, we show that this approach only increases the total communication volume of a baseline DP system to 1.5x". The communication section opens with the reader's worry: "it is only natural to ask if we are trading communication volume for memory efficiency." It answers in the next sentence, before the derivation: "The answer is in two parts:".

**Evaluation.** Uses bold run-ins (Implementation / Hardware / Baseline / Model Configurations). Hardware is spelled out: "We conducted our experiments on a cluster of 400 V100 GPUs (25 DGX-2 nodes) with 800 Gbps internode communication bandwidth." The baseline choice is justified: "we use Megatron-LM because it is, to our knowledge, the state-of-art." Results give absolute numbers alongside the fraction of peak: "a sustained throughput of 15 PetaFlops (over 30% of the peak)". Dips are explained: "the slight reduction in performance beyond 100B is due to lack of enough memory to run larger batch sizes." Exceptions are flagged: "The only caveat is the performance drop between C4 and C5 for 60B parameter model." Configurations C1–C5 are defined in a table so the prose can say "C1 vs C2". A table caption confirms the analysis against measurement: "demonstrating that our memory analysis provides realistic upper bounds on model sizes."

**Tone: the cautionary case.** ZeRO uses exclamation marks ("Running a model with a trillion parameters efficiently is no longer impossible!") and grand claims ("represents a revolutionary transformation", "it is still just a tip of the iceberg"). It also relies on untested extrapolation ("We expect this behaviour to continue further as we increase the number of GPUs beyond 400."). It does contain one good scoped disclaimer: "While we do not claim knowing or addressing all of them". The prose also has typos and grammar slips ("complimentary" for complementary, "pptimizer"). It has no limitations section.

**Related work (early, §2).** Sorted by approach, and each paragraph ends with positioning: "In contrast, ZeRO obtains the same or better memory efficiency than PP without incurring functionality, performance and convergence related restrictions of PP." Others are labelled "orthogonal" or complementary: "ZeRO is orthogonal to these efforts".

---

## 4. TVM (OSDI)

**Title.** "TVM: An Automated End-to-End Optimizing Compiler for Deep Learning". The title stacks adjectives that each map to a contribution.

**Abstract (~170 words).** Need ("There is an increasing need to bring machine learning to a wide diversity of hardware devices."), status quo ("Current frameworks rely on vendor-specific operator libraries and optimize for a narrow range of server-class GPUs."), the cost of the status quo ("requires significant manual effort"), method, challenges solved, a qualitative result ("competitive with state-of-the-art, hand-tuned libraries"), and impact ("The system is open sourced and in production use inside several major companies."). Note: **no numbers in the abstract**. This is weaker than the other three; the 1.2×–3.8× figure appears only at the end of the intro.

**Introduction.** Opens on capability: "Deep learning (DL) models can now recognize images, process natural language, and defeat humans in challenging strategy games." Figure 1 makes the hardware divergence visible, and its caption gives the takeaway: "This divergence must be addressed when generating optimized code." The gap is framed as a dilemma: frameworks "must make the difficult choice between: (1) avoiding graph optimizations that yield new operators not in the predefined operator library, and (2) using unoptimized implementations of these new operators." Then the paper pivots: "we take a fundamentally different, end-to-end approach."

The challenges get their own framing: "This goal requires addressing the key challenges described below." Two bold-headed challenge paragraphs follow (Leveraging Specific Hardware Features and Abstractions; Large Search Space for Optimization). Each challenge paragraph also argues why the obvious alternative fails (black-box auto-tuning is costly; predefined cost models are hard to build). Challenges map one to one onto solutions: "TVM addresses these challenges with three key modules." followed by (1)(2)(3). The contributions follow "This paper makes the following contributions:" with verb-led bullets (identify / introduce / propose and implement / build). The headline number comes in the last intro paragraph: "achieves speedups ranging from 1.2× to 3.8× over existing frameworks backed by hand-optimized libraries."

**Overview section.** An end-to-end walkthrough: "This section describes TVM by using an example to walk through its components." The system diagram doubles as a paper map: "Figure 2 summarizes execution steps in TVM and their corresponding sections in the paper." A code snippet shows the user's view ("End-User Example.").

**Design.** Each subsection follows the same arc: problem, existing approach, why it is insufficient, our primitive, and a micro-result (with a figure) that validates it right away. Examples: "We find that fused operators generate up to a 1.2× to 2× speedup by reducing memory accesses." and "Peak compute utilization increased from 70% with no latency hiding to 88% with latency hiding." Necessity is argued before the solution: "This approach is no longer sustainable when targeting an increasing number of hardware back-ends", followed by "We therefore need an extensible solution." New terms are coined by contrast with a familiar one: "We dub this tensorization: it is analogous to vectorization for SIMD architectures but has significant differences." Alternatives are compared in a table (Table 1: data cost / model bias / needs hardware info / learns from history). A design choice is justified with a measured comparison and closed with a fair hedge: "As a result, we chose gradient tree boosting as the default cost model in our experiments." and "Nevertheless, we believe that both approaches are valuable and expect more future research on this problem."

**Evaluation.** Framed by research questions in bullets: "We now focus on an end-to-end evaluation that aims to answer the following questions:", for example "Can TVM optimize DL workloads over multiple platforms?". Subsections are ordered by platform (server GPU, embedded CPU, embedded GPU, FPGA). Baselines are pinned to versions or commits ("MXNet (v1.1), Tensorflow (v1.7)", "Tensorflow Lite (TFLite, commit: 7558b085)"). Each result gives a range and a cause: "with speedups ranging from 1.6× to 3.8× due to both joint graph optimization and the automatic optimizer". Outliers are explained: "DQN's 3.8 x speedup results from its use of unconventional operators". Disappointing results are owned: "Unfortunately, due to Amdahl's law, the overall performance of the FPGA accelerated system was bottlenecked by the sections of the workload that had to be executed on the CPU." Baseline caveats go in footnotes ("According to personal communication [41], TC is not yet meant to be used for compute-bound problems."; "DCGAN and LSTM results are not presented because they are not yet supported by the baseline."). Engineering effort is quantified: "Adding the specialized accelerator back-end took ∼2k LoC in Python."

**Related work (§7, near the end).** Organised by category (frameworks, graph DSLs, Halide and DSLs, auto-tuning, accelerators). Credit is given explicitly: "We adopt Halide's insights". Each category ends with the differentiator: "We specifically focus on solving the new scheduling challenges of DL workloads for GPUs and specialized accelerators."

**Conclusion.** Short: restated contribution plus a hope ("We hope this work will encourage additional studies of end-to-end compilation approaches"). There is no limitations section.

---

## 5. Sentence-level habits (all four)

- **Voice:** first-person plural, active ("We propose", "We observe", "We implement"). The system name is the grammatical subject of result sentences ("FlashAttention trains…", "vLLM can sustain…", "TVM outperforms…").
- **Sentence length:** mostly 15–30 words. The longest sentences are enumerations, and numbers carry the load.
- **Paragraph openers:** the topic sentence states the claim, and the evidence follows (FlashAttention "BERT. FlashAttention yields the fastest single-node BERT training speed that we know of.").
- **Run-in headings:** bold run-in paragraph labels are everywhere (challenges, baselines, setup items, result categories, limitations). They let reviewers skim.
- **Signposting:** section openers say what the section does ("In this section, we evaluate…", "We present the analysis in this section."). Forward references use § and Fig. numbers ("We study the effect of block size in §7.2").
- **Terminology:** coined names are used consistently (PagedAttention vs. vLLM; ZeRO-DP / ZeRO-R / P_os / C1–C5; tensorization). Once defined, abbreviations are never re-expanded or varied.
- **Inline enumeration:** (i)/(ii), (1)/(2), and a)/b)/c) inside sentences, mirrored between problem and solution.

## 6. What NOT to copy

- ZeRO's exclamation marks, "revolutionary transformation", "tip of the iceberg", and the "Last but not the least" register. Its untested extrapolations stated as expectations.
- TVM's number-free abstract.
- The typos and grammar slips that appear even in famous papers (ZeRO "complimentary", "pptimizer"; vLLM "facilities sharing", "Next, We"; FlashAttention "violaged", "that we know off").
- Unscoped "state-of-the-art" claims. The good papers scope them ("that we know of", "to our knowledge").
- Leaving related work out of the main body (FlashAttention's appendix placement suits NeurIPS page limits, but it is risky elsewhere).

---

## Cross-paper patterns: transferable rules

1. **Put numbers in the abstract, each paired with its baseline and workload.** "15% end-to-end wall-clock speedup on BERT-large (seq. length 512) compared to the MLPerf 1.1 training speed record"; "This represents an 8x increase in model size and 10x increase in achievable performance over state-of-the-art." (TVM's number-free abstract is the counterexample.)
2. **Diagnose the gap by its cause, not just its existence.** "One main reason is that they focus on FLOP reduction (which may not correlate with wall-clock speed) and tend to ignore overheads from memory access (IO)."
3. **Quantify the bottleneck with your own measurement before proposing anything.** "only 20.4% - 38.2% of the KV cache memory is used to store the actual token states in the existing systems."; "(less than 5% of hardware peak)".
4. **Count and enumerate the shortcomings, then mirror them in the solution.** "These characteristics make the existing systems' approach significantly inefficient in two ways:"; "TVM addresses these challenges with three key modules."
5. **State the key insight in one plain sentence, often as an analogy.** "one can think of blocks as pages, tokens as bytes, and requests as processes."; "ZeRO powered DP is based on three key insights:"
6. **List contributions as verb-led bullets, and treat characterization as a contribution.** "We identify the challenges in memory allocation in serving LLMs and quantify their impact on serving performance."; "We identify the major optimization challenges in providing performance portability".
7. **Admit the cost of your design, then show why it does not matter.** "Even with the increased FLOPs due to recomputation, our algorithm both runs faster"; "this leads to 20–26% higher attention kernel latency" followed by "We believe the overhead is small as it only affects the attention operator".
8. **Pre-empt the reader's objection in their own words, then answer it right away.** "it is only natural to ask if we are trading communication volume for memory efficiency." then "The answer is in two parts:"
9. **Show back-of-envelope arithmetic inline.** "the KV cache of a single token demands 800 KB of space, calculated as 2 (key and value vectors) × 5120 (hidden state size) × 40 (number of layers) × 2 (bytes per FP16)."; "16TB divided by 1024 is 16GB, which is well within a reasonable bound for a GPU".
10. **Give every result a mechanism ("This is because…", "due to…").** "This is because vLLM's PagedAttention can efficiently manage the memory usage"; "with speedups ranging from 1.6× to 3.8× due to both joint graph optimization and the automatic optimizer".
11. **Report results as ranges against named baselines under a matched condition.** "vLLM can sustain 1.7×–2.7× higher request rates compared to Orca (Oracle) and 2.7×–8× compared to Orca (Max), while maintaining similar latencies."
12. **Be generous to baselines and disclose how you obtained them.** "This shows the upper-bound performance of Orca, which is infeasible to achieve in practice."; "Since Orca is not publicly available for use, we implement our own version of Orca."; "Our reproduced baselines perform better than as reported in the original comparison [80]."
13. **Name exceptions and negative results, and explain them.** "One exception is Fig. 12 (f), where vLLM's advantage over Orca (Oracle) and Orca (Pow2) is less pronounced."; "for sequence length beyond 1K, some approximate attention methods (e.g., Linformer) start to become faster."; "Unfortunately, due to Amdahl's law…"
14. **Pin the setup down: hardware, versions, run counts, and cost compromises.** "We conducted our experiments on a cluster of 400 V100 GPUs (25 DGX-2 nodes) with 800 Gbps internode communication bandwidth."; "Averaged over 10 runs on 8×A100 GPUs."; "we use 15-minute traces for the OPT-175B model due to the cost limit."
15. **Scope superiority and generality claims, and say where the idea does not apply.** "faster than all existing approximate attention methods that we know of."; "However, this does not generally hold for every GPU workload."; "Our current approach to building IO-aware implementations of attention requires writing a new CUDA kernel for each new attention implementation."

Supporting habits: frame the evaluation with explicit research questions ("Can TVM optimize DL workloads over multiple platforms?"); write figure captions that state the takeaway ("HBM access is the primary factor affecting runtime."); validate a design micro-result right where the design is introduced ("Peak compute utilization increased from 70% with no latency hiding to 88% with latency hiding."); and justify defaults with data ("In practice, we find that the block size 16 is large enough to efficiently utilize the GPU and small enough to avoid significant internal fragmentation in most workloads.").
