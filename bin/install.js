#!/usr/bin/env node
/**
 * npx installer for claude-ai-engineering
 *
 * Usage:
 *   npx github:jaykim/claude-ai-engineering                    # Install all plugins
 *   npx github:jaykim/claude-ai-engineering learning-summary   # Install specific plugin
 *   npx github:jaykim/claude-ai-engineering --list             # List available plugins
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CLAUDE_DIR = path.join(process.env.HOME, '.claude');
const SOURCE_DIR = path.join(__dirname, '..');

// Parse arguments
const args = process.argv.slice(2);
const specificPlugin = args[0];

console.log('📦 Claude AI Engineering Toolkit Installer\n');

// Ensure Claude directories exist
if (!fs.existsSync(CLAUDE_DIR)) {
  fs.mkdirSync(CLAUDE_DIR, { recursive: true });
}

const skillsDir = path.join(CLAUDE_DIR, 'skills');
const agentsDir = path.join(CLAUDE_DIR, 'agents');
const commandsDir = path.join(CLAUDE_DIR, 'commands');

if (!fs.existsSync(skillsDir)) fs.mkdirSync(skillsDir, { recursive: true });
if (!fs.existsSync(agentsDir)) fs.mkdirSync(agentsDir, { recursive: true });
if (!fs.existsSync(commandsDir)) fs.mkdirSync(commandsDir, { recursive: true });

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
 * Install a specific plugin
 */
function installPlugin(name) {
  const pluginPath = path.join(SOURCE_DIR, 'plugins', name);

  if (!fs.existsSync(pluginPath)) {
    console.error(`❌ Error: Plugin "${name}" not found`);
    return false;
  }

  let itemsInstalled = 0;

  // Install skills from this plugin
  const skillsPath = path.join(pluginPath, 'skills');
  if (fs.existsSync(skillsPath)) {
    const skills = fs.readdirSync(skillsPath, { withFileTypes: true })
      .filter(entry => entry.isDirectory())
      .map(entry => entry.name);

    for (const skill of skills) {
      const src = path.join(skillsPath, skill);
      const dest = path.join(skillsDir, skill);

      // Remove existing
      if (fs.existsSync(dest)) {
        fs.rmSync(dest, { recursive: true, force: true });
      }

      copyDir(src, dest);
      console.log(`  ✓ Installed skill: ${skill}`);
      itemsInstalled++;
    }
  }

  // Install agents from this plugin
  const agentsPath = path.join(pluginPath, 'agents');
  if (fs.existsSync(agentsPath)) {
    const agents = fs.readdirSync(agentsPath)
      .filter(file => file.endsWith('.md'));

    for (const agent of agents) {
      const src = path.join(agentsPath, agent);
      const dest = path.join(agentsDir, agent);

      // Remove existing
      if (fs.existsSync(dest)) {
        fs.rmSync(dest, { force: true });
      }

      fs.copyFileSync(src, dest);
      console.log(`  ✓ Installed agent: ${agent}`);
      itemsInstalled++;
    }
  }

  // Install commands from this plugin
  const commandsPath = path.join(pluginPath, 'commands');
  if (fs.existsSync(commandsPath)) {
    const commands = fs.readdirSync(commandsPath, { withFileTypes: true })
      .filter(entry => entry.isDirectory())
      .map(entry => entry.name);

    for (const command of commands) {
      const src = path.join(commandsPath, command);
      const dest = path.join(commandsDir, command);

      // Remove existing
      if (fs.existsSync(dest)) {
        fs.rmSync(dest, { recursive: true, force: true });
      }

      copyDir(src, dest);
      console.log(`  ✓ Installed command: ${command}`);
      itemsInstalled++;
    }
  }

  return itemsInstalled > 0;
}

/**
 * Install all plugins
 */
function installAll() {
  const pluginsPath = path.join(SOURCE_DIR, 'plugins');

  if (!fs.existsSync(pluginsPath)) {
    console.error('❌ Error: No plugins directory found');
    return 0;
  }

  const plugins = fs.readdirSync(pluginsPath, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name);

  let totalInstalled = 0;

  for (const plugin of plugins) {
    console.log(`📦 Plugin: ${plugin}`);
    const count = installPlugin(plugin);
    if (count) {
      totalInstalled++;
      console.log('');
    }
  }

  return totalInstalled;
}

/**
 * List available plugins
 */
function listAvailable() {
  const pluginsPath = path.join(SOURCE_DIR, 'plugins');

  if (!fs.existsSync(pluginsPath)) {
    console.error('❌ Error: No plugins directory found');
    return;
  }

  const plugins = fs.readdirSync(pluginsPath, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name);

  console.log('📋 Available Plugins:\n');

  for (const plugin of plugins) {
    const pluginJsonPath = path.join(pluginsPath, plugin, '.claude-plugin', 'plugin.json');

    if (fs.existsSync(pluginJsonPath)) {
      const pluginInfo = JSON.parse(fs.readFileSync(pluginJsonPath, 'utf8'));
      console.log(`   ${plugin}`);
      console.log(`      ${pluginInfo.description || 'No description'}`);
      console.log('');
    } else {
      console.log(`   ${plugin}`);
      console.log('');
    }
  }

  console.log('Usage:');
  console.log('   npx github:jaykim/claude-ai-engineering <plugin-name>');
}

// Main execution
if (!specificPlugin || specificPlugin === '--all') {
  // Install all
  const count = installAll();
  console.log(`✅ Successfully installed ${count} plugins to ${CLAUDE_DIR}`);
} else if (specificPlugin === '--list') {
  // List available
  listAvailable();
} else {
  // Install specific plugin
  console.log(`📦 Plugin: ${specificPlugin}`);
  const success = installPlugin(specificPlugin);

  if (success) {
    console.log(`\n✅ Successfully installed plugin: ${specificPlugin}`);
  } else {
    console.error(`\n❌ Plugin "${specificPlugin}" not found`);
    console.log('\nRun with --list to see available plugins:');
    console.log('  npx github:jaykim/claude-ai-engineering --list');
    process.exit(1);
  }
}

console.log('\n💡 Installation complete! Your plugins are ready to use.');
