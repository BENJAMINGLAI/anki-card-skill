# anki-expert

A Claude Code skill for generating high-quality Anki flashcards from text or local files, with automatic export to `.tsv` or `.apkg` format.

## Features

- **Expert flashcard generation** — follows Anki best practices: minimum information principle, structured HTML formatting, hierarchical tags
- **Multiple input sources** — inline text, `.md`, `.txt`, `.pdf` files
- **Auto export** — `.tsv` (direct Anki import) or `.apkg` (portable deck file)
- **Chinese & English** — full support for CJK content and mixed-language cards
- **Smart formatting** — HTML tags with cost-aware emphasis (bold/italic/highlight)
- **Hierarchical tags** — multi-level `::` separated tags for structured knowledge

## Installation

### As a Claude Code Skill

```bash
# 1. Install the export tool (needed for .tsv / .apkg export)
cd /path/to/this/repo
pip install -e .

# 2. Add this repo as a Claude Code marketplace
claude plugin marketplace add /path/to/this/repo
# or from GitHub:
# claude plugin marketplace add YOUR_USERNAME/newankiskill

# 3. Install the skill plugin
claude plugin install anki-expert
```

### CLI Only (export tool)

```bash
cd /path/to/this/repo
pip install -e .
```

## Usage

### In Claude Code

Tell Claude to create Anki cards from text:

```
Make Anki cards from this text:
{
衰老细胞的特征是细胞内水分减少，导致细胞萎缩，体积变小，代谢减慢。
}
nidd1726052151484
```

Or from a file:

```
Create Anki flashcards from ./notes/lecture-5.md
```

Claude will generate cards following expert rules and automatically export them.

### CLI Export Tool

```bash
# Export to TSV (Anki can import directly)
anki-export cards.txt -f tsv -o output.tsv

# Export to APKG (portable deck file)
anki-export cards.txt -f apkg -o output.apkg -d "My Deck"

# Read from stdin
cat cards.txt | anki-export - -f tsv -o output.tsv
```

## Card Format

Cards use pipe-delimited format with three fields:

```
问题 | 答案 | 标签
------- | -------- | --------
衰老细胞的<b>根本特征</b>？ | 细胞内 <b>水分减少</b>。<br><br>nidd123 | 生物学::细胞衰老
```

### HTML Formatting

Cards use HTML for rich formatting:
- `<b>` bold (low cost) — keywords, item names
- `<i>` italic (medium cost) — English terms, abbreviations
- `<span style="background-color: rgb(255, 255, 0);">` highlight (high cost) — only for the most critical terms
- `<ul>/<ol>` lists — structured answers
- `<code>` — code snippets
- `<br>` — line breaks

### Tags

Hierarchical tags using `::` separator:
```
计算机科学::算法::图论::最短路径::单源最短路径
```

## Publishing

Push this repo to GitHub, then anyone can install with:

```bash
claude plugin marketplace add YOUR_USERNAME/newankiskill
claude plugin install anki-expert
```

To submit to the official Anthropic marketplace, open a PR at [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official).

## License

MIT
