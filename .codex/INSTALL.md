# Installing anki-expert for Codex

## Prerequisites

- Git
- Python 3.10+ (for the `anki-export` CLI tool)

## Installation

1. **Install the export tool:**
   ```bash
   pip install git+https://github.com/gong1414/anki-card-skill.git
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/gong1414/anki-card-skill.git ~/.codex/anki-expert
   ```

3. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/anki-expert/anki-expert ~/.agents/skills/anki-expert
   ```

4. **Restart Codex** to discover the skill.

## Verify

```bash
ls -la ~/.agents/skills/anki-expert
```

You should see a symlink pointing to the anki-expert skill directory.

## Updating

```bash
cd ~/.codex/anki-expert && git pull
```

## Uninstalling

```bash
rm ~/.agents/skills/anki-expert
rm -rf ~/.codex/anki-expert
```
