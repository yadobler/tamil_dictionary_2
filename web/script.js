document.getElementById("searchBox").addEventListener("input", async (e) => {
  const query = e.target.value.trim();
  if (query.length === 0) return;

  const results = await eel.search_query(query)();
  renderResults(results);
});

document.getElementById("toggleTheme").addEventListener("click", () => {
  document.body.classList.toggle("night");
});

let resultElements = [];
let currentIndex = -1;

function renderResults(results) {
  const container = document.getElementById("results");
  container.innerHTML = "";
  resultElements = [];
  currentIndex = -1;

  results.forEach((entry) => {
    const div = document.createElement("div");
    div.className = "result-item";
    div.tabIndex = 0;
    div.innerHTML = `
      <div class="result-headword">${entry.headword}</div>
      <div class="result-translit">${entry.transliteration || ""}</div>
      <div class="result-preview">${entry.definition.slice(0, 120)}...</div>
    `;
    div.onclick = () => showDefinition(entry);
    container.appendChild(div);
    resultElements.push({ el: div, entry });
  });
}

function showDefinition(entry) {
  document.getElementById("definitionContent").innerHTML = `
    <div class="result-headword">${entry.headword}</div>
    <div class="result-translit">${entry.transliteration || ""}</div>
    <div class="result-preview">${entry.definition}</div>
  `;
}

document.addEventListener("keydown", (e) => {
  if (resultElements.length === 0) return;

  if (e.key === "ArrowDown") {
    e.preventDefault();
    currentIndex = (currentIndex + 1) % resultElements.length;
    updateHighlight();
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    currentIndex = (currentIndex - 1 + resultElements.length) % resultElements.length;
    updateHighlight();
  } else if (e.key === "Enter") {
    if (currentIndex >= 0) {
      resultElements[currentIndex].el.click();
    }
  } else if (e.key === "Escape") {
    currentIndex = -1;
    updateHighlight();
    document.getElementById("searchBox").focus();
  }
});

function updateHighlight() {
  resultElements.forEach(({ el }, i) => {
    el.style.backgroundColor = i === currentIndex ? "#b3d4fc" : "";
  });

  const selected = resultElements[currentIndex]?.el;
  if (selected) {
    const container = document.getElementById("results");
    const containerTop = container.scrollTop;
    const containerBottom = containerTop + container.clientHeight;

    const elementTop = selected.offsetTop;
    const elementBottom = elementTop + selected.offsetHeight;

    if (elementTop < containerTop) {
      container.scrollTop = elementTop;
    } else if (elementBottom > containerBottom) {
      container.scrollTop = elementBottom - container.clientHeight;
    }
  }
}

