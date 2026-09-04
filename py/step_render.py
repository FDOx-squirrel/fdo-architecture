"""S1 — render: builds dist/architecture.mmd and docs/index.html from registry.yaml.

Runnable standalone: python py/step_render.py
Both outputs are generated. Do not hand-edit them; edit registry.yaml instead.
"""

from __future__ import annotations

import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import architecture_utils as au  # noqa: E402

UNVERIFIED_MARKERS = ("not verified", "assumed", "unverified")


def _mermaid_id(repo_id: str) -> str:
    """Mermaid-safe node id: registry ids use hyphens, node ids use underscores."""
    return repo_id.replace("-", "_")


def build_mermaid(repos: list[dict]) -> str:
    lines = [
        "flowchart LR",
        "    classDef repo fill:#eef2ff,stroke:#4338ca,color:#1e1b4b;",
        "    classDef external fill:#fef3c7,stroke:#b45309,color:#451a03;",
        "",
    ]

    for repo in repos:
        mid = _mermaid_id(repo["id"])
        if repo.get("org"):
            label = f'{repo["id"]} ({repo["org"]})'
        elif repo["kind"] == "external-system":
            label = f'{repo["id"]} (external system)'
        else:
            label = repo["id"]
        label = label.replace('"', "'")
        if repo["kind"] == "external-system":
            lines.append(f'    {mid}{{{{"{label}"}}}}')
        else:
            lines.append(f'    {mid}["{label}"]')

    lines.append("")

    for repo in repos:
        mid = _mermaid_id(repo["id"])
        for consumed in repo.get("consumes") or []:
            source = consumed.get("from")
            if not source:
                continue
            source_mid = _mermaid_id(source)
            note = (consumed.get("note") or "").lower()
            artifact = consumed.get("artifact") or ""
            edge_label = artifact.split(",")[0].strip().replace('"', "'")
            if len(edge_label) > 40:
                edge_label = edge_label[:37] + "..."
            unverified = any(marker in note for marker in UNVERIFIED_MARKERS)
            if unverified:
                lines.append(f'    {source_mid} -. "{edge_label}" .-> {mid}')
            else:
                lines.append(f'    {source_mid} -- "{edge_label}" --> {mid}')

    lines.append("")
    for repo in repos:
        mid = _mermaid_id(repo["id"])
        css_class = "external" if repo["kind"] == "external-system" else "repo"
        lines.append(f"    class {mid} {css_class};")
        if repo.get("url"):
            lines.append(f'    click {mid} "{repo["url"]}" "_blank"')

    return "\n".join(lines)


def _artifact_list(entries: list[dict], key_from: bool = False) -> str:
    if not entries:
        return "—"
    parts = []
    for e in entries:
        artifact = e.get("artifact", "?")
        fmt = e.get("format")
        piece = f"{artifact} ({fmt})" if fmt else artifact
        if key_from and e.get("from"):
            piece = f"from {e['from']}: {piece}"
        elif key_from:
            piece = f"external: {piece}"
        parts.append(piece)
    return "; ".join(parts)


STATUS_LABELS = {"done": "done", "in-progress": "in progress", "error": "error"}
STATUS_CSS_CLASS = {"done": "status-done", "in-progress": "status-progress", "error": "status-error"}


def _status_badge(level: str | None) -> str:
    """A small coloured pill: done (green), in-progress (amber), error (red).

    Falls back to a neutral grey badge labelled with the raw value if
    registry.yaml carries something step_validate.py did not catch — the
    page should never go blank over an unknown status_level.
    """
    css_class = STATUS_CSS_CLASS.get(level, "status-unknown")
    label = STATUS_LABELS.get(level, level or "unknown")
    return f'<span class="badge {css_class}">{html.escape(label)}</span>'


def build_html(repos: list[dict], mermaid_source: str) -> str:
    rows = []
    for repo in repos:
        rows.append(
            "        <tr>"
            f'<td><a href="{html.escape(repo["url"])}">{html.escape(repo["id"])}</a></td>'
            if repo.get("url")
            else f'        <tr><td>{html.escape(repo["id"])}</td>'
        )
        rows.append(f'          <td>{html.escape(repo.get("org") or "—")}</td>')
        rows.append(f'          <td>{html.escape(repo.get("role", ""))}</td>')
        rows.append(
            f'          <td>{_status_badge(repo.get("status_level"))}<br>'
            f'<span class="status-note">{html.escape(repo.get("status", ""))}</span></td>'
        )
        rows.append(f'          <td>{html.escape(_artifact_list(repo.get("produces") or []))}</td>')
        rows.append(
            f'          <td>{html.escape(_artifact_list(repo.get("consumes") or [], key_from=True))}</td>'
        )
        rows.append("        </tr>")
    table_rows = "\n".join(rows)
    release = au.RELEASE

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>FDOx — Architecture</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; color: #1e1b4b; }}
  h1 {{ margin-bottom: 0.2rem; }}
  .meta {{ color: #555; font-size: 0.9rem; margin-bottom: 2rem; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.9rem; }}
  th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; vertical-align: top; }}
  th {{ background: #eef2ff; }}
  .mermaid {{ margin: 2rem 0; }}
  .badge {{ display: inline-block; padding: 0.1rem 0.6rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }}
  .status-done {{ background: #dcfce7; color: #166534; }}
  .status-progress {{ background: #fef3c7; color: #92400e; }}
  .status-error {{ background: #fee2e2; color: #991b1b; }}
  .status-unknown {{ background: #e5e7eb; color: #374151; }}
  .status-note {{ color: #555; font-size: 0.85rem; }}
  .legend {{ margin: 0.5rem 0 1.5rem; font-size: 0.85rem; color: #555; }}
  .legend .badge {{ margin-right: 0.3rem; }}
  footer {{ margin-top: 2rem; color: #777; font-size: 0.85rem; }}
</style>
</head>
<body>
<h1>FDOx — Architecture</h1>
<p class="meta">Generated from <code>registry.yaml</code> by <code>py/step_render.py</code>. As of {release}.</p>

<pre class="mermaid">
{mermaid_source}
</pre>

<p class="legend">
  <span class="badge status-done">done</span> currently works, nothing blocking —
  <span class="badge status-progress">in progress</span> actively being built —
  <span class="badge status-error">error</span> broken or blocked
</p>

<table>
  <thead>
    <tr><th>Repo</th><th>Org</th><th>Role</th><th>Status</th><th>Produces</th><th>Consumes</th></tr>
  </thead>
  <tbody>
{table_rows}
  </tbody>
</table>

<footer>FDOx-squirrel · <a href="https://github.com/FDOx-squirrel">github.com/FDOx-squirrel</a></footer>

<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({{ startOnLoad: true }});
</script>
</body>
</html>
"""


def run() -> int:
    data = au.load_registry()
    repos = data["repos"]
    au.ensure_dirs()

    mermaid_source = build_mermaid(repos)
    au.write_text(au.MERMAID_PATH, mermaid_source)

    html_source = build_html(repos, mermaid_source)
    au.write_text(au.INDEX_HTML_PATH, html_source)

    print(f"wrote {au.MERMAID_PATH.relative_to(au.ROOT)}")
    print(f"wrote {au.INDEX_HTML_PATH.relative_to(au.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
