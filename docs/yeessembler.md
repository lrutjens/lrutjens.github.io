<div class="md-container" style="padding: 16px;">
  <div class="md-input-wrapper" style="position: relative; margin-bottom: 20px;">
    <textarea id="input"class="md-input md-input--code"placeholder="Enter Yeessembly Code Here"style="resize: none; min-height: 120px; width: 100%; overflow: hidden; box-sizing: border-box;"></textarea>
  </div>
  <button id="assemble-button" class="md-button md-button--primary md-button--raised" style="margin-bottom: 20px;">
    Assemble
  </button>
  <div class="md-output-wrapper" style="margin-top: 20px;">
    <h4 style="margin-bottom: 10px;">Output</h4>
    <pre id="output" class="md-output" style="margin: 0;">
    </pre>
  </div>
</div>
<script>
  const inputArea = document.getElementById('input');
  inputArea.style.height = inputArea.scrollHeight + 'px';

  function initializeAssembler() {
    const OPCODES = {
      'ADD': '1000',
      'SUB': '1001',
      'SUBTRACT': '1001',
      'IF': '1010',
      'MOVE RAM': '1011',
      'MOVE ROM': '1100',
      'MOV RAM': '1011',
      'MOV ROM': '1100',
      'POP': '1101',
      'READ': '1110',
      'WRITE': '1111',
      'WR': '1111',
    };

    const inputArea = document.getElementById('input');
    if (inputArea) {
      inputArea.style.height = inputArea.scrollHeight + 'px';
      inputArea.value = localStorage.getItem('assemblyCode') || '';

      inputArea.addEventListener('input', () => {
        inputArea.style.height = 'auto';
        inputArea.style.height = inputArea.scrollHeight + 'px';

        localStorage.setItem('assemblyCode', inputArea.value);
      });
    }

    const assembleButton = document.getElementById('assemble-button');
    if (assembleButton) {
      assembleButton.addEventListener('click', () => {
        const assemblyCode = inputArea.value;
        const machineCode = assembleCode(assemblyCode);
        document.getElementById('output').innerText = machineCode;
      });
    }

    function assembleCode(assemblyCode) {
      const lines = assemblyCode.split('\n');
      const machineCode = [];
      for (let line of lines) {
        line = line.trim();
        if (!line || line.startsWith(';')) continue;

        let instruction = '';
        if (line.toUpperCase().startsWith('MOVE RAM')) {
          instruction = 'MOVE RAM';
        } else if (line.toUpperCase().startsWith('MOVE ROM')) {
          instruction = 'MOVE ROM';
        } else {
          const parts = line.split(/\s+/);
          instruction = parts[0].toUpperCase();
        }

        if (OPCODES[instruction]) {
          machineCode.push(OPCODES[instruction]);
        } else if (/^\d{4}$/.test(instruction)) {
          machineCode.push(instruction);
        } else {
          machineCode.push(`Error: Unknown instruction "${line}"`);
        }
      }
      return machineCode.join('\n');
    }
  }

  if (window.$docsify) {
    window.$docsify.plugins = (window.$docsify.plugins || []).concat(() => {
      window.addEventListener('navigation.start', initializeAssembler);
    });
  } else {
    document.addEventListener('DOMContentLoaded', initializeAssembler);
    document.addEventListener('DOMContentUpdated', initializeAssembler);
  }
</script>

<style>
  textarea.md-input.md-input--code {
    font-family: monospace;
    font-size: 14px;
    padding: 16px;
    border: 1px solid var(--md-primary-fg-color);
    border-radius: 6px;
    background-color: var(--md-code-bg-color);
    color: var(--md-primary-fg-color);
    line-height: 1.6;
    outline: none;
    transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  }
  textarea.md-input.md-input--code:focus {
    border-color: var(--md-accent-fg-color);
    box-shadow: 0 0 10px var(--md-accent-fg-color);
  }
  .md-output-wrapper {
    margin-top: 20px;
    padding: 12px;
    background-color: var(--md-code-bg-color);
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  pre.md-output {
    padding: 16px;
    background-color: var(--md-code-bg-color);
    border: 1px solid var(--md-primary-fg-color);
    border-radius: 6px;
    color: var(--md-primary-fg-color);
    overflow: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
</style>
