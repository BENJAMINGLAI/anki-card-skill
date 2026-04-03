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
# 1. Install the export tool
pip install anki-skill
# or
uv tool install anki-skill

# 2. Install the skill in Claude Code
claude skill add --from github:YOUR_USERNAME/newankiskill
```

### CLI Only

```bash
pip install anki-skill
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

## Publishing to Skill Registry

To submit this skill to the Claude Code skill registry:

1. Fork and push to your GitHub repository
2. Open an issue or PR at [claude-skill-registry-core](https://github.com/majiayu000/claude-skill-registry-core)
3. Include: skill name, repo URL, description, category (`productivity`)

## License

MIT
