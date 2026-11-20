const obsidian = require('obsidian');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

const REPO_FOLDER = 'iec-standards-obsidian-vault';

class AskModal extends obsidian.Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
  }

  onOpen() {
    const el = this.contentEl;
    el.createEl('h2', { text: 'Ask the IEC vault' });
    el.createEl('p', {
      text: 'Answers come from tools/agent-loop.py. Out-of-vault questions abstain.',
    });

    const input = el.createEl('textarea', {
      attr: {
        rows: 3,
        placeholder: 'e.g. What is the price of IEC 62443-4-1:2018?',
      },
    });
    input.style.width = '100%';

    const button = el.createEl('button', { text: 'Ask' });
    const output = el.createEl('pre');
    output.style.whiteSpace = 'pre-wrap';

    button.addEventListener('click', async () => {
      const question = input.value.trim();
      if (!question) return;
      button.disabled = true;
      output.textContent = 'Retrieving and judging evidence…';
      try {
        output.textContent = await this.plugin.ask(question);
      } catch (error) {
        output.textContent = 'Error: ' + error.message;
      }
      button.disabled = false;
    });

    input.focus();
  }

  onClose() {
    this.contentEl.empty();
  }
}

class IecVaultAskPlugin extends obsidian.Plugin {
  onload() {
    const base = this.app.vault.adapter.getBasePath
      ? this.app.vault.adapter.getBasePath()
      : '';
    this.repoDir = path.join(base, REPO_FOLDER);

    const open = () => {
      if (!fs.existsSync(path.join(this.repoDir, 'tools', 'agent-loop.py'))) {
        new obsidian.Notice(
          `IEC Vault Ask: repo not found at ${this.repoDir}`
        );
        return;
      }
      new AskModal(this.app, this).open();
    };

    this.addRibbonIcon('message-square', 'Ask IEC vault', open);
    this.addCommand({
      id: 'ask-vault',
      name: 'Ask IEC vault',
      callback: open,
    });
  }

  ask(question) {
    return new Promise((resolve, reject) => {
      execFile(
        'python3',
        [path.join('tools', 'agent-loop.py'), question],
        { cwd: this.repoDir, timeout: 180000, maxBuffer: 1024 * 1024 },
        (error, stdout, stderr) => {
          if (error) {
            reject(new Error(stderr || error.message));
          } else {
            resolve(stdout.trim() || '(no answer produced)');
          }
        }
      );
    });
  }
}

module.exports = IecVaultAskPlugin;
