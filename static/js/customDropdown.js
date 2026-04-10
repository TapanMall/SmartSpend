/**
 * Custom Dropdown Logic
 * Replaces all native <select> elements across the project with a fully styled
 * custom component matching the claymorphism/neon theme.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Inject the CSS dynamically into the head
    const style = document.createElement("style");
    style.innerHTML = `
        .ss-select-wrapper {
            position: relative;
            user-select: none;
            width: 100%;
            font-family: inherit;
        }
        .ss-select-trigger {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card2, #1a1f26);
            border: 1px solid var(--border2, #2a313c);
            border-radius: 12px;
            padding: 0.7rem 1rem;
            color: var(--text, #e2e8f0);
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .ss-select-trigger:hover, .ss-select-wrapper.open .ss-select-trigger {
            border-color: var(--g, #39ff7e);
            background: var(--card, #13171d);
        }
        .ss-select-wrapper.open .ss-select-trigger {
            box-shadow: 0 0 0 3px rgba(57, 255, 126, 0.15);
        }
        .ss-select-arrow {
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--muted, #64748b);
        }
        .ss-select-wrapper.open .ss-select-arrow {
            transform: rotate(180deg);
            color: var(--g, #39ff7e);
        }
        .ss-select-options {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 8px;
            background: var(--card, #13171d);
            border: 1px solid var(--border, #2a313c);
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            z-index: 9999;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            max-height: 250px;
            overflow-y: auto;
        }
        .ss-select-wrapper.open .ss-select-options {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        .ss-select-option {
            padding: 0.75rem 1.25rem;
            color: var(--muted, #94a3b8);
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }
        .ss-select-option:hover {
            color: var(--text, #fff);
            background: var(--card2, #1a1f26);
        }
        .ss-select-option.selected {
            color: var(--g, #39ff7e);
            font-weight: 600;
            background: rgba(57, 255, 126, 0.05);
        }
        /* Scrollbar styling for options */
        .ss-select-options::-webkit-scrollbar {
            width: 6px;
        }
        .ss-select-options::-webkit-scrollbar-thumb {
            background: var(--border2);
            border-radius: 10px;
        }
    `;
    document.head.appendChild(style);

    function initCustomSelects() {
        const selects = document.querySelectorAll("select");
        
        selects.forEach((select) => {
            if (select.dataset.customized) return;
            select.dataset.customized = "true";

            // Hide native select
            select.style.display = "none";

            // Wrapper
            const wrapper = document.createElement("div");
            wrapper.className = "ss-select-wrapper";
            if (select.parentElement) {
                // To maintain width constraints, let original class cascade
                if(select.classList.contains("form-input")) {
                    wrapper.style.marginBottom = "0"; // handle native parent margins
                }
                select.parentElement.insertBefore(wrapper, select.nextSibling);
            }

            // Trigger Box
            const trigger = document.createElement("div");
            trigger.className = "ss-select-trigger";
            
            const selectedTextNode = document.createElement("span");
            
            // Set initial value
            const initialSelectedOption = select.options[select.selectedIndex];
            selectedTextNode.textContent = initialSelectedOption ? initialSelectedOption.text : "Select an option";

            // SVG Arrow
            const arrow = document.createElement("div");
            arrow.className = "ss-select-arrow";
            arrow.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>`;

            trigger.appendChild(selectedTextNode);
            trigger.appendChild(arrow);
            wrapper.appendChild(trigger);

            // Options Container
            const optionsContainer = document.createElement("div");
            optionsContainer.className = "ss-select-options";

            // Populate options
            Array.from(select.options).forEach((option, index) => {
                const optDiv = document.createElement("div");
                optDiv.className = "ss-select-option";
                if (option.selected) optDiv.classList.add("selected");
                optDiv.textContent = option.text;
                
                optDiv.addEventListener("click", (e) => {
                    e.stopPropagation();
                    select.selectedIndex = index;
                    selectedTextNode.textContent = option.text;
                    
                    // Dispatch change event to trigger native listeners
                    select.dispatchEvent(new Event("change"));
                    
                    // Update selected class visually
                    optionsContainer.querySelectorAll(".ss-select-option").forEach(el => el.classList.remove("selected"));
                    optDiv.classList.add("selected");
                    
                    wrapper.classList.remove("open");
                });
                
                optionsContainer.appendChild(optDiv);
            });

            wrapper.appendChild(optionsContainer);

            // Toggle Open/Close
            trigger.addEventListener("click", (e) => {
                e.stopPropagation();
                // Close all other instances first
                document.querySelectorAll(".ss-select-wrapper.open").forEach(w => {
                    if (w !== wrapper) w.classList.remove("open");
                });
                wrapper.classList.toggle("open");
            });
        });
    }

    // Close options when clicking completely outside
    document.addEventListener("click", () => {
        document.querySelectorAll(".ss-select-wrapper.open").forEach(wrapper => {
            wrapper.classList.remove("open");
        });
    });

    // Run custom select builder immediately, and export function globally just in case
    initCustomSelects();
    window.refreshCustomSelects = initCustomSelects;
});
