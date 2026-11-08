#!/usr/bin/env python3
"""Mechanical checks for academic prose in a LaTeX paper (or a .md/.txt file).

Finds what is easy to miss by reading: informal words, hype words, dashes,
vague back-references, hard-coded cross-references, long sentences,
terminology drift, spelling variants of the same name, abbreviations used
before they are defined or defined twice, figures and tables that are never
referenced, and numbers in the abstract, introduction, or conclusion that do
not appear anywhere else in the paper.

Usage:
    python3 check.py PATH [--only CHECK,...] [--max N] [--long WORDS]

PATH is the main .tex file, a directory (the file with \\documentclass is found
automatically; main.tex is preferred), or a .md/.txt file. \\input, \\include,
and \\subfile are followed. Zero-argument \\newcommand macros are expanded so
that terms defined as macros are counted.

Checks: informal, hype, dashes, vague-refs, hardcoded-refs, long, terms,
variants, abbrev, floats, numbers.

Every hit is a candidate, not a verdict. Judge each one in context.
"""
import argparse
import bisect
import os
import re
import sys
from collections import defaultdict

# --------------------------------------------------------------------------
# Loading

INPUT_RE = re.compile(r"\\(?:input|include|subfile)\{([^}]+)\}")
SKIP_ENVS = {
    "equation", "equation*", "align", "align*", "alignat", "alignat*",
    "gather", "gather*", "multline", "multline*", "eqnarray", "eqnarray*",
    "displaymath", "math", "split", "cases", "tabular", "tabular*", "tabularx",
    "longtable", "array", "lstlisting", "verbatim", "Verbatim", "minted",
    "algorithmic", "algorithm2e", "tikzpicture", "thebibliography", "comment",
}
FLOAT_ENVS = {"figure": "figure", "figure*": "figure", "wrapfigure": "figure",
              "subfigure": "figure", "table": "table", "table*": "table",
              "wraptable": "table"}


def strip_comment(line):
    out, i = [], 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2])
            i += 2
            continue
        if c == "%":
            break
        out.append(c)
        i += 1
    return "".join(out)


def find_main(directory):
    cands = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".tex"):
                continue
            p = os.path.join(root, f)
            try:
                txt = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if re.search(r"^\s*\\documentclass", txt, re.M):
                cands.append(p)
    if not cands:
        sys.exit(f"No .tex file with \\documentclass found under {directory}")
    cands.sort(key=lambda p: (os.path.basename(p) != "main.tex", len(p)))
    return cands[0]


def load_tex(path, base, seen, warnings):
    lines = []
    path = os.path.normpath(path)
    if path in seen:
        return lines
    seen.add(path)
    with open(path, encoding="utf-8", errors="replace") as fh:
        for n, raw in enumerate(fh, 1):
            line = strip_comment(raw.rstrip("\n"))
            matches = list(INPUT_RE.finditer(line))
            if not matches:
                lines.append((path, n, line))
                continue
            lines.append((path, n, INPUT_RE.sub(" ", line)))
            for m in matches:
                name = m.group(1).strip()
                p = os.path.join(base, name)
                if not os.path.exists(p) and os.path.exists(p + ".tex"):
                    p += ".tex"
                if os.path.exists(p):
                    lines.extend(load_tex(p, base, seen, warnings))
                else:
                    warnings.append(f"{path}:{n}: included file not found: {name}")
    return lines


def load_plain(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return [(path, n, raw.rstrip("\n")) for n, raw in enumerate(fh, 1)]


# --------------------------------------------------------------------------
# LaTeX to prose

NONTEXT = (r"(?:cite[a-zA-Z]*|[cC]ref|[cC]pageref|ref|autoref|eqref|pageref|vref|Vref|"
           r"nameref|labelcref|subref|label|url|includegraphics|bibliography|"
           r"bibliographystyle|vspace|hspace|setlength|addtolength|newcommand|"
           r"renewcommand|providecommand|def|usepackage|documentclass|resizebox|"
           r"scalebox|includepdf|multicolumn|multirow|cline|hypersetup|color|"
           r"textcolor|definecolor|captionsetup|graphicspath)")
NONTEXT_RE = re.compile(r"\\" + NONTEXT + r"\*?(?:\[[^\]]*\])*(?:\{[^{}]*\})*")
MACRO_DEF_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand)\*?\s*\{?\\([a-zA-Z]+)\}?\s*\{(.*)\}\s*$")


def collect_macros(lines):
    macros = {}
    for _, _, line in lines:
        m = MACRO_DEF_RE.search(line)
        if not m or "#" in m.group(2):
            continue
        body = m.group(2)
        # keep only simple text bodies, e.g. {FooNet} or {\textsc{FooNet}}
        body = re.sub(r"\\(?:xspace|textsc|textrm|textsf|textbf|textit|emph|mbox|text)\b", "", body)
        body = body.replace("{", "").replace("}", "").strip()
        if body and not re.search(r"\\", body):
            macros[m.group(1)] = body
    return macros


def expand_macros(s, macros):
    if not macros:
        return s
    pat = re.compile(r"\\(" + "|".join(sorted(map(re.escape, macros), key=len, reverse=True))
                     + r")(?![a-zA-Z])(?:\{\})?")
    return pat.sub(lambda m: macros[m.group(1)], s)


def to_prose(s, macros):
    s = expand_macros(s, macros)
    s = re.sub(r"\\\((.*?)\\\)", " x ", s)
    s = re.sub(r"(?<!\\)\$[^$]*\$", " x ", s)
    s = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", s)
    s = NONTEXT_RE.sub(" ", s)
    s = re.sub(r"\\(?:item)\b(?:\[[^\]]*\])?", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", s)
    s = s.replace("\\%", "%").replace("\\&", "&").replace("\\_", "_").replace("\\#", "#")
    s = s.replace("``", '"').replace("''", '"')
    s = re.sub(r"[{}]", "", s)
    s = s.replace("~", " ")
    s = re.sub(r"\\[,;:! ]", " ", s)
    return re.sub(r"\s+", " ", s)


ENV_RE = re.compile(r"\\(begin|end)\{([^}]+)\}|\\\[|\\\]|\$\$")
SECTION_RE = re.compile(r"\\(chapter|section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}")


# --------------------------------------------------------------------------
# Document model

class Doc:
    def __init__(self, lines, tex):
        self.tex = tex
        self.macros = collect_macros(lines) if tex else {}
        self.paragraphs = []      # list of (text, offsets, locs, region)
        self.labels = {}          # label -> (kind, loc)
        self.refs = defaultdict(list)
        self.unlabeled_floats = []
        self.number_lines = []    # (region, loc, text)
        self.has_cleveref = False
        self.build(lines)

    def build(self, lines):
        in_doc = not self.tex
        state = {"skip": None, "stack": []}
        region = "body"
        seen_intro = False
        float_stack = []  # [kind, loc, has_label]
        cur = {"text": [], "offsets": [], "locs": [], "region": region}

        def flush():
            if cur["text"]:
                joined = " ".join(cur["text"])
                if joined.strip():
                    self.paragraphs.append((joined, cur["offsets"][:], cur["locs"][:], cur["region"]))
            cur["text"], cur["offsets"], cur["locs"] = [], [], []

        def add(piece, loc, reg):
            if cur["text"] and cur["region"] != reg:
                flush()
            cur["region"] = reg
            start = sum(len(t) + 1 for t in cur["text"])
            cur["text"].append(piece)
            cur["offsets"].append(start)
            cur["locs"].append(loc)

        for path, n, line in lines:
            loc = (path, n)
            if self.tex:
                if re.search(r"\\usepackage(?:\[[^\]]*\])?\{[^}]*cleveref", line):
                    self.has_cleveref = True
                if not in_doc:
                    if "\\begin{document}" in line:
                        in_doc = True
                        line = line.split("\\begin{document}", 1)[1]
                    else:
                        continue
                if "\\end{document}" in line:
                    line = line.split("\\end{document}", 1)[0]
                    in_doc = False
                if re.search(r"\\appendix\b", line):
                    region = "appendix"
                sm = SECTION_RE.search(line)
                if sm and sm.group(1) in ("chapter", "section"):
                    title = sm.group(2).lower()
                    if region != "appendix":
                        if "intro" in title and not seen_intro:
                            region, seen_intro = "intro", True
                        elif "conclu" in title:
                            region = "conclusion"
                        else:
                            region = "body"
                for lm in re.finditer(r"\\label\{([^}]+)\}", line):
                    kind = None
                    if float_stack:
                        kind = float_stack[-1][0]
                        float_stack[-1][2] = True
                    self.labels[lm.group(1)] = (kind, loc)
                for rm in re.finditer(
                        r"\\(?:[cC]ref|ref|autoref|eqref|pageref|vref|Vref|nameref|labelcref|subref|[cC]pageref)\*?\{([^}]+)\}",
                        line):
                    for key in rm.group(1).split(","):
                        self.refs[key.strip()].append(loc)
                reg_now = "abstract" if "abstract" in state["stack"] else region
                self.number_lines.append((reg_now, loc, line))
                if sm or re.match(r"\s*$", line):
                    flush()
                # environments and math, piece by piece
                prose_parts, pos = [], 0
                for m in ENV_RE.finditer(line):
                    if state["skip"] is None:
                        prose_parts.append(line[pos:m.start()])
                    if m.group(1) == "begin":
                        env = m.group(2)
                        state["stack"].append(env)
                        if env in FLOAT_ENVS:
                            float_stack.append([FLOAT_ENVS[env], loc, False])
                        if env == "abstract":
                            flush()
                        if state["skip"] is None and env in SKIP_ENVS:
                            state["skip"] = env
                            prose_parts.append(" x ")
                    elif m.group(1) == "end":
                        env = m.group(2)
                        if env in state["stack"]:
                            while state["stack"]:
                                if state["stack"].pop() == env:
                                    break
                        if env in FLOAT_ENVS and float_stack:
                            kind, floc, has = float_stack.pop()
                            if not has:
                                self.unlabeled_floats.append((kind, floc))
                        if state["skip"] == env and env not in state["stack"]:
                            state["skip"] = None
                        if env == "abstract":
                            prose_parts.append(" ")
                            piece = to_prose("".join(prose_parts), self.macros)
                            if piece.strip():
                                add(piece, loc, "abstract")
                            prose_parts = []
                            flush()
                    else:
                        tok = m.group(0)
                        if tok == "\\[" and state["skip"] is None:
                            state["skip"] = "\\["
                            prose_parts.append(" x ")
                        elif tok == "\\]" and state["skip"] == "\\[":
                            state["skip"] = None
                        elif tok == "$$":
                            if state["skip"] is None:
                                state["skip"] = "$$"
                                prose_parts.append(" x ")
                            elif state["skip"] == "$$":
                                state["skip"] = None
                    pos = m.end()
                if state["skip"] is None:
                    prose_parts.append(line[pos:])
                if not in_doc and not prose_parts:
                    continue
                reg_now = "abstract" if "abstract" in state["stack"] else region
                piece = to_prose("".join(prose_parts), self.macros)
                if sm:
                    if piece.strip():
                        add(piece.strip() + ".", loc, reg_now)
                    flush()
                elif piece.strip():
                    add(piece, loc, reg_now)
            else:
                if not line.strip():
                    flush()
                    continue
                self.number_lines.append((region, loc, line))
                add(line, loc, region)
        flush()


# --------------------------------------------------------------------------
# Sentences

ABBR_DOTS = ["e.g.", "i.e.", "et al.", "Fig.", "Figs.", "Eq.", "Eqs.", "Sec.", "Secs.",
             "vs.", "cf.", "etc.", "Tab.", "approx.", "resp.", "No.", "Ref.", "Refs.",
             "Dr.", "Mr.", "Ms.", "Prof.", "Inc.", "Ltd.", "St.", "Jr.", "Sr.", "w.r.t."]


def sentences(par):
    """Yield (sentence, start_offset) for one paragraph string."""
    text, masked = par, par
    for a in ABBR_DOTS:
        masked = masked.replace(a, a.replace(".", "\x00"))
    start = 0
    for m in re.finditer(r"(?<=[.!?])[\"')\]]?\s+(?=[\"'(\[]?[A-Z0-9\\])", masked):
        yield text[start:m.start() + 1].strip(), start
        start = m.end()
    if text[start:].strip():
        yield text[start:].strip(), start


def locate(offsets, locs, pos):
    i = bisect.bisect_right(offsets, pos) - 1
    return locs[max(i, 0)]


def fmt_loc(loc):
    path, n = loc
    try:
        rel = os.path.relpath(path)
        path = rel if not rel.startswith("..") else path
    except ValueError:
        pass
    return f"{path}:{n}"


def snippet(text, start, end, width=50):
    a, b = max(0, start - width), min(len(text), end + width)
    s = text[a:b].strip()
    return ("..." if a > 0 else "") + s + ("..." if b < len(text) else "")


# --------------------------------------------------------------------------
# Checks

INFORMAL = [
    (r"\bso\b(?!\s+that\b)(?!-called)", "so", "therefore / thus / hence, or restructure with 'Because ...'"),
    (r"\bbut\b", "but", "however / whereas / while / although"),
    (r"\b(?:a lot|lots of|tons of)\b", "a lot", "many / much / the number"),
    (r"\b(?:big|bigger|biggest|huge)\b", "big/huge", "large / substantial / the number"),
    (r"\b(?:get|gets|got|getting|gotten)\b", "get", "obtain / achieve / become / a specific verb"),
    (r"\b(?:really|pretty|basically|actually|quite)\b", "filler", "delete or give the number"),
    (r"\bjust\b", "just", "delete if filler (fine in 'just outside', 'just before')"),
    (r"\blike\b", "like", "such as (fine as a verb)"),
    (r"\b(?:things?|stuff|kind of|sort of)\b", "vague noun", "the specific noun"),
    (r"\b(?:okay|anyway|of course)\b", "colloquial", "delete"),
    (r"\b\w+n['\u2019]t\b|\b(?:it|that|there|here|what|who|let)['\u2019]s\b|\b(?:we|they|you|I)['\u2019](?:re|ve|ll|d|m)\b",
     "contraction", "full form"),
    (r"\badditionally\b", "additionally", "also / in addition"),
    (r"\b(?:in order to)\b", "in order to", "to"),
    (r"\bdue to the fact that\b", "due to the fact that", "because"),
    (r"\butili[sz](?:e|es|ed|ing|ation)\b", "utilize", "use"),
]
INITIAL = re.compile(r"^(?:And|Also|Plus|But|So)\b")
HYPE = [
    (r"\bnovel\b", "novel"), (r"\bsignificant(?:ly)?\b", "significant (only with a statistical test)"),
    (r"\brevolution\w*", "revolutionary"), (r"\bdemocrati[sz]\w*", "democratize"),
    (r"\bbreakthrough\w*", "breakthrough"), (r"\bgroundbreaking\b", "groundbreaking"),
    (r"\bunprecedented\b", "unprecedented"), (r"\bcrucial(?:ly)?\b", "crucial"),
    (r"\bpivotal\b", "pivotal"), (r"\bdelv\w*", "delve"), (r"\bleverag\w*", "leverage"),
    (r"\bseamless\w*", "seamless"), (r"\bcutting-edge\b", "cutting-edge"),
    (r"\bremarkabl\w*", "remarkable"), (r"\bgame-chang\w*", "game-changing"),
    (r"\bstate-of-the-art\b", "state-of-the-art (scope it)"), (r"\b(?:the|is the|are the) first (?:to|work|method|system|approach|paper|study|framework|accelerator|design)\b", "'the first' (scope it: to our knowledge)"),
    (r"\bparadigm shift\b", "paradigm shift"), (r"\bholistic\b", "holistic"), (r"\brobust(?:ly|ness)?\b", "robust (keep if technical)"),
]
VAGUE = re.compile(
    r"\bas (?:mentioned|stated|discussed|noted|described|shown|explained|seen|outlined)\s+"
    r"(?:above|below|before|earlier|previously|later|in the previous section)\b"
    r"|\b(?:see above|see below|aforementioned|above-mentioned)\b", re.I)
HARDCODED = re.compile(
    r"\b(?:Sections?|Sec\.|Figures?|Fig\.|Tables?|Tab\.|Appendix|Appendices|Equations?|Eq\.)\s*"
    r"(?:\(?\d+(?:\.\d+)*[a-z]?\)?|[A-H](?:\.\d+)*)\b")

DRIFT_GROUPS = {
    "data": ["dataset", "data set", "benchmark", "prompt set", "corpus", "corpora", "task suite"],
    "model": ["model", "network", "LM", "architecture"],
    "evaluated subset": ["cohort", "evaluation set", "subset", "split", "test set"],
    "baseline": ["baseline", "reference model", "comparison model"],
    "own contribution": ["method", "approach", "framework", "technique", "pipeline", "procedure"],
    "experiment": ["experiment", "study", "analysis", "test", "evaluation"],
    "metric": ["metric", "measure", "score"],
    "quality": ["accuracy", "correctness", "performance"],
    "run": ["run", "trial", "seed", "repetition"],
}
COMMON_ABBR = {
    "AI", "ML", "NLP", "GPU", "GPUs", "CPU", "CPUs", "TPU", "TPUs", "RAM", "SRAM", "DRAM",
    "API", "APIs", "URL", "PDF", "USA", "UK", "EU", "IEEE", "ACM", "LaTeX", "TeX", "CUDA",
    "FP16", "FP32", "FP8", "BF16", "INT8", "INT4", "II", "III", "IV", "VI", "OK", "MB", "GB",
    "TB", "KB", "kB", "MHz", "GHz", "TOPS", "FLOPs", "FLOPS", "SoC", "MCU", "MCUs", "IoT",
    "PhD", "MSc", "BSc", "NeurIPS", "ICLR", "ICML", "ACL", "EMNLP", "NAACL", "MLSys", "ISCA",
    "OSDI", "SOSP", "CVPR", "AAAI", "IJCAI", "ArXiv", "GitHub", "PyTorch", "TensorFlow", "JAX",
    "BLEU", "ROUGE", "USB", "SSD", "HBM", "CMOS", "RTL", "FPGA", "ASIC", "DSP", "LLM", "LLMs",
}


def check_text(doc, args, out):
    want = lambda c: not args.only or c in args.only
    for par, offsets, locs, region in doc.paragraphs:
        for sent, s0 in sentences(par):
            loc = lambda m: locate(offsets, locs, s0 + m.start())
            if want("informal"):
                for pat, name, fix in INFORMAL:
                    for m in re.finditer(pat, sent, re.I):
                        out["informal"].append((loc(m), f"'{m.group(0)}' ({name}) -> {fix}", snippet(sent, m.start(), m.end())))
                m = INITIAL.match(sent)
                if m:
                    out["informal"].append((loc(m), f"sentence starts with '{m.group(0)}'", snippet(sent, 0, len(m.group(0)))))
            if want("hype"):
                for pat, name in HYPE:
                    for m in re.finditer(pat, sent, re.I):
                        out["hype"].append((loc(m), name, snippet(sent, m.start(), m.end())))
            if want("dashes"):
                for m in re.finditer(r"\u2014|---|(?<=\w)\s+--\s+(?=\w)|\s\u2013\s", sent):
                    out["dashes"].append((loc(m), "dash used as a connector -> comma, colon, period, or parentheses",
                                          snippet(sent, m.start(), m.end())))
            if want("vague-refs"):
                for m in VAGUE.finditer(sent):
                    out["vague-refs"].append((loc(m), f"'{m.group(0)}' -> name the section, equation, figure, or table",
                                              snippet(sent, m.start(), m.end())))
            if want("hardcoded-refs") and doc.tex and doc.labels:
                for m in HARDCODED.finditer(sent):
                    fix = "\\Cref{...}" if doc.has_cleveref else "Section~\\ref{...} / Table~\\ref{...}"
                    out["hardcoded-refs"].append((loc(m), f"hard-coded '{m.group(0)}' -> {fix}", snippet(sent, m.start(), m.end())))
            if want("long"):
                words = re.findall(r"[A-Za-z0-9][\w'\-.%\u00d7]*", sent)
                if len(words) > args.long and region != "abstract" or len(words) > args.long + 10:
                    out["long"].append((locate(offsets, locs, s0), f"{len(words)} words", sent[:160] + ("..." if len(sent) > 160 else "")))


def check_terms(doc, args, out):
    full = " ".join(p[0] for p in doc.paragraphs)
    for group, forms in DRIFT_GROUPS.items():
        counts = {}
        for f in forms:
            flags = 0 if f.isupper() else re.I
            n = len(re.findall(r"\b" + re.escape(f) + r"(?:s|es)?\b", full, flags))
            if n:
                counts[f] = n
        if len(counts) > 1:
            out["terms"].append((None, group, ", ".join(f"{k}: {v}" for k, v in sorted(counts.items(), key=lambda x: -x[1]))))


def check_variants(doc, args, out):
    forms = defaultdict(lambda: defaultdict(int))
    tok = re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:[-\u2010][A-Za-z0-9]+)+\b|\b[A-Za-z]+[A-Z][A-Za-z0-9]*\b|\b[A-Z][a-z]+\b")
    full_parts = []
    for par, _, _, _ in doc.paragraphs:
        for sent, _ in sentences(par):
            full_parts.append(sent)
            for i, m in enumerate(tok.finditer(sent)):
                if m.start() == 0 or sent[:m.start()].strip() in ('"', "(", "'"):
                    continue
                w = m.group(0)
                forms[re.sub(r"[-\u2010]", "", w.lower())][w] += 1
    full = " ".join(full_parts)
    for key, fs in list(forms.items()):
        if any("-" in f or "\u2010" in f for f in fs):
            base = next(f for f in fs if "-" in f or "\u2010" in f)
            parts = re.split(r"[-\u2010]", base)
            spaced = " ".join(parts)
            joined = "".join(parts)
            for variant in (spaced, joined):
                n = len(re.findall(r"\b" + re.escape(variant) + r"\b", full))
                if n and variant not in fs:
                    fs[variant] += n
            for variant in (spaced.lower(), joined.lower()):
                n = len(re.findall(r"\b" + re.escape(variant) + r"\b", full))
                if n and variant not in fs:
                    fs[variant] += n
    for key, fs in sorted(forms.items()):
        if len(fs) < 2:
            continue
        # ignore forms that differ only in the case of the first letter (headings, table rows)
        if len({f[0].lower() + f[1:] for f in fs}) < 2:
            continue
        out["variants"].append((None, key, ", ".join(f"{f}: {n}" for f, n in sorted(fs.items(), key=lambda x: -x[1]))))


def check_abbrev(doc, args, out):
    abbr = re.compile(r"(?<![-\w])[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*s?\b")
    first, defs = {}, defaultdict(list)
    for par, offsets, locs, region in doc.paragraphs:
        if region == "abstract":
            continue
        for m in abbr.finditer(par):
            a = m.group(0)
            core = a[:-1] if a.endswith("s") and a[:-1].isupper() else a
            if core in COMMON_ABBR or a in COMMON_ABBR or len(core) < 2:
                continue
            before = par[max(0, m.start() - 2):m.start()]
            after = par[m.end():m.end() + 2]
            is_def = before.endswith("(") and after.startswith(")")
            if is_def:
                defs[core].append(locate(offsets, locs, m.start()))
            if core not in first:
                first[core] = (locate(offsets, locs, m.start()), is_def, snippet(par, m.start(), m.end()))
    for a, (loc, is_def, snip) in first.items():
        if not is_def and not defs[a]:
            out["abbrev"].append((loc, f"'{a}' never defined as '... ({a})' (fine if it is a name, not an abbreviation)", snip))
        elif not is_def:
            out["abbrev"].append((loc, f"'{a}' used before its definition at {fmt_loc(defs[a][0])}", snip))
        if len(defs[a]) > 1:
            out["abbrev"].append((defs[a][1], f"'{a}' defined again (first at {fmt_loc(defs[a][0])}); say it once", ""))


def check_floats(doc, args, out):
    if not doc.tex:
        return
    for label, (kind, loc) in doc.labels.items():
        kind = kind or ("figure" if label.startswith("fig") else "table" if label.startswith("tab") else None)
        if kind and not doc.refs.get(label):
            out["floats"].append((loc, f"{kind} '{label}' is never referenced in the text", ""))
    for kind, loc in doc.unlabeled_floats:
        out["floats"].append((loc, f"{kind} has no \\label, so the text cannot reference it", ""))
    for key, locs in doc.refs.items():
        if key not in doc.labels:
            out["floats"].append((locs[0], f"reference to undefined label '{key}'", ""))


NUM_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(\\%|%|\\times|\u00d7|x(?![a-zA-Z]))?")


def check_numbers(doc, args, out):
    clean = re.compile(r"\\(?:label|[cC]ref|ref|autoref|eqref|cite[a-zA-Z]*|url|includegraphics|vspace|hspace|"
                       r"setlength|resizebox|scalebox)\*?(?:\[[^\]]*\])*(?:\{[^{}]*\})*")
    by_region = defaultdict(list)
    for region, loc, line in doc.number_lines:
        line = clean.sub(" ", line)
        line = re.sub(r"\[[^\]]*(?:width|height|scale)[^\]]*\]", " ", line)
        for m in NUM_RE.finditer(line):
            val, unit = m.group(1).replace(",", ""), m.group(2)
            if "." not in val and not unit:
                continue
            by_region[region].append((val, loc, line.strip()[:120]))
    for region in ("abstract", "intro", "conclusion"):
        others = {v for r, items in by_region.items() if r not in (region, "abstract") for v, _, _ in items}
        for val, loc, line in by_region.get(region, []):
            if val not in others:
                out["numbers"].append((loc, f"{val} in the {region} does not appear in the body, tables, or appendix", line))


# --------------------------------------------------------------------------

TITLES = {
    "informal": "Informal words and connectives",
    "hype": "Hype and unscoped claims",
    "dashes": "Dashes as connectors",
    "vague-refs": "Vague back-references",
    "hardcoded-refs": "Hard-coded cross-references",
    "long": "Long sentences",
    "terms": "Terminology drift (same concept, several words?)",
    "variants": "Spelling and capitalization variants",
    "abbrev": "Abbreviations",
    "floats": "Figures, tables, and labels",
    "numbers": "Numbers to cross-check",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--only", help="comma-separated list of checks")
    ap.add_argument("--max", type=int, default=40, help="max hits shown per check (0 = all)")
    ap.add_argument("--long", type=int, default=30, help="word count above which a sentence is long")
    args = ap.parse_args()
    args.only = set(args.only.split(",")) if args.only else None

    path, warnings = args.path, []
    if os.path.isdir(path):
        path = find_main(path)
    tex = path.endswith(".tex")
    lines = load_tex(path, os.path.dirname(os.path.abspath(path)), set(), warnings) if tex else load_plain(path)
    doc = Doc(lines, tex)

    out = defaultdict(list)
    check_text(doc, args, out)
    for name, fn in (("terms", check_terms), ("variants", check_variants), ("abbrev", check_abbrev),
                     ("floats", check_floats), ("numbers", check_numbers)):
        if not args.only or name in args.only:
            fn(doc, args, out)

    print(f"# Prose check: {fmt_loc((path, 0)).rsplit(':', 1)[0]}")
    files = sorted({fmt_loc((p, 0)).rsplit(':', 1)[0] for p, _, _ in lines})
    print(f"\nFiles read: {', '.join(files)}")
    if doc.macros:
        expanded = ", ".join("\\" + k + " = " + v for k, v in sorted(doc.macros.items()))
        print("Macros expanded: " + expanded)
    for w in warnings:
        print(f"Warning: {w}")
    total = sum(len(v) for v in out.values())
    print(f"\n{total} candidates. Each is a candidate, not a verdict: judge it in context.\n")
    for key, title in TITLES.items():
        hits = out.get(key, [])
        if not hits:
            continue
        print(f"## {title} ({len(hits)})\n")
        shown = hits if args.max == 0 else hits[:args.max]
        for loc, msg, snip in shown:
            where = f"{fmt_loc(loc)}: " if loc else ""
            print(f"- {where}{msg}" + (f"\n  > {snip}" if snip else ""))
        if len(shown) < len(hits):
            print(f"- ... {len(hits) - len(shown)} more (use --max 0 to show all)")
        print()


if __name__ == "__main__":
    main()
