# fdo-architecture

An overview of the FDOx repository family: which repositories exist, what
each one produces, and what it consumes from another. The relationships live
in one hand-maintained file, `registry.yaml`; everything else is generated
from it.

## What this is

```
registry.yaml (edited by hand)
        │
        ▼
python main.py validate   →  shape errors, dangling references
        │
        ▼
python main.py render     →  dist/architecture.mmd   (Mermaid source, versioned)
                              docs/index.html          (diagram + table, GitHub Pages)
```

`docs/index.html` is a single static file. It loads [Mermaid](https://mermaid.js.org/)
from a CDN and renders the diagram in the browser — no build step runs on the
GitHub Pages side, the same approach the family already uses for
[`fdo-squirrel-spec`](https://github.com/FDOx-squirrel/fdo-squirrel-spec).

## Usage

```
pip install -r requirements.txt
python main.py              # validate, then render
python main.py --list       # show the two steps
python main.py --only render
python main.py --strict     # warnings become errors (what CI runs)
```

Running it twice produces byte-identical output; `git status` stays clean
after the second run.

## Updating the diagram

Edit `registry.yaml`, then run `python main.py`. Never hand-edit
`dist/architecture.mmd` or `docs/index.html` — both are overwritten on the
next run.

## Scope

Only the FDOx family (`fdo-squirrel`, `fdo-squirrel-spec`,
`fdo-squirrel-registry`, `fdo-squirrel-md-generator`, and SquirrelBase as an
external system). See `PRIMER.md` for the decisions behind that scope and for
open questions, including entries not yet verified against the real
repositories.

## License

MIT, see `LICENSE`. Please cite via `CITATION.cff`.
