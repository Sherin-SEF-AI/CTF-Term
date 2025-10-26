# CTF Terminal 🚩

**ctf-term** - A production-ready, cross-platform terminal CTF engine with both CLI and TUI interfaces. Features local SQLite storage, importable challenge packs (YAML), salted-hash flag verification, hint penalties, and live leaderboards.

**Created by:** [Sherin Joseph Roy](https://sherinjosephroy.link) • Co-Founder & Head of Products at [DeepMost AI](https://deepmost.ai)

## Features

- 🎯 **Clean CLI** with all essential CTF commands
- 🖥️ **Beautiful TUI** built with Textual for keyboard-first navigation
- 🔒 **Secure** flag verification using SHA256 salted hashes
- 📦 **Pack System** - import challenges from YAML files
- 🏆 **Advanced Leaderboard** with hint penalties and first blood bonuses
- 🩸 **First Blood** - 10% bonus points for being the first solver
- 💾 **Local Storage** - SQLite database with proper indexes
- 🎨 **Rich Output** - beautiful terminal tables and formatting
- 🌗 **Themes** - dark and light modes (TUI)
- ⚡ **Fast** - optimized for low-end machines
- 🧪 **Tested** - comprehensive test suite
- 📊 **Challenge Stats** - tracking solves, hints, and performance

## Quick Start

### Installation

```bash
pipx install ctf-term
```

Or from source:

```bash
git clone <repo>
cd ctf-term
pipx install .
```

### CLI Usage

```bash
# Initialize the app
ctf init

# Import a challenge pack
ctf import-pack ~/.ctf/packs/sample.yml

# List challenges
ctf list
ctf list --category crypto

# Show challenge details
ctf show rot13-hello

# Get a hint (view-only, no penalty yet)
ctf hint alice rot13-hello

# Submit a flag
ctf submit alice rot13-hello flag{flap}

# View leaderboard
ctf scoreboard

# Generate flag hash for pack authors
ctf make-flag-hash "flag{example}" "salt"
```

### TUI Usage

```bash
# Launch the interactive TUI
ctf tui
```

**Keyboard Shortcuts:**
- `?` / `F1` - Help
- `/` - Search challenges
- `c` - Filter by category
- `u` - Switch/create user
- `Enter` - Open challenge
- `s` - Submit flag
- `h` - Show hint
- `g` - Go to scoreboard
- `t` - Toggle theme
- `Esc` - Go back / Close dialogs
- `q` - Quit

## Pack Authoring

### YAML Schema

```yaml
pack: My CTF Pack
version: 1
challenges:
  - id: unique-challenge-id
    title: Challenge Title
    category: crypto  # crypto, pwn, web, forensics, misc
    description: |
      This is the challenge description.
      Can be multi-line markdown.
    points: 100
    salt: "unique-salt-per-challenge"
    flag_hash: "sha256(salt:flag)"
    hint: "Optional hint text"
    hint_penalty: 20
```

### Creating Flag Hashes

```bash
# Method 1: Use the CLI tool
ctf make-flag-hash "flag{my_flag}" "my_salt"

# Method 2: Manual calculation
python3 -c "import hashlib; print(hashlib.sha256(b'my_salt:flag{my_flag}').hexdigest())"
```

### Development Mode

For local testing, you can use `flag_plain` which will be automatically hashed:

```yaml
challenges:
  - id: test-challenge
    title: Test Challenge
    category: misc
    description: "Test description"
    points: 50
    salt: "s1"
    flag_plain: "flag{test}"  # Dev only - never commit this!
    hint: "This is a hint"
    hint_penalty: 10
```

**⚠️ Warning:** Never commit packs with `flag_plain` to version control!

## Project Structure

```
ctf-term/
├── src/ctfterm/
│   ├── __init__.py
│   ├── cli.py              # CLI commands
│   ├── db.py               # Database operations
│   ├── model.py            # Data models
│   ├── packs.py            # Pack import/export
│   ├── security.py         # Flag verification
│   ├── paths.py            # Path resolution
│   ├── settings.py         # Settings management
│   ├── __main__.py         # Python module entrypoint
│   ├── tui/                # TUI implementation
│   │   ├── app.py
│   │   ├── router.py
│   │   ├── styles.tcss
│   │   ├── views/
│   │   └── widgets/
│   └── services/           # Business logic
│       ├── challenges.py
│       ├── users.py
│       ├── scoreboard.py
│       └── flags.py
├── tests/                  # Test suite
├── examples/               # Sample packs
└── pyproject.toml
```

## Security

- Flags are never stored in plaintext
- Verification uses `SHA256(salt:flag)` only
- Database stores `salt` and `flag_hash`
- No network calls - completely offline
- No dynamic code execution

## Development

### Setup

```bash
git clone <repo>
cd ctf-term
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=src/ctfterm --cov-report=html
```

### Code Formatting

```bash
ruff check src/ tests/
black src/ tests/
```

## Author & Credits

### Sherin Joseph Roy
**Co-Founder & Head of Products** at [DeepMost AI](https://deepmost.ai)

Sherin is an AI entrepreneur and product leader specializing in enterprise AI systems that connect data, automation, and intelligence. With expertise in scalable, human-centered AI solutions, he focuses on bridging research and application to solve real-world challenges.

#### Connect & Learn More
- 🌐 **Portfolio**: [sherinjosephroy.link](https://sherinjosephroy.link)
- 💼 **LinkedIn**: [linkedin.com/in/sherin-roy-deepmost](https://www.linkedin.com/in/sherin-roy-deepmost)
- 🐦 **X (Twitter)**: [@SherinSEF](https://x.com/SherinSEF)
- 🐘 **Mastodon**: [@sherinjoesphroy](https://mastodon.social/@sherinjoesphroy)
- 💻 **GitHub**: [github.com/Sherin-SEF-AI](https://github.com/Sherin-SEF-AI)
- 📧 **Contact**: [sherinjosephroy.link/contact](https://sherinjosephroy.link/contact)

#### About DeepMost AI
DeepMost AI builds enterprise AI systems that help organizations think, decide, and grow through intelligent automation and data-driven solutions.

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Textual](https://textual.textualize.io/) - TUI framework
- [PyYAML](https://pyyaml.org/) - YAML parsing

