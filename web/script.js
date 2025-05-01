// Store grouped results and the corresponding DOM elements
let resultElements = [];
let currentIndex = -1;

document.getElementById("searchBox").addEventListener("input", async (e) => {
    const query = e.target.value.trim();
    if (query.length === 0) {
        // Optionally clear results or show a default state when input is empty
        document.getElementById("results").innerHTML = "";
        document.getElementById("definitionContent").innerHTML = "";
        resultElements = [];
        currentIndex = -1;
        return;
    }

    // Call the backend search function
    const results = await eel.search_query(query)();
    // Render the results, now with grouping logic
    renderResults(results);
});

document.getElementById("toggleTheme").addEventListener("click", () => {
    document.body.classList.toggle("night");
});

// --- Modified renderResults function to group entries ---
function renderResults(results) {
    const container = document.getElementById("results");
    container.innerHTML = ""; // Clear previous results
    resultElements = []; // Clear previous element references
    currentIndex = -1; // Reset selection index

    // 1. Group results by headword
    const groupedResults = new Map(); // Use a Map to maintain insertion order if needed, or an object {} works too

    results.forEach(entry => {
        const headword = entry.headword;
        if (!groupedResults.has(headword)) {
            // If this is the first time seeing this headword, create a new group
            groupedResults.set(headword, {
                headword: headword,
                // Assuming transliteration is mostly consistent, take the first one
                transliteration: entry.transliteration || "",
                entries: [], // This array will hold all original entry objects for this headword
                sources: new Set() // Use a Set to collect unique sources
            });
        }
        // Add the current entry to the group's entries list
        const group = groupedResults.get(headword);
        group.entries.push(entry);
         if (entry.source) { // Collect sources from individual entries
            group.sources.add(entry.source);
        }
    });

    // 2. Render a list item for each grouped headword
    // Iterate over the values (the group objects) in the Map
    groupedResults.forEach(group => {
        const div = document.createElement("div");
        div.className = "result-item";
        div.tabIndex = 0; // Make it focusable for keyboard navigation

        // Use the headword and the collected transliteration for the display item
        // For the preview, use the first entry's preview as a representative
        const firstEntryInGroup = group.entries[0];
        const previewText = firstEntryInGroup.definition
             .map(def => def.slice(0, 20) + '...') // Take preview from the first entry's definitions
             .join("; ");

        div.innerHTML = `
            <div class="result-headword">${group.headword}</div>
            <div class="result-translit">${group.transliteration}</div>
            <div class="result-preview">${previewText}</div>
        `;

        // When this group item is clicked, show the definitions for ALL entries in the group
        div.onclick = () => showDefinition(group);

        container.appendChild(div);
        // Store the element and the full group object in resultElements
        resultElements.push({ el: div, group: group });
    });

    // Optional: automatically select the first item if there are results
    if (resultElements.length > 0) {
         currentIndex = 0;
         updateHighlight();
         // Optional: show the definition of the first item immediately
         // showDefinition(resultElements[0].group);
    }
}

// --- Modified showDefinition function to display all definitions in a group ---
function showDefinition(group) { // This function now receives a group object
    const definitionContent = document.getElementById("definitionContent");
    let html = `
        <div>
            <span class="result-headword">${group.headword}</span>
            <span class="result-translit">${group.transliteration}</span>
    `;

    // Display all collected unique sources
    if (group.sources.size > 0) {
        html += `<div class="result-source">Source(s): ${Array.from(group.sources).join(", ")}</div>`;
    }

    // Iterate through all original entries belonging to this headword
    group.entries.forEach(entry => {
        // Optionally add a separator or indicator for each entry if needed
        // For example, if sources differ significantly or you want to delineate
        // html += `<div class="entry-block">`; // Start block for this entry

        // Display the definitions for this specific entry
        entry.definition.forEach(def => {
            html += `<div class="result-definition">${def}</div>`;
        });

        // html += `</div>`; // End block for this entry
    });

    html += `</div>`; // Close the main definition container div

    definitionContent.innerHTML = html;
}

// --- Keyboard Navigation (mostly the same, but operates on the grouped items) ---
document.addEventListener("keydown", (e) => {
    if (resultElements.length === 0) return; // No results to navigate

    if (e.key === "ArrowDown") {
        e.preventDefault(); // Prevent default scrolling
        currentIndex = (currentIndex + 1) % resultElements.length;
        updateHighlight();
    } else if (e.key === "ArrowUp") {
        e.preventDefault(); // Prevent default scrolling
        currentIndex = (currentIndex - 1 + resultElements.length) % resultElements.length;
        updateHighlight();
    } else if (e.key === "Enter") {
        // Simulate click on the currently selected item (which represents a group)
        if (currentIndex >= 0) {
            resultElements[currentIndex].el.click();
        }
    } else if (e.key === "Escape") {
         // Reset selection and potentially clear definition/focus search box
        currentIndex = -1;
        updateHighlight(); // Remove highlight
        document.getElementById("definitionContent").innerHTML = ""; // Clear definition area
        document.getElementById("searchBox").focus(); // Move focus back to search box
    }
    // Add more keys here if needed (e.g., PageUp/PageDown for faster scrolling)
});

function updateHighlight() {
    // Remove highlight from all items
    resultElements.forEach(({ el }) => {
        el.classList.remove("selected");
    });

    // Add highlight to the current item if currentIndex is valid
    if (currentIndex >= 0 && currentIndex < resultElements.length) {
        const selectedItem = resultElements[currentIndex].el;
        selectedItem.classList.add("selected");

        // Scroll the results container to make the selected item visible
        const container = document.getElementById("results");
        const containerTop = container.scrollTop;
        const containerBottom = containerTop + container.clientHeight;

        const elementTop = selectedItem.offsetTop;
        const elementBottom = elementTop + selectedItem.offsetHeight;

        if (elementTop < containerTop) {
            // Scroll up
            container.scrollTop = elementTop;
        } else if (elementBottom > containerBottom) {
            // Scroll down
            container.scrollTop = elementBottom - container.clientHeight;
        }
    }
}
