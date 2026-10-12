# Modern High-Performance CLI Tooling Standards

## 1. Core Mandate
When executing shell operations via `run_command` or bash scripts, **never rely on slow legacy GNU built-ins (`grep`, `find`, `cat`) or interactive shell aliases**. Direct invocation of modern, multithreaded, SIMD-accelerated binaries written in Rust/Go is required for maximum execution speed, safety, and token efficiency.

Shell aliases (e.g. `alias grep='rg'`) are **not** expanded in non-interactive subshells; you must invoke the modern binary explicitly.

---

## 2. Binary Replacement Matrix

| Legacy Built-in | Modern Binary | Why It Is Mandatory | Non-Interactive Flags & Syntax |
| :--- | :--- | :--- | :--- |
| **`grep`** | **`rg`** *(ripgrep)* | AVX2/NEON SIMD scanning (`memchr`), multithreaded directory crawling, skips ignored/binary files by default. | `rg --color=never --no-heading -n --smart-case --max-columns=500 "$PATTERN" "$PATH"`<br>• Use `-H` / `--hidden` for dotfiles.<br>• Use `-u` / `-uu` to search ignored/untracked files. |
| **`find`** | **`fd`** *(fd-find)* | Parallel work-stealing tree traversal (`rayon`), 5x–10x faster than POSIX `find`, intuitive regex/glob syntax. | `fd --color=never -H -I --type f "$PATTERN" "$PATH"`<br>• `-H`: Include hidden files.<br>• `-I`: Bypass `.gitignore` when scanning entire projects.<br>• `-0`: Null-delimiter for pipeline safety. |
| **`cat`** | **`bat`** | Memory-mapped I/O, syntax awareness, line slicing without `head`/`tail`/`sed` pipelines. | `bat -pp --color=never "$FILE"`<br>• **CRITICAL:** Always use `-pp` (`--style=plain --paging=never`) to prevent terminal hangs.<br>• Use `-r 1:50` (`--line-range`) for targeted slices. |
| **`ls`** | **`eza`** / **`fd -d 1`** | Batched metadata queries, Git annotations. When `eza`/`lsd` is absent, **strictly use `fd -d 1 -l` (or `fd -d 1 -l -H` for hidden files)** instead of legacy `ls`. | `eza -1 -a --no-quotes --color=never --icons=never "$PATH"`<br>*(If absent: `fd -d 1 -l -H . "$PATH"`)* |
| **`sed`** | **`sd`** | PCRE regex, no slash escaping, cross-platform atomic writes without `.bak` artifacts. | `sd -s "$FIND" "$REPLACE" "$FILE"` (for literal strings)<br>`sd "$REGEX" "$REPLACE" "$FILE"` |
| **`ps`** | **`procs`** | Multithreaded procfs parsing, Docker/cgroup detection, native JSON. Fallback to `ps aux`. | `procs --color=never --pager=disable "$QUERY"` |
| **`du`** | **`dust`** | Parallel recursive traversal with descending size hierarchy. Fallback to `du -sh`. | `dust -c -b -d 2 "$PATH"` |
| **`df`** | **`duf`** | Excludes virtual/loop devices, structured JSON output. Fallback to `df -h`. | `duf --style=plain "$PATH"` |

---

## 3. Automation & Subshell Safety Guidelines

1. **Pager Hang Prevention:**
   - Binaries such as `bat`, `procs`, and `delta` will hang waiting for user keypresses if a pager (`less`) is invoked.
   - Always supply non-paging flags (e.g. `bat -pp`, `procs --pager=disable`) and execute commands with `PAGER=cat`.

2. **Strip ANSI Escape Sequences:**
   - Terminal color sequences pollute token contexts and break string matching. Always include `--color=never` or ensure `NO_COLOR=1`.

3. **Handle Exit Codes Gracefully:**
   - `rg` and `grep` return exit status `1` when no pattern matches are found. In scripts with `set -e`, append `|| true` when a zero-match result is an expected condition.

4. **Graceful Fallbacks:**
   - If operating in an environment where a modern tool is not yet installed, check presence with `command -v <tool>` before falling back to the standard POSIX utility.
