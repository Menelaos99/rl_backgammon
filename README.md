# RL Backgammon

> **Status: work in progress — training agents still to be implemented.**

A lightweight, pure‑Python playground for experimenting with reinforcement‑learning (RL) techniques on the classic board game **Backgammon**.

Current capabilities

* Python game environment with board logic and legal‑move generation (see `utils/`).
* Command‑line interface for self‑play roll‑outs or debugging (see `main.py`).

Planned features

* ✨ Neural‑network agents (TD‑Gammon‑style, self‑play, tree search).
* 📈 Training scripts & evaluation dashboards.
* 🏆 Pre‑trained checkpoints.

---

## Quick start

```bash
git clone https://github.com/Menelaos99/rl_backgammon.git
cd rl_backgammon
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   
python main.py --help
```

### Play one random game

```bash
python main.py 
```

---

## Repository structure

```
rl_backgammon/
├── utils/            # Board representation, legal moves, helpers
│   ├── board.py
│   ├── game.py
│   └── ...
├── main.py           # Entry‑point CLI
└── tests/            # (coming soon)
```

---

## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes and remember to add/ update tests.

## License

[MIT](LICENSE)
