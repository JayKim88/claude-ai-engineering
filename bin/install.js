#!/usr/bin/env node
/**
 * npx installer for claude-ai-engineering
 *
 * Usage:
 *   npx github:jaykim/claude-ai-engineering                  # Install all
 *   npx github:jaykim/claude-ai-engineering learning-summary # Install specific skill
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CLAUDE_DIR = path.join(process.env.HOME, '.claude');
const SOURCE_DIR = path.join(__dirname, '..');

// Parse arguments
const args = process.argv.slice(2);
const specificItem = args[0];

console.log('📦 Claude AI Engineering Toolkit Installer\n');

// Ensure Claude directories exist
if (!fs.existsSync(CLAUDE_DIR)) {
  fs.mkdirSync(CLAUDE_DIR, { recursive: true });
}

const skillsDir = path.join(CLAUDE_DIR, 'skills');
const agentsDir = path.join(CLAUDE_DIR, 'agents');

if (!fs.existsSync(skillsDir)) fs.mkdirSync(skillsDir, { recursive: true });
if (!fs.existsSync(agentsDir)) fs.mkdirSync(agentsDir, { recursive: true });

/**
 * Copy directory recursively
 */
function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * Install a specific skill
 */
function installSkill(name) {
  const src = path.join(SOURCE_DIR, 'skills', name);
  const dest = path.join(skillsDir, name);

  if (!fs.existsSync(src)) {
    console.error(`❌ Error: Skill "${name}" not found`);
    return false;
  }

  // Remove existing
  if (fs.existsSync(dest)) {
    fs.rmSync(dest, { recursive: true, force: true });
  }

  copyDir(src, dest);
  console.log(`✓ Installed skill: ${name}`);
  return true;
}

/**
 * Install a specific agent
 */
function installAgent(name) {
  const src = path.join(SOURCE_DIR, 'agents', name);
  const dest = path.join(agentsDir, name);

  if (!fs.existsSync(src)) {
    console.error(`❌ Error: Agent "${name}" not found`);
    return false;
  }

  // Remove existing
  if (fs.existsSync(dest)) {
    fs.rmSync(dest, { recursive: true, force: true });
  }

  copyDir(src, dest);
  console.log(`✓ Installed agent: ${name}`);
  return true;
}

/**
 * Install all skills and agents
 */
function installAll() {
  let count = 0;

  // Install all skills
  const skillsSource = path.join(SOURCE_DIR, 'skills');
  if (fs.existsSync(skillsSource)) {
    const skills = fs.readdirSync(skillsSource, { withFileTypes: true })
      .filter(entry => entry.isDirectory())
      .map(entry => entry.name);

    for (const skill of skills) {
      if (installSkill(skill)) count++;
    }
  }

  // Install all agents
  const agentsSource = path.join(SOURCE_DIR, 'agents');
  if (fs.existsSync(agentsSource)) {
    const agents = fs.readdirSync(agentsSource, { withFileTypes: true })
      .filter(entry => entry.isDirectory())
      .map(entry => entry.name);

    for (const agent of agents) {
      if (installAgent(agent)) count++;
    }
  }

  return count;
}

/**
 * List available items
 */
function listAvailable() {
  console.log('📋 Available Skills:');
  const skillsSource = path.join(SOURCE_DIR, 'skills');
  if (fs.existsSync(skillsSource)) {
    const skills = fs.readdirSync(skillsSource, { withFileTypes: true })
      .filter(entry => entry.isDirectory())
      .map(entry => entry.name);
    skills.forEach(skill => console.log(`   - ${skill}`));
  }

  console.log('\n📋 Available Agents:');
  const agentsSource = path.join(SOURCE_DIR, 'agents');
  if (fs.existsSync(agentsSource)) {
    const agents = fs.readdirSync(agentsSource, { withFileTypes: true })
      .filter(entry => entry.isDirectory())
      .map(entry => entry.name);
    agents.forEach(agent => console.log(`   - ${agent}`));
  }
}

// Main execution
if (!specificItem || specificItem === '--all') {
  // Install all
  const count = installAll();
  console.log(`\n✅ Successfully installed ${count} items to ${CLAUDE_DIR}`);
} else if (specificItem === '--list') {
  // List available
  listAvailable();
} else {
  // Try to install specific item (check skills first, then agents)
  if (installSkill(specificItem)) {
    console.log(`\n✅ Successfully installed skill: ${specificItem}`);
  } else if (installAgent(specificItem)) {
    console.log(`\n✅ Successfully installed agent: ${specificItem}`);
  } else {
    console.error(`\n❌ Item "${specificItem}" not found`);
    console.log('\nRun with --list to see available items:');
    console.log('  npx github:jaykim/claude-ai-engineering --list');
    process.exit(1);
  }
}

console.log('\n💡 Installation complete! Your skills/agents are ready to use.');
