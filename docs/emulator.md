---
title: "Yessembly Emulator"
---

###### Version 1.0

<div class="md-container" style="padding: 16px;">
    <h1>Yessembly Emulator</h1>
    <div class="md-output-wrapper" style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 10px;">
        <div class="md-input-wrapper" style="flex: 1;">
            <textarea id="input" class="md-input md-input--code" placeholder="Enter assembly code here..." style="resize: none; min-height: 270px; width: 100%; overflow: hidden; box-sizing: border-box; padding-bottom: 20px;"></textarea>
        </div>

        <div class="controls" style="display: flex; flex-direction: column; gap: 12px;">
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;">
                <button id="start" class="md-button md-button--primary md-button--raised">Start</button>
                <button id="step" class="md-button md-button--primary md-button--raised">Step</button>
                <button id="stop" class="md-button md-button--primary md-button--raised">Stop</button>
                <button id="reset" class="md-button md-button--secondary md-button--raised">Reset</button>
            </div>

            <button id="load" class="md-button md-button--secondary md-button--raised" style="width: 100%;">Load Program</button>

            <div style="width: 100%; margin-top: 8px;">
                <label for="speed-slider" style="display: block; font-weight: bold; text-align: center;">Emulation Speed (ms per step)</label>
                <input id="speed-slider" type="range" min="10" max="2000" step="10" value="1000" style="width: 100%; accent-color: var(--md-primary-fg-color);">
                <span id="speed-value" style="display: block; text-align: right;">1000 ms</span>
            </div>
        </div>
    </div>

    <div class="md-output-wrapper" style="display: flex; gap: 20px; margin-top: 4px;">
        <div>
            <h2 style="margin-top: 8px; margin-left: 8px;">RAM</h2>
            <div id="ram" class="table" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;"></div>
        </div>
        <div>
            <h2 style="margin-top: 8px;">ROM</h2>
            <div id="rom" class="table" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;"></div>
        </div>
    </div>

    <div class="md-output-wrapper" style="margin-top: 16px;">
        <h2>Stack</h2>
        <div id="stack" class="table" style="display: flex; gap: 8px; flex-wrap: wrap;"></div>
    </div>
</div>

<script>
    const ramSize = 16;
      const romSize = 16;
    
      let ram = Array(ramSize).fill("0000");
      let rom = Array(romSize).fill("0000");
      let stack = [];
      let romPointer = 0;
      let ramPointer = 0;
      let intervalId = null;
      let speed = 1000;
    
      const inputArea = document.getElementById('input');
      const speedSlider = document.getElementById('speed-slider');
      const speedValue = document.getElementById('speed-value');
    
      const resizeTextarea = () => {
        inputArea.style.height = 'auto';
        inputArea.style.height = Math.max(inputArea.scrollHeight, 120) + 'px'; 
      };
    
      inputArea.value = localStorage.getItem('assemblyCode') || '';
      resizeTextarea();
    
      inputArea.addEventListener('input', () => {
        resizeTextarea();
        localStorage.setItem('assemblyCode', inputArea.value);
      });
    
      window.addEventListener('resize', resizeTextarea);
    
      const updateSpeedDisplay = () => {
        speedSlider.value = speed;
        speedValue.textContent = `${speed} ms`;
      };
    
      window.addEventListener('load', () => {
        updateSpeedDisplay();
      });
    
      const updateDisplay = () => {
        const ramDiv = document.getElementById("ram");
        const romDiv = document.getElementById("rom");
        const stackDiv = document.getElementById("stack");
    
        ramDiv.innerHTML = "";
        romDiv.innerHTML = "";
        stackDiv.innerHTML = "";
    
        ram.forEach((cell, i) => {
          const cellDiv = document.createElement("div");
          cellDiv.className = "cell";
          cellDiv.textContent = cell;
          if (i === ramPointer) cellDiv.classList.add("highlight");
          ramDiv.appendChild(cellDiv);
        });
    
        rom.forEach((cell, i) => {
          const cellDiv = document.createElement("div");
          cellDiv.className = "cell";
          cellDiv.textContent = cell;
          if (i === romPointer) cellDiv.classList.add("highlight");
          romDiv.appendChild(cellDiv);
        });
    
        stack.forEach((value, i) => {
          const cellDiv = document.createElement("div");
          cellDiv.className = "cell";
          cellDiv.textContent = value;
          if (i === stack.length - 1) cellDiv.classList.add("highlight");
          stackDiv.appendChild(cellDiv);
        });
      };
    
      const executeInstruction = (instruction) => {
        switch (instruction) {
          case "1000":
            if (stack.length < 2) stack.push("0000");
            const addResult = (parseInt(stack.pop(), 2) + parseInt(stack.pop(), 2)).toString(2).padStart(4, "0");
            stack.push(addResult);
            break;
          case "1001":
            if (stack.length < 2) stack.push("0000");
            const subResult = (parseInt(stack.pop(stack.length-2), 2) - parseInt(stack.pop(stack.length-1), 2)).toString(2).padStart(4, "0");
            stack.push(subResult);
            if (subResult.includes("-")) {
              stack.pop();
              alert("Subtraction caused a negative number");
              stop();
            }
            break;
          case "1010":
            if (stack.length < 3) stack.push("0000");
            const condition = stack.pop();
            const compare = stack.pop();
            const newPointer = stack.pop();
            if (parseInt(condition, 2) > parseInt(compare, 2)) {
              romPointer = parseInt(newPointer, 2) - 1;
            }
            break;
          case "1011":
            ramPointer = parseInt(stack[stack.length-1] || "0", 2);
            break;
          case "1100":
            romPointer = parseInt(stack[stack.length-1] || "0", 2) - 1;
            break;
          case "1101":
            stack.pop();
            break;
          case "1110":
            stack.push(ram[ramPointer]);
            break;
          case "1111":
            ram[ramPointer] = stack.pop() || "0000";
            break;
          default:
            stack.push(instruction);
            break;
        }
      };
    
      const step = () => {
        if (romPointer >= romSize) {
          romPointer -= 1;
          updateDisplay();
          stop();
          return;
        }
        const instruction = rom[romPointer];
        executeInstruction(instruction);
        romPointer++;
        updateDisplay();
      };
    
      const start = () => {
        if (intervalId) return;
        intervalId = setInterval(step, speed);
      };
    
      const stop = () => {
        clearInterval(intervalId);
        intervalId = null;
      };
    
      const reset = () => {
        ram = Array(ramSize).fill("0000");
        rom = Array(romSize).fill("0000");
        stack = [];
        romPointer = 0;
        ramPointer = 0;
        stop();
        updateDisplay();
      };
    
      const loadProgram = () => {
        const program = document.getElementById("input").value.split("\n").map(line => line.trim());
        for (let i = 0; i < romSize && i < program.length; i++) {
          rom[i] = program[i] || "0000";
        }
        updateDisplay();
      };
    
      const updateSpeed = (newSpeed) => {
        speed = newSpeed;
        updateSpeedDisplay();
        if (intervalId) {
          stop();
          start();
        }
      };
    
      document.getElementById("speed-slider").addEventListener("input", (event) => updateSpeed(event.target.value));
      document.getElementById("step").addEventListener("click", step);
      document.getElementById("start").addEventListener("click", start);
      document.getElementById("stop").addEventListener("click", stop);
      document.getElementById("reset").addEventListener("click", reset);
      document.getElementById("load").addEventListener("click", loadProgram);
    
      updateDisplay();
</script>

<style>
    .cell {
        padding: 8px;
        border: 1px solid var(--md-primary-fg-color);
        text-align: center;
        border-radius: 4px;
        font-family: monospace;
      }
    
      .highlight {
        background-color: var(--md-accent-bg-color);
        color: var(--md-accent-fg-color);
      }
    
      .table {
        background-color: var(--md-code-bg-color);
        padding: 8px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
    
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
        margin-top: 12px;
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