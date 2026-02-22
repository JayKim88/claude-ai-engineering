#!/usr/bin/env python3
"""Initialize a new Business Avengers project directory structure."""

import os
import sys
import yaml
import json
from datetime import datetime

# --- Config loader ---

def _config_path():
    """Return the path to org-structure.yaml (sibling of this script)."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "org-structure.yaml")


def _load_config():
    """Load org-structure.yaml and return the parsed dict."""
    with open(_config_path()) as f:
        return yaml.safe_load(f)


def get_projects_dir():
    """Resolve the projects directory.

    Priority: BUSINESS_AVENGERS_DIR env var > org-structure.yaml settings > default.
    """
    env = os.environ.get("BUSINESS_AVENGERS_DIR")
    if env:
        return os.path.expanduser(env)

    config = _load_config()
    configured = config.get("settings", {}).get("projects_dir", "~/.business-avengers/projects")
    return os.path.expanduser(configured)


def get_phase_dirs(config=None):
    """Build phase directory names from org-structure.yaml phases.

    Returns a list like ["phase-0-ideation", "phase-1-market-research", ...].
    """
    if config is None:
        config = _load_config()
    phases = config.get("phases", {})
    dirs = []
    for num in sorted(phases.keys()):
        dir_name = phases[num].get("dir_name", f"phase-{num}")
        dirs.append(f"phase-{num}-{dir_name}")
    return dirs


# --- Commands ---

def create_project(project_name: str, project_slug: str, workflow_mode: str = "idea-first"):
    """Create project directory structure and project.yaml."""
    projects_dir = get_projects_dir()
    project_dir = os.path.join(projects_dir, project_slug)

    if os.path.exists(project_dir):
        print(json.dumps({"status": "exists", "path": project_dir}))
        return

    os.makedirs(projects_dir, exist_ok=True)

    # Phase directories from org-structure.yaml
    phase_dirs = get_phase_dirs()

    for phase in phase_dirs:
        phase_dir = os.path.join(project_dir, phase)
        os.makedirs(phase_dir, exist_ok=True)
        os.makedirs(os.path.join(phase_dir, "history"), exist_ok=True)

    # Create sprints directory
    os.makedirs(os.path.join(project_dir, "sprints"), exist_ok=True)

    # Create project.yaml
    now = datetime.now().strftime("%Y-%m-%d")
    project_data = {
        "name": project_name,
        "slug": project_slug,
        "created": now,
        "updated": now,
        "status": "in_progress",
        "current_sprint": 1,
        "workflow_mode": workflow_mode,
        "phases": {
            i: {"status": "pending"} for i in range(13)
        },
        "sprints": {
            1: {"goal": "Initial Setup", "phases": [], "status": "in_progress", "started": now}
        },
        "ceo_decisions": [],
    }

    with open(os.path.join(project_dir, "project.yaml"), "w") as f:
        yaml.dump(project_data, f, default_flow_style=False, allow_unicode=True)

    print(json.dumps({"status": "created", "path": project_dir}))


def load_project(project_slug: str):
    """Load existing project data."""
    project_dir = os.path.join(get_projects_dir(), project_slug)
    yaml_path = os.path.join(project_dir, "project.yaml")

    if not os.path.exists(yaml_path):
        print(json.dumps({"status": "not_found", "slug": project_slug}))
        return

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    print(json.dumps({"status": "loaded", "data": data}, default=str))


def update_phase(project_slug: str, phase_num: int, status: str, version: str = None):
    """Update a phase's status in project.yaml."""
    project_dir = os.path.join(get_projects_dir(), project_slug)
    yaml_path = os.path.join(project_dir, "project.yaml")

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    phase_data = data["phases"].get(phase_num, {})
    phase_data["status"] = status

    if status == "in_progress":
        phase_data["started_at"] = now
    elif status == "completed":
        phase_data["completed_at"] = now

    if version:
        phase_data["version"] = version

    data["phases"][phase_num] = phase_data
    data["updated"] = datetime.now().strftime("%Y-%m-%d")

    with open(yaml_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    print(json.dumps({"status": "updated", "phase": phase_num, "new_status": status}))


def backup_document(project_slug: str, phase_dir_name: str, filename: str, version: str):
    """Backup a document to history/ before updating."""
    project_dir = os.path.join(get_projects_dir(), project_slug)
    phase_dir = os.path.join(project_dir, phase_dir_name)
    source = os.path.join(phase_dir, filename)

    if not os.path.exists(source):
        print(json.dumps({"status": "no_file", "path": source}))
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    name, ext = os.path.splitext(filename)
    backup_name = f"{name}-{version}-{date_str}{ext}"
    dest = os.path.join(phase_dir, "history", backup_name)

    import shutil
    shutil.copy2(source, dest)
    print(json.dumps({"status": "backed_up", "from": source, "to": dest}))


def _normalize_perm(perm):
    """Normalize a permission string for comparison.

    Handles ~ expansion and // absolute path format:
      "Write(~/.business-avengers/**)" → "Write(//Users/jaykim/.business-avengers/**)"
      "Write(/Users/jaykim/...)"       → "Write(//Users/jaykim/...)"  (fix single-slash)
    """
    home = os.path.expanduser("~")
    # Expand ~ to absolute path with // prefix
    if "~" in perm:
        perm = perm.replace("~", "/" + home)  # ~ → //abs/path
    return perm


def check_permissions():
    """Check if required permissions are set in ~/.claude/settings.json.

    Reads required_permissions from org-structure.yaml and verifies they exist
    in the global settings allow list.

    IMPORTANT: Claude Code uses // (double slash) for absolute paths in permissions.
    Single / is relative to the settings file directory. Sub-agents (Task tool) have
    no interactive fallback, so the permission string must match exactly.
    """
    config = _load_config()
    required = config.get("settings", {}).get("required_permissions", [])

    settings_path = os.path.expanduser("~/.claude/settings.json")
    if not os.path.exists(settings_path):
        print(json.dumps({
            "status": "error",
            "message": f"Global settings not found: {settings_path}",
            "missing": required,
            "fix": f"Create {settings_path} with permissions.allow list",
        }))
        return

    with open(settings_path) as f:
        settings = json.load(f)

    allowed = settings.get("permissions", {}).get("allow", [])

    # Normalize all permissions for comparison
    allowed_normalized = [_normalize_perm(p) for p in allowed]

    missing = []
    warnings = []
    for perm in required:
        perm_norm = _normalize_perm(perm)
        found = any(
            p == perm or p == perm_norm
            or perm in p or perm_norm in p
            for p in allowed
        ) or any(
            perm_norm in p_norm or p_norm in perm_norm
            for p_norm in allowed_normalized
        )
        if not found:
            missing.append(perm)
        else:
            # Check for single-slash absolute path (common mistake)
            home = os.path.expanduser("~")
            for p in allowed:
                if home in p and not p.startswith("//") and "(" in p:
                    # Extract the path part inside parentheses
                    path_part = p.split("(", 1)[1].rstrip(")")
                    if path_part.startswith(home) or path_part.startswith("/" + home[1:]):
                        if not path_part.startswith("//"):
                            warnings.append({
                                "permission": p,
                                "issue": "Uses single / for absolute path. Sub-agents need // prefix.",
                                "fix": p.replace(f"({path_part}", f"(/{path_part}") if not path_part.startswith("/") else p.replace(f"(/{home}", f"(//{home}"),
                            })

    result = {"status": "ok", "permissions": required}

    if missing:
        home = os.path.expanduser("~")
        fix_perms = [_normalize_perm(p) for p in missing]
        result = {
            "status": "missing_permissions",
            "missing": missing,
            "settings_path": settings_path,
            "fix": f"Add to {settings_path} permissions.allow: {fix_perms}",
        }

    if warnings:
        result["warnings"] = warnings
        if result["status"] == "ok":
            result["status"] = "warnings"

    print(json.dumps(result, ensure_ascii=False))


def resolve_paths(project_slug: str, phase_num: int):
    """Resolve input/output paths for a phase.

    Returns JSON with:
      - save_dir: absolute path where this phase writes outputs
      - outputs: list of {filename, path} for expected output files
      - inputs: list of {filename, path, exists} from upstream phases
      - phase: metadata (name, lead, agents)
    """
    config = _load_config()
    projects_dir = get_projects_dir()
    project_dir = os.path.join(projects_dir, project_slug)

    phases = config.get("phases", {})
    phase_cfg = phases.get(phase_num)
    if phase_cfg is None:
        print(json.dumps({"status": "error", "message": f"Phase {phase_num} not found in config"}))
        return

    # This phase's save directory
    dir_name = phase_cfg.get("dir_name", f"phase-{phase_num}")
    save_dir = os.path.join(project_dir, f"phase-{phase_num}-{dir_name}")

    # Output files
    output_files = []
    for fname in phase_cfg.get("outputs", []):
        output_files.append({
            "filename": fname,
            "path": os.path.join(save_dir, fname),
        })

    # Input files from upstream phases
    input_files = []
    for upstream_num in phase_cfg.get("inputs_from", []):
        upstream_cfg = phases.get(upstream_num, {})
        upstream_dir_name = upstream_cfg.get("dir_name", f"phase-{upstream_num}")
        upstream_dir = os.path.join(project_dir, f"phase-{upstream_num}-{upstream_dir_name}")
        for fname in upstream_cfg.get("outputs", []):
            fpath = os.path.join(upstream_dir, fname)
            input_files.append({
                "filename": fname,
                "path": fpath,
                "from_phase": upstream_num,
                "exists": os.path.exists(fpath),
            })

    result = {
        "status": "ok",
        "phase": phase_num,
        "name": phase_cfg.get("name"),
        "lead": phase_cfg.get("lead"),
        "agents": phase_cfg.get("agents", []),
        "save_dir": save_dir,
        "outputs": output_files,
        "inputs": input_files,
    }
    print(json.dumps(result, ensure_ascii=False))


def list_projects():
    """List all projects."""
    projects_dir = get_projects_dir()
    if not os.path.exists(projects_dir):
        print(json.dumps({"status": "empty", "projects": []}))
        return

    projects = []
    for slug in os.listdir(projects_dir):
        yaml_path = os.path.join(projects_dir, slug, "project.yaml")
        if os.path.exists(yaml_path):
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            projects.append({
                "slug": slug,
                "name": data.get("name", slug),
                "status": data.get("status", "unknown"),
                "current_sprint": data.get("current_sprint", 0),
                "workflow_mode": data.get("workflow_mode", "idea-first"),
            })

    print(json.dumps({"status": "ok", "projects": projects}))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: init-project.py <command> [args...]")
        print("Commands: create, load, update-phase, backup, list, resolve-paths, check-permissions")
        sys.exit(1)

    command = sys.argv[1]

    if command == "check-permissions":
        check_permissions()

    elif command == "create":
        name = sys.argv[2] if len(sys.argv) > 2 else "Untitled Project"
        slug = sys.argv[3] if len(sys.argv) > 3 else name.lower().replace(" ", "-")
        mode = sys.argv[4] if len(sys.argv) > 4 else "idea-first"
        create_project(name, slug, mode)

    elif command == "load":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "Usage: init-project.py load <slug>"}))
            sys.exit(1)
        slug = sys.argv[2]
        load_project(slug)

    elif command == "update-phase":
        if len(sys.argv) < 5:
            print(json.dumps({"status": "error", "message": "Usage: init-project.py update-phase <slug> <phase> <status> [version]"}))
            sys.exit(1)
        slug = sys.argv[2]
        try:
            phase = int(sys.argv[3])
        except ValueError:
            print(json.dumps({"status": "error", "message": f"Invalid phase number: {sys.argv[3]}"}))
            sys.exit(1)
        status = sys.argv[4]
        version = sys.argv[5] if len(sys.argv) > 5 else None
        update_phase(slug, phase, status, version)

    elif command == "backup":
        if len(sys.argv) < 6:
            print(json.dumps({"status": "error", "message": "Usage: init-project.py backup <slug> <phase_dir> <filename> <version>"}))
            sys.exit(1)
        slug = sys.argv[2]
        phase_dir = sys.argv[3]
        filename = sys.argv[4]
        version = sys.argv[5]
        backup_document(slug, phase_dir, filename, version)

    elif command == "resolve-paths":
        if len(sys.argv) < 4:
            print(json.dumps({"status": "error", "message": "Usage: init-project.py resolve-paths <slug> <phase>"}))
            sys.exit(1)
        slug = sys.argv[2]
        try:
            phase = int(sys.argv[3])
        except ValueError:
            print(json.dumps({"status": "error", "message": f"Invalid phase number: {sys.argv[3]}"}))
            sys.exit(1)
        resolve_paths(slug, phase)

    elif command == "list":
        list_projects()

    else:
        print(json.dumps({"status": "error", "message": f"Unknown command: {command}"}))
        sys.exit(1)
