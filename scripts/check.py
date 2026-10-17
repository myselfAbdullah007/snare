#!/usr/bin/env python3
"""Validate the plugin manifests, skill frontmatter, and command file.

A malformed plugin.json breaks /plugin install silently, so this runs in CI.
ponytail: stdlib only — no jsonschema, no pyyaml (the badge says deps-0).
"""
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
fail = []


def check(cond, msg):
    if not cond:
        fail.append(msg)


# manifests parse, and declare the fields the marketplace reads
plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
for key in ("name", "version", "description", "author"):
    check(key in plugin, f"plugin.json missing {key!r}")
check(
    re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")) is not None,
    f"plugin.json version is not semver: {plugin.get('version')!r}",
)
check(
    any(p["name"] == plugin["name"] for p in market["plugins"]),
    f"marketplace.json lists no plugin named {plugin['name']!r}",
)

# skill: frontmatter delimited, name matches its directory, description present
skill_path = ROOT / "skills" / plugin["name"] / "SKILL.md"
check(skill_path.exists(), f"missing {skill_path.relative_to(ROOT)}")
if skill_path.exists():
    body = skill_path.read_text()
    fm = re.match(r"^---\n(.*?)\n---\n", body, re.S)
    check(fm is not None, "SKILL.md has no --- frontmatter block")
    if fm:
        check(
            re.search(rf"^name:\s*{plugin['name']}\s*$", fm.group(1), re.M) is not None,
            f"SKILL.md name does not match plugin name {plugin['name']!r}",
        )
        check("description:" in fm.group(1), "SKILL.md frontmatter has no description")
        check(len(body) - len(fm.group(0)) > 200, "SKILL.md body is suspiciously short")

# command file parses and carries a non-trivial prompt
cmd = tomllib.loads((ROOT / "commands" / f"{plugin['name']}.toml").read_text())
check("description" in cmd, "command toml missing description")
check(len(cmd.get("prompt", "")) > 200, "command toml prompt is missing or too short")

# every local link in the README resolves
readme = (ROOT / "README.md").read_text()
for target in re.findall(r"\]\((?!https?:|#)([^)\s]+)\)", readme):
    check((ROOT / target).exists(), f"README links to missing path: {target}")

for msg in fail:
    print(f"FAIL: {msg}")
print(f"{'FAILED' if fail else 'OK'} — {len(fail)} problem(s)")
sys.exit(1 if fail else 0)
