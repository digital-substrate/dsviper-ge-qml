# Contributing to Graph Editor (dsviper-ge-qml)

Thanks for your interest in contributing.

## Reporting issues

Use [GitHub Issues](https://github.com/digital-substrate/dsviper-ge-qml/issues) and pick the appropriate template (bug report or feature request).

## Submitting pull requests

1. Fork the repository and create a feature branch from `main`
2. Make your changes (see "Running locally" below)
3. Verify the app still launches and the flows you changed still work; if you touched
   `graph_editor/ge/`, run `python3 tests/golden/scenario.py`
4. Open a pull request with a clear description of what changed and why

## Running locally

Requires Python 3.10-3.14 and PySide6 with QML support.

```bash
pip install -r requirements.txt          # PySide6, the dsviper binding and deps
```

Launch the Graph Editor:

```bash
python3 graph_editor.py                           # Launch
python3 graph_editor.py path/to/database.graph    # Open an existing database
```

## Architecture

A QML app built on the shared `dsviper_components_qml/` library (Python models + QML components). `dsviper` provides persistence and commit operations — don't attempt to port Viper.

- `graph_editor/` — the Graph Editor: render canvas, vertex/edge operations, Python editor
- `dsviper_components_qml/` — synced from `dsviper-components-qml` (see the README); don't edit it here

`graph_editor/gei/` is generated from the Graph Editor model as `kibo.toml` declares: don't
edit it by hand, regenerate it (see the README) and commit the result. The business
functions belong in `graph_editor/ge/`.

A change to `graph_editor/ge/` that is meant to change what a function writes needs the
golden file re-recorded, deliberately: `python3 tests/golden/scenario.py --record`, and
the diff of `tests/golden/golden.json` reviewed with the change.

## License

This project is licensed under the MIT License (see [LICENSE](LICENSE)). By submitting a pull request, you agree that your contribution is provided under the same license (inbound = outbound). No CLA is required.
