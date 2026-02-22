#!/usr/bin/env python3
"""Initialize a new Business Avengers project directory structure."""

import os
import sys
import yaml
import json
from datetime import datetime

def create_project(project_name: str, project_slug: str, workflow_mode: str = "idea-first"):
    """Create project directory structure and project.yaml."""
    base_dir = os.path.expanduser("~/.business-avengers")
    project_dir = os.path.join(base_dir, "projects", project_slug)

    if os.path.exists(project_dir):
        print(json.dumps({"status": "exists", "path": project_dir}))
        return

    # Create base directories
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "projects"), exist_ok=True)

    # Phase directories
    phases = [
        "phase-0-ideation",
        "phase-1-market-research",
        "phase-2-product-planning",
        "phase-3-design",
        "phase-4-tech-planning",
        "phase-5-development",
        "phase-6-qa",
        "phase-7-launch",
        "phase-8-monetization",
        "phase-9-operations",
    ]

    for phase in phases:
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
            i: {"status": "pending"} for i in range(10)
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
    project_dir = os.path.expanduser(f"~/.business-avengers/projects/{project_slug}")
    yaml_path = os.path.join(project_dir, "project.yaml")

    if not os.path.exists(yaml_path):
        print(json.dumps({"status": "not_found", "slug": project_slug}))
        return

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    print(json.dumps({"status": "loaded", "data": data}, default=str))


def update_phase(project_slug: str, phase_num: int, status: str, version: str = None):
    """Update a phase's status in project.yaml."""
    project_dir = os.path.expanduser(f"~/.business-avengers/projects/{project_slug}")
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
    project_dir = os.path.expanduser(f"~/.business-avengers/projects/{project_slug}")
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


def list_projects():
    """List all projects."""
    projects_dir = os.path.expanduser("~/.business-avengers/projects")
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
        print("Commands: create, load, update-phase, backup, list")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
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

    elif command == "list":
        list_projects()

    else:
        print(json.dumps({"status": "error", "message": f"Unknown command: {command}"}))
        sys.exit(1)
