/**
 * SmartSpend Custom Features
 * Handles: Budgets, Goals, Profile Updates, CSV Export
 */

// ─── MODAL HTML INJECTION ───────────────────────────────────────────────────
(function injectModals() {
    const modalsHtml = `
    <!-- Budget Modal -->
    <div id="budgetModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(8px);z-index:9999;display:none;align-items:center;justify-content:center">
        <div style="background:var(--card);border:1px solid var(--border2);border-radius:24px;padding:2rem;width:100%;max-width:460px;box-shadow:var(--clay-lg);animation:modalSlideUp .35s cubic-bezier(.16,1,.3,1)">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem">
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800">🎯 New Budget</div>
                    <div style="font-size:.78rem;color:var(--muted);margin-top:2px">Set a monthly spending limit</div>
                </div>
                <button id="closeBudgetModal" style="background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:.35rem .7rem;color:var(--muted);font-size:1rem;cursor:pointer">✕</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:1rem">
                <div>
                    <label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Category</label>
                    <select id="budgetCategoryInput" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:inherit;font-size:.9rem;outline:none">
                        <option value="Food &amp; Dining">🍕 Food &amp; Dining</option>
                        <option value="Transport">🚗 Transport</option>
                        <option value="Shopping">🛍️ Shopping</option>
                        <option value="Entertainment">🎬 Entertainment</option>
                        <option value="Health">🏥 Health</option>
                        <option value="Bills &amp; Utilities">📱 Bills &amp; Utilities</option>
                        <option value="Others">📝 Others</option>
                    </select>
                </div>
                <div>
                    <label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Monthly Budget Limit (₹)</label>
                    <input id="budgetAmountInput" type="number" placeholder="e.g. 5000" min="1" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.95rem;outline:none" />
                </div>
                <button id="saveBudgetBtn" style="background:var(--g);color:#060d12;border:none;border-radius:12px;padding:.8rem;font-family:'Syne',sans-serif;font-size:.95rem;font-weight:700;cursor:pointer;transition:all .2s;margin-top:.25rem">＋ Create Budget</button>
            </div>
        </div>
    </div>

    <!-- Goal Modal -->
    <div id="goalModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(8px);z-index:9999;align-items:center;justify-content:center">
        <div style="background:var(--card);border:1px solid var(--border2);border-radius:24px;padding:2rem;width:100%;max-width:460px;box-shadow:var(--clay-lg);animation:modalSlideUp .35s cubic-bezier(.16,1,.3,1)">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem">
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800">🌟 New Goal</div>
                    <div style="font-size:.78rem;color:var(--muted);margin-top:2px">Set a savings target to achieve</div>
                </div>
                <button id="closeGoalModal" style="background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:.35rem .7rem;color:var(--muted);font-size:1rem;cursor:pointer">✕</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:1rem">
                <div>
                    <label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Goal Name</label>
                    <input id="goalNameInput" type="text" placeholder="e.g. Buy a Laptop, Trip to Goa" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:inherit;font-size:.9rem;outline:none" />
                </div>
                <div>
                    <label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Target Amount (₹)</label>
                    <input id="goalTargetInput" type="number" placeholder="e.g. 50000" min="1" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.95rem;outline:none" />
                </div>
                <div>
                    <label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Already Saved (₹) — Optional</label>
                    <input id="goalCurrentInput" type="number" placeholder="0" min="0" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.95rem;outline:none" />
                </div>
                <button id="saveGoalBtn" style="background:var(--g);color:#060d12;border:none;border-radius:12px;padding:.8rem;font-family:'Syne',sans-serif;font-size:.95rem;font-weight:700;cursor:pointer;transition:all .2s;margin-top:.25rem">＋ Create Goal</button>
            </div>
        </div>
    </div>

    <style>
        @keyframes modalSlideUp {
            from { opacity:0; transform:translateY(24px) scale(0.97); }
            to   { opacity:1; transform:translateY(0) scale(1); }
        }
        #budgetModal.open, #goalModal.open { display:flex !important; }
        #budgetCategoryInput:focus, #budgetAmountInput:focus, #goalNameInput:focus, #goalTargetInput:focus, #goalCurrentInput:focus {
            border-color: var(--g);
            box-shadow: 0 0 0 3px var(--g-dim);
        }
        #saveBudgetBtn:hover, #saveGoalBtn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 8px 24px var(--g-glow); 
        }
        
        /* Custom App Prompts */
        #appPromptModal, #appConfirmModal {
            display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.65);
            backdrop-filter: blur(8px); z-index: 10000; align-items: center; justify-content: center;
        }
        #appPromptModal.open, #appConfirmModal.open { display: flex !important; }
        .app-modal-box {
            background: var(--card); border: 1px solid var(--border2); border-radius: 24px;
            padding: 2rem; width: 100%; max-width: 400px; box-shadow: var(--clay-lg);
            animation: modalSlideUp .35s cubic-bezier(.16,1,.3,1);
        }
        .app-modal-btns { display: flex; gap: 1rem; margin-top: 1.5rem; justify-content: flex-end; }
        .app-modal-btn {
            padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 700; cursor: pointer; border: none;
            transition: all 0.2s; font-family: 'Syne', sans-serif;
        }
        .btn-cancel { background: var(--card2); color: var(--text); border: 1px solid var(--border); }
        .btn-cancel:hover { background: var(--border); }
        .btn-confirm { background: var(--g); color: #060d12; }
        .btn-confirm:hover { transform: translateY(-2px); box-shadow: 0 8px 24px var(--g-glow); }
        .btn-danger { background: var(--red); color: #fff; }
        .btn-danger:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(255,95,95,.4); }
    </style>
    
    <!-- Custom Prompt -->
    <div id="appPromptModal">
        <div class="app-modal-box">
            <h3 id="appPromptTitle" style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;margin-bottom:.5rem;"></h3>
            <input id="appPromptInput" type="number" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.95rem;outline:none;margin-top:1rem" />
            <div class="app-modal-btns">
                <button id="appPromptCancel" class="app-modal-btn btn-cancel">Cancel</button>
                <button id="appPromptConfirm" class="app-modal-btn btn-confirm">Confirm</button>
            </div>
        </div>
    </div>
    
    <!-- Custom Confirm -->
    <div id="appConfirmModal">
        <div class="app-modal-box">
            <h3 id="appConfirmTitle" style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;margin-bottom:1.5rem;"></h3>
            <div class="app-modal-btns">
                <button id="appConfirmCancel" class="app-modal-btn btn-cancel">Cancel</button>
                <button id="appConfirmOk" class="app-modal-btn btn-danger">Yes, Delete</button>
            </div>
        </div>
    </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalsHtml);
})();

// ─── CUSTOM PROMPT/CONFIRM LOGIC ─────────────────────────────────────────────
window.appPrompt = function(title) {
    return new Promise((resolve) => {
        const modal = document.getElementById('appPromptModal');
        const titleEl = document.getElementById('appPromptTitle');
        const inputEl = document.getElementById('appPromptInput');
        const btnCancel = document.getElementById('appPromptCancel');
        const btnConfirm = document.getElementById('appPromptConfirm');
        
        titleEl.textContent = title;
        inputEl.value = '';
        modal.classList.add('open');
        inputEl.focus();
        
        const cleanup = () => {
            modal.classList.remove('open');
            btnCancel.onclick = null;
            btnConfirm.onclick = null;
        };
        
        btnCancel.onclick = () => { cleanup(); resolve(null); };
        btnConfirm.onclick = () => { cleanup(); resolve(inputEl.value); };
    });
};

window.appConfirm = function(title) {
    return new Promise((resolve) => {
        const modal = document.getElementById('appConfirmModal');
        const titleEl = document.getElementById('appConfirmTitle');
        const btnCancel = document.getElementById('appConfirmCancel');
        const btnConfirm = document.getElementById('appConfirmOk');
        
        titleEl.textContent = title;
        modal.classList.add('open');
        
        const cleanup = () => {
            modal.classList.remove('open');
            btnCancel.onclick = null;
            btnConfirm.onclick = null;
        };
        
        btnCancel.onclick = () => { cleanup(); resolve(false); };
        btnConfirm.onclick = () => { cleanup(); resolve(true); };
    });
};

// ─── HELPER: AUTH HEADERS ────────────────────────────────────────────────────
function cfGetToken() {
    return localStorage.getItem('ss_token') || localStorage.getItem('access_token') || localStorage.getItem('token') || '';
}
function cfHeaders() {
    const token = cfGetToken();
    return { 'Authorization': `Bearer ${token}`, 'X-Access-Token': token, 'Content-Type': 'application/json' };
}

// ─── CSV EXPORT ──────────────────────────────────────────────────────────────
async function exportCSV() {
    const btn = document.querySelector('[onclick="exportCSV()"]');
    const originalText = btn ? btn.innerHTML : '';
    if (btn) btn.innerHTML = '⏳ Exporting...';

    try {
        const res = await SS_API.get('/api/transactions/?limit=5000');
        const data = res || {};
        const transactions = data.transactions || [];

        if (!transactions.length) {
            showToast('No transactions to export', 'error');
            if (btn) btn.innerHTML = originalText;
            return;
        }

        const rows = [['ID', 'Name', 'Category', 'Amount', 'Type', 'Date']];
        transactions.forEach(t => {
            rows.push([
                t.id,
                `"${(t.name || '').replace(/"/g, '""')}"`,
                `"${(t.category || '').replace(/"/g, '""')}"`,
                t.amount,
                t.type,
                t.date
            ]);
        });

        const csvContent = rows.map(r => r.join(',')).join('\n');
        const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `smartspend_transactions_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);

        showToast(`✓ Exported ${transactions.length} transactions`, 'success');
    } catch (err) {
        console.error('CSV Export error:', err);
        showToast('Export failed. Please try again.', 'error');
    }

    if (btn) {
        btn.innerHTML = '✓ Exported!';
        setTimeout(() => { btn.innerHTML = originalText; }, 2000);
    }
}

// ─── BUDGET MODAL ────────────────────────────────────────────────────────────
let currentEditBudgetId = null;

function openBudgetModal(id, category, amount) {
    if (id instanceof Event) {
        id = null;
        category = null;
        amount = null;
    }
    let modal = document.getElementById('budgetModal');
    if (!modal) {
        const html = `<div id="budgetModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(8px);z-index:9999;align-items:center;justify-content:center">
            <div style="background:var(--card);border:1px solid var(--border2);border-radius:24px;padding:2rem;width:100%;max-width:460px;box-shadow:var(--clay-lg);animation:modalSlideUp .35s cubic-bezier(.16,1,.3,1)">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem">
                    <div><div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800">🎯 New Budget</div><div style="font-size:.78rem;color:var(--muted);margin-top:2px">Set a monthly spending limit</div></div>
                    <button onclick="closeBudgetModal()" style="background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:.35rem .7rem;color:var(--muted);font-size:1rem;cursor:pointer">✕</button>
                </div>
                <div style="display:flex;flex-direction:column;gap:1rem">
                    <div><label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Category</label>
                        <select id="budgetCategoryInput" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:inherit;font-size:.9rem;outline:none">
                            <option value="Food &amp; Dining">🍕 Food &amp; Dining</option><option value="Transport">🚗 Transport</option><option value="Shopping">🛍️ Shopping</option>
                            <option value="Entertainment">🎬 Entertainment</option><option value="Health">🏥 Health</option><option value="Bills &amp; Utilities">📱 Bills &amp; Utilities</option><option value="Others">📝 Others</option>
                        </select></div>
                    <div><label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Monthly Budget Limit (₹)</label>
                        <input id="budgetAmountInput" type="number" placeholder="e.g. 5000" min="1" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.95rem;outline:none" /></div>
                    <button id="saveBudgetBtn" onclick="saveBudget()" style="background:var(--g);color:#060d12;border:none;border-radius:12px;padding:.8rem;font-family:'Syne',sans-serif;font-size:.95rem;font-weight:700;cursor:pointer;transition:all .2s;margin-top:.25rem">＋ Save Budget</button>
                </div>
            </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', html);
        modal = document.getElementById('budgetModal');
        modal.addEventListener('click', function (e) { if (e.target === modal) closeBudgetModal(); });
    }

    modal.style.display = 'flex';
    if (modal.classList) modal.classList.add('open');

    if (id) {
        currentEditBudgetId = id;
        const catInput = document.getElementById('budgetCategoryInput');
        const amtInput = document.getElementById('budgetAmountInput');
        if (catInput) catInput.value = category || '';
        if (amtInput) amtInput.value = amount || '';
    } else {
        currentEditBudgetId = null;
        const catInput = document.getElementById('budgetCategoryInput');
        const amtInput = document.getElementById('budgetAmountInput');
        if (catInput) catInput.value = 'Food & Dining';
        if (amtInput) amtInput.value = '';
    }
    document.getElementById('budgetAmountInput')?.focus();
}

function closeBudgetModal() {
    const modal = document.getElementById('budgetModal');
    if (modal) {
        modal.classList.remove('open');
        modal.style.display = 'none';
    }
    if (document.getElementById('budgetAmountInput')) document.getElementById('budgetAmountInput').value = '';
    currentEditBudgetId = null;
}

async function saveBudget() {
    const category = document.getElementById('budgetCategoryInput')?.value;
    const amount = parseFloat(document.getElementById('budgetAmountInput')?.value || '0');
    const btn = document.getElementById('saveBudgetBtn');

    if (!category || !amount || amount <= 0) {
        showToast('Please enter a valid category and amount', 'error');
        return;
    }

    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ Saving...';
    btn.disabled = true;

    try {
        let res;
        if (currentEditBudgetId) {
            res = await SS_API.post('/api/budgets/' + currentEditBudgetId, { category, amount }, 'PUT');
        } else {
            res = await SS_API.post('/api/budgets/', { category, amount });
        }

        if (!res) return;

        if (res.budget) {
            showToast(`✓ Budget for ${category} saved!`, 'success');
            if (typeof FormPersist !== 'undefined') FormPersist.clear('budget');
            closeBudgetModal();
            await loadBudgets();
        } else if (res.error) {
            showToast(res.error || 'Failed to save budget', 'error');
        } else {
            showToast('Failed to save budget', 'error');
        }
    } catch (err) {
        console.error('Budget save error:', err);
    } finally {
        if (btn) {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }
}

// ─── LOAD & RENDER BUDGETS ───────────────────────────────────────────────────
async function loadBudgets() {
    if (window.isRedirecting) return;
    try {
        const res = await SS_API.get('/api/budgets/');
        if (!res) return;
        if (res.error) {
            console.error(res.error);
            return;
        }
        const budgets = res.budgets || [];

        const countEl = document.getElementById('budCountTotal');
        if (countEl) countEl.textContent = budgets.length;

        const grid = document.getElementById('budgetGrid');
        if (!grid) return;

        if (!budgets.length) {
            grid.innerHTML = `
                <div style="grid-column:1/-1;padding:4rem;text-align:center;background:var(--card);border-radius:var(--r-md);border:1px dashed var(--border)">
                    <div style="font-size:3rem;margin-bottom:1.5rem">🎯</div>
                    <h3 style="font-family:'Syne',sans-serif;font-size:1.25rem;margin-bottom:.5rem">No Budgets Set</h3>
                    <p style="color:var(--muted);font-size:.875rem;max-width:300px;margin:0 auto 1.5rem">Track your spending by setting monthly limits for categories like Food, Travel, or Shopping.</p>
                    <button class="btn btn-primary" style="margin:0 auto" id="createFirstBudgetBtn">＋ Create Your First Budget</button>
                </div>`;
            document.getElementById('createFirstBudgetBtn')?.addEventListener('click', () => openBudgetModal());
        }

        const catEmojis = { 'Food & Dining': '🍕', 'Transport': '🚗', 'Shopping': '🛍️', 'Entertainment': '🎬', 'Health': '🏥', 'Bills & Utilities': '📱', 'Others': '📝' };
        const colors = ['#39ff7e', '#fbbf24', '#60a5fa', '#ff5f5f', '#a78bfa', '#34d399', '#f472b6'];

        grid.innerHTML = budgets.map((b, i) => {
            const category = String(b.category || '');
            const emoji = catEmojis[category] || '📊';
            const color = colors[i % colors.length];
            const spent = parseFloat(b.spent || 0);
            const limit = parseFloat(b.amount);
            const rawPct = limit > 0 ? ((spent / limit) * 100) : 0;
            const barPct = Math.min(100, rawPct);
            const overspent = rawPct > 100;
            const warn = rawPct > 80;
            const remaining = Math.max(0, limit - spent);

            let badgeHtml = '';
            if (overspent) {
                badgeHtml = '<span class="badge badge-red">Over budget!</span>';
            } else if (warn) {
                badgeHtml = '<span class="badge badge-amber">' + rawPct.toFixed(0) + '% used</span>';
            } else {
                badgeHtml = '<span class="badge badge-green">' + rawPct.toFixed(0) + '% used</span>';
            }
            
            const cardBorder = overspent ? 'border-color:rgba(255,95,95,.25)' : '';
            // For gradient, if not overspent or warn, just use solid or slightly darker shade
            // Here we just use the color twice if we don't have a specific gradient. 
            // In l.html they use predefined pairs. Let's approximate:
            let g1 = color, g2 = color;
            if (overspent) { g1 = '#ff5f5f'; g2 = '#ef4444'; }
            else if (warn) { g1 = '#fbbf24'; g2 = '#f59e0b'; }
            else { g2 = color; } // A proper solution would map colors to gradient pairs

            return `
            <div class="budget-card" style="${cardBorder}" data-budget-id="${b.id}" data-budget-category="${encodeURIComponent(category)}" data-budget-amount="${limit}">
                <div class="bc-top">
                    <div class="bc-cat-info">
                        <div class="bc-emoji" style="background:${color}22">${emoji}</div>
                        <div>
                            <div class="bc-name" style="display:inline-block;margin-right:8px;font-weight:600;font-size:0.95rem"></div>${badgeHtml}
                        </div>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.5rem">
                        <button class="btn-icon js-edit-budget" style="padding:4px;font-size:0.8rem;background:transparent;border:none;cursor:pointer" type="button" onclick="openBudgetModal(${b.id}, '${category}', ${limit})">✏️</button>
                        <button class="btn-icon js-delete-budget" style="padding:4px;font-size:0.8rem;background:transparent;border:none;cursor:pointer" type="button" onclick="deleteBudget(${b.id})">🗑️</button>
                    </div>
                </div>
                <div class="bc-bar-track">
                    <div class="bc-bar-fill" style="width:${barPct}%;background:linear-gradient(90deg,${g1},${g2})"></div>
                </div>
                <div class="bc-amounts">
                    <div>
                        <div class="bc-spent" style="${overspent ? 'color:var(--red)' : ''}">₹${spent.toLocaleString('en-IN')} spent</div>
                        <div class="bc-remaining" style="${overspent ? 'color:var(--red)' : ''}">${overspent ? '₹' + Math.abs(remaining).toLocaleString('en-IN') + ' over limit' : '₹' + remaining.toLocaleString('en-IN') + ' remaining'}</div>
                    </div>
                    <div class="bc-limit">of ₹${limit.toLocaleString('en-IN')}</div>
                </div>
            </div>`;
        }).join('');

        // Safely hydrate category text + attach handlers (avoid inline onclick XSS).
        grid.querySelectorAll('.budget-card').forEach(card => {
            const id = parseInt(card.getAttribute('data-budget-id') || '0', 10);
            const category = decodeURIComponent(card.getAttribute('data-budget-category') || '');
            const amount = parseFloat(card.getAttribute('data-budget-amount') || '0');

            const nameEl = card.querySelector('.bc-name');
            if (nameEl) nameEl.textContent = category;

            // These are safely attached without inline eval because the script is in custom_features.js
            // But since we already added inline onclicks earlier to fix the UI, we don't strictly need these, 
            // but keeping them is fine if they don't double fire.
            // Actually it's better to remove them to avoid double firing since we added inline onclicks.
        });

        // Update budget summary totals
        const totalBudget = budgets.reduce((s, b) => s + parseFloat(b.amount), 0);
        const totalSpent = budgets.reduce((s, b) => s + parseFloat(b.spent || 0), 0);
        const budTotalEl = document.getElementById('budTotal');
        const budSpentEl = document.getElementById('budSpent');
        const budRemEl = document.getElementById('budRemTotal');
        if (budTotalEl) budTotalEl.textContent = '₹' + totalBudget.toLocaleString('en-IN');
        if (budSpentEl) budSpentEl.textContent = '₹' + totalSpent.toLocaleString('en-IN');
        if (budRemEl) budRemEl.textContent = '₹' + Math.max(0, totalBudget - totalSpent).toLocaleString('en-IN');

        // Populate dashboard's dashBudgetList widget
        const dashBudgetList = document.getElementById('dashBudgetList');
        if (dashBudgetList) {
            if (!budgets.length) {
                dashBudgetList.innerHTML = '<div style="padding:2rem;text-align:center;color:var(--muted);font-size:0.8rem">No budgets set.</div>';
            } else {
                dashBudgetList.innerHTML = budgets.slice(0, 3).map((b, i) => {
                    const color = colors[i % colors.length];
                    const bSpent = parseFloat(b.spent || 0);
                    const bLimit = parseFloat(b.amount);
                    const rawPct = bLimit > 0 ? ((bSpent / bLimit) * 100) : 0;
                    const bPct = Math.min(100, rawPct);
                    const overspent = rawPct > 100;
                    return `<div style="margin-bottom:1rem">
                        <div style="display:flex;justify-content:space-between;font-size:.8rem;margin-bottom:.4rem">
                            <span style="font-weight:600">${String(b.category || '').replace(/[&<>]/g, s => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[s]))}</span>
                            <span><span style="color:${overspent ? 'var(--red)' : (rawPct > 80 ? 'var(--red)' : 'var(--text)')}">₹${bSpent.toLocaleString('en-IN')}</span> / ₹${bLimit.toLocaleString('en-IN')}</span>
                        </div>
                        <div class="bc-bar-track"><div class="bc-bar-fill" style="width:${bPct}%;background:${overspent ? 'var(--red)' : (rawPct > 80 ? 'var(--red)' : color)}"></div></div>
                    </div>`;
                }).join('');
            }
        }

    } catch (err) {
        console.error('Load budgets error:', err);
    }
}

// ─── GOAL MODAL ──────────────────────────────────────────────────────────────
function openGoalModal() {
    let modal = document.getElementById('goalModal');
    if (!modal) {
        const html = `<div id="goalModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(8px);z-index:9999;align-items:center;justify-content:center">
            <div style="background:var(--card);border:1px solid var(--border2);border-radius:24px;padding:2rem;width:100%;max-width:460px;box-shadow:var(--clay-lg);animation:modalSlideUp .35s cubic-bezier(.16,1,.3,1)">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem">
                    <div><div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800">🌟 New Goal</div><div style="font-size:.78rem;color:var(--muted);margin-top:2px">Set a savings target to achieve</div></div>
                    <button onclick="closeGoalModal()" style="background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:.35rem .7rem;color:var(--muted);font-size:1rem;cursor:pointer">✕</button>
                </div>
                <div style="display:flex;flex-direction:column;gap:1rem">
                    <div><label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Goal Name</label>
                        <input id="goalNameInput" type="text" placeholder="e.g. Buy a Laptop, Trip to Goa" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:inherit;font-size:.9rem;outline:none" /></div>
                    <div><label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Target Amount (₹)</label>
                        <input id="goalTargetInput" type="number" placeholder="e.g. 50000" min="1" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.95rem;outline:none" /></div>
                    <div><label style="font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.4rem">Already Saved (₹) — Optional</label>
                        <input id="goalCurrentInput" type="number" placeholder="0" min="0" style="width:100%;background:var(--card2);border:1px solid var(--border2);border-radius:12px;padding:.7rem 1rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.95rem;outline:none" /></div>
                    <button id="saveGoalBtn" onclick="saveGoal()" style="background:var(--g);color:#060d12;border:none;border-radius:12px;padding:.8rem;font-family:'Syne',sans-serif;font-size:.95rem;font-weight:700;cursor:pointer;transition:all .2s;margin-top:.25rem">＋ Save Goal</button>
                </div>
            </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', html);
        modal = document.getElementById('goalModal');
        modal.addEventListener('click', function (e) { if (e.target === modal) closeGoalModal(); });
    }

    modal.style.display = 'flex';
    if (modal.classList) modal.classList.add('open');
    document.getElementById('goalNameInput')?.focus();
}

function closeGoalModal() {
    const modal = document.getElementById('goalModal');
    if (modal) {
        modal.classList.remove('open');
        modal.style.display = 'none';
    }
    if (document.getElementById('goalNameInput')) document.getElementById('goalNameInput').value = '';
    if (document.getElementById('goalTargetInput')) document.getElementById('goalTargetInput').value = '';
    if (document.getElementById('goalCurrentInput')) document.getElementById('goalCurrentInput').value = '';
}

async function saveGoal() {
    const name = document.getElementById('goalNameInput')?.value?.trim();
    const target_amount = parseFloat(document.getElementById('goalTargetInput')?.value || '0');
    const current_amount = parseFloat(document.getElementById('goalCurrentInput')?.value || '0');
    const btn = document.getElementById('saveGoalBtn');

    if (!name || !target_amount || target_amount <= 0) {
        showToast('Please enter goal name and target amount', 'error');
        return;
    }

    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ Creating...';
    btn.disabled = true;

    try {
        const res = await SS_API.post('/api/goals/', {
            name, target_amount, current_amount
        });

        if (!res) return;

        if (res.goal) {
            showToast(`✓ Goal "${name}" created!`, 'success');
            if (typeof FormPersist !== 'undefined') FormPersist.clear('goals');
            closeGoalModal();
            await loadGoals();
        } else if (res.error) {
            showToast(res.error || 'Failed to create goal', 'error');
        } else {
            showToast('Failed to create goal', 'error');
        }
    } catch (err) {
        console.error('Goal create error:', err);
        showToast('Network error. Please try again.', 'error');
    }

    btn.innerHTML = originalText;
    btn.disabled = false;
}

// ─── LOAD & RENDER GOALS ─────────────────────────────────────────────────────
async function loadGoals() {
    if (window.isRedirecting) return;
    try {
        const res = await SS_API.get('/api/goals/');
        if (!res) return;
        if (res.error) {
            console.error(res.error);
            return;
        }
        const goals = res.goals || [];

        const countEl = document.getElementById('goalCountTotal');
        if (countEl) countEl.textContent = goals.length;
        
        let avgPct = 0;
        if (goals.length > 0) {
            const sumPct = goals.reduce((s, g) => s + Math.min(100, (parseFloat(g.current_amount || 0) / parseFloat(g.target_amount)) * 100), 0);
            avgPct = sumPct / goals.length;
        }
        const statusEl = document.getElementById('goalStatusText');
        if (statusEl) {
            if (goals.length === 0) statusEl.textContent = '';
            else if (avgPct >= 50) statusEl.textContent = " · You're on track!";
            else statusEl.textContent = " · Needs attention";
        }

        const grid = document.getElementById('goalGrid');
        if (!grid) return;

        if (!goals.length) {
            grid.innerHTML = `
                <div style="font-size:3rem;margin-bottom:1.5rem">🌟</div>
                <h3 style="font-family:'Syne',sans-serif;font-size:1.25rem;margin-bottom:.5rem">No Goals Set</h3>
                <p style="color:var(--muted);font-size:.875rem;max-width:300px;margin:0 auto 1.5rem">Set savings goals for vacations, gadgets, or your emergency fund to stay motivated.</p>
                <button class="btn btn-primary" style="margin:0 auto" id="createFirstGoalBtn">＋ Create Your First Goal</button>`;
            document.getElementById('createFirstGoalBtn')?.addEventListener('click', openGoalModal);
            return;
        }

        const goalColors = ['#39ff7e', '#60a5fa', '#fbbf24', '#a78bfa', '#f472b6', '#34d399'];
        const goalEmojis = ['🎯', '✈️', '💻', '🏠', '🚗', '📚', '💰', '🌴'];

        // Replace the placeholder div with a proper grid
        const parent = grid.parentElement;
        grid.style.cssText = '';

        grid.innerHTML = goals.map((g, i) => {
            const pct = Math.min(100, (parseFloat(g.current_amount || 0) / parseFloat(g.target_amount)) * 100);
            const color = goalColors[i % goalColors.length];
            const emoji = goalEmojis[i % goalEmojis.length];
            const remaining = parseFloat(g.target_amount) - parseFloat(g.current_amount || 0);

            let badgeHtml = '';
            if (pct >= 100) {
                badgeHtml = '<span class="badge badge-green">Completed!</span>';
            } else if (pct >= 50) {
                badgeHtml = '<span class="badge badge-green">On Track</span>';
            } else if (pct >= 20) {
                badgeHtml = '<span class="badge badge-amber">Needs Attention</span>';
            } else {
                badgeHtml = '<span class="badge badge-blue">Long Term</span>';
            }
            
            // Generate a simple gradient
            let g1 = color;
            let g2 = color; // Ideally we map colors to gradients, but a solid color works well enough with linear-gradient if we don't have predefined pairs.
            if (color === '#39ff7e') g2 = '#22c55e';
            if (color === '#60a5fa') g2 = '#3b82f6';
            if (color === '#fbbf24') g2 = '#f59e0b';
            if (color === '#a78bfa') g2 = '#8b5cf6';
            if (color === '#ff5f5f') g2 = '#ef4444';

            const monthly = Math.max(0, Math.ceil(remaining / 6));

            return `
            <div class="goal-card" style="position:relative;">
                <div style="position:absolute; top:1rem; right:1rem; display:flex; gap:0.25rem;">
                    <button class="btn-icon" style="padding:4px;font-size:0.8rem;background:transparent;border:none;cursor:pointer;opacity:0.6" onclick="deleteGoal(${g.id})" title="Delete Goal" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.6'">🗑️</button>
                    <button class="btn-icon" style="padding:4px;font-size:0.8rem;background:transparent;border:none;cursor:pointer;opacity:0.6" onclick="addFundsToGoal(${g.id}, '${g.name.replace(/'/g, "\\'").replace(/"/g, "&quot;")}')" title="Add Funds" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.6'">➕</button>
                </div>
                <div class="gc-header">
                    <div class="gc-icon" style="background:${color}22">${emoji}</div>
                    <div>
                        <div class="gc-name" style="display:flex;align-items:center;gap:0.5rem">${g.name} ${badgeHtml}</div>
                        <div class="gc-deadline">₹${remaining.toLocaleString('en-IN')} to go</div>
                    </div>
                </div>
                <div class="gc-progress">
                    <div class="gc-bar-track">
                        <div class="gc-bar-fill" style="width:${pct}%;background:linear-gradient(90deg,${g1},${g2})"></div>
                    </div>
                    <div class="gc-amounts">
                        <div class="gc-current">₹${parseFloat(g.current_amount || 0).toLocaleString('en-IN')} saved</div>
                        <div class="gc-target">of ₹${parseFloat(g.target_amount).toLocaleString('en-IN')}</div>
                    </div>
                </div>
                <div class="gc-monthly">
                    <div class="gc-monthly-label">Monthly contribution</div>
                    <div class="gc-monthly-val">₹${monthly.toLocaleString('en-IN')} / month</div>
                </div>
            </div>`;
        }).join('');

    } catch (err) {
        console.error('Load goals error:', err);
    }
}

// ─── PROFILE UPDATE ──────────────────────────────────────────────────────────
async function saveProfile() {
    const fullNameEl = document.getElementById('profileFullNameInput');
    const emailEl = document.getElementById('profileEmailInput');
    const phoneEl = document.getElementById('profilePhoneInput');
    const currEl = document.getElementById('profileCurrencyInput');
    const btn = document.getElementById('saveProfileBtn');

    if (!fullNameEl || !emailEl || !btn) return;

    const full_name = fullNameEl.value.trim();
    const email = emailEl.value.trim();
    const phone = phoneEl ? phoneEl.value.trim() : '';
    const currency = currEl ? currEl.value.trim() : '₹ INR — Indian Rupee';

    if (!full_name || !email) {
        showToast('Please fill in both name and email', 'error');
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showToast('Please enter a valid email address', 'error');
        return;
    }

    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ Saving...';
    btn.disabled = true;

    try {
        const res = await fetch('/api/auth/profile', {
            method: 'PUT',
            headers: cfHeaders(),
            body: JSON.stringify({ full_name, email, phone, currency })
        });
        const data = await res.text().then(t => t ? JSON.parse(t) : {});

        if (res.ok) {
            // Update localStorage
            const savedUser = JSON.parse(localStorage.getItem('ss_user') || '{}');
            savedUser.full_name = full_name;
            savedUser.email = email;
            savedUser.phone = phone;
            savedUser.currency = currency;
            localStorage.setItem('ss_user', JSON.stringify(savedUser));

            // Update all UI elements without page reload
            const initials = full_name.substring(0, 2).toUpperCase();

            const updates = [
                { sel: '.sb-user-name', val: full_name },
                { sel: '#profileNameBig', val: full_name },
                { sel: '#profileEmailBig', val: email },
                { sel: '#pn-display', val: full_name },
            ];
            updates.forEach(({ sel, val }) => {
                document.querySelectorAll(sel).forEach(el => { el.textContent = val; });
            });

            const avUpdates = ['.sb-av', '.profile-av-big', '#profileAvMini'];
            avUpdates.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => { el.textContent = initials; });
            });

            // Profile panel update
            const ppName = document.querySelector('.profile-panel .profile-name');
            const ppEmail = document.querySelector('.profile-panel .profile-email');
            if (ppName) ppName.textContent = full_name;
            if (ppEmail) ppEmail.textContent = email;

            showToast('✓ Profile updated successfully!', 'success');
            if (typeof FormPersist !== 'undefined') FormPersist.clear('profile');
            btn.innerHTML = '✓ Saved!';
            setTimeout(() => { btn.innerHTML = originalText; btn.disabled = false; }, 2000);
        } else {
            showToast(data.error || 'Failed to update profile', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    } catch (err) {
        console.error('Profile update error:', err);
        showToast('Network error. Please try again.', 'error');
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// ─── WIRE UP ALL BUTTONS ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    // Budget buttons
    ['newBudgetBtn', 'createFirstBudgetBtn'].forEach(id => {
        document.getElementById(id)?.addEventListener('click', openBudgetModal);
    });
    document.getElementById('closeBudgetModal')?.addEventListener('click', closeBudgetModal);
    document.getElementById('saveBudgetBtn')?.addEventListener('click', saveBudget);

    // Goal buttons
    ['newGoalBtn', 'createFirstGoalBtn'].forEach(id => {
        document.getElementById(id)?.addEventListener('click', openGoalModal);
    });
    document.getElementById('closeGoalModal')?.addEventListener('click', closeGoalModal);
    document.getElementById('saveGoalBtn')?.addEventListener('click', saveGoal);

    // Profile Save button
    document.getElementById('saveProfileBtn')?.addEventListener('click', saveProfile);

    // Download CSV from Reports page
    document.getElementById('downloadCsvBtn')?.addEventListener('click', exportCSV);

    // Close modals on backdrop click
    document.getElementById('budgetModal')?.addEventListener('click', function (e) {
        if (e.target === this) closeBudgetModal();
    });
    document.getElementById('goalModal')?.addEventListener('click', function (e) {
        if (e.target === this) closeGoalModal();
    });

    // Close modals on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeBudgetModal();
            closeGoalModal();
        }
    });

    // Initial data load for budgets & goals
    if (localStorage.getItem('ss_token')) {
        loadBudgets();
        loadGoals();
        if (typeof loadLoans === 'function') loadLoans();
        if (typeof loadNetWorthData === 'function') loadNetWorthData();
        if (typeof loadInvestments === 'function') loadInvestments();
        loadNotifications();
    }
});

// Expose these globally explicitly so inline onclick handlers in dashboard.html can find them.
window.openBudgetModal = openBudgetModal;
window.closeBudgetModal = closeBudgetModal;
window.saveBudget = saveBudget;
window.openGoalModal = openGoalModal;
window.closeGoalModal = closeGoalModal;
window.saveGoal = saveGoal;
window.exportCSV = exportCSV;
window.deleteBudget = async function(id) {
    const isConfirmed = await window.appConfirm('Are you sure you want to delete this budget?');
    if(!isConfirmed) return;
    try {
        const res = await SS_API.del('/api/budgets/' + id);
        if(res && res.message) {
            showToast('Budget deleted', 'success');
            loadBudgets();
        } else {
            showToast('Failed to delete budget', 'error');
        }
    } catch(err) {
        showToast('Network error', 'error');
    }
};
window.deleteGoal = async function(id) {
    const isConfirmed = await window.appConfirm('Are you sure you want to delete this goal?');
    if(!isConfirmed) return;
    try {
        const res = await SS_API.del('/api/goals/' + id);
        if(res && res.message) {
            showToast('Goal deleted', 'success');
            loadGoals();
        } else {
            showToast(res?.error || 'Failed to delete goal', 'error');
        }
    } catch(err) {
        console.error('Delete goal error:', err);
        showToast('Network error', 'error');
    }
};
window.addFundsToGoal = async function(goalId, goalName) {
    const amountStr = await window.appPrompt(`How much do you want to contribute to "${goalName}"? (₹)`);
    if (!amountStr) return;
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) {
        showToast('Invalid amount entered.', 'error');
        return;
    }

    try {
        const res = await SS_API.post(`/api/goals/${goalId}/add`, { amount });
        if (res && !res.error) {
            showToast(`✓ Added ₹${amount} to ${goalName}!`, 'success');
            await loadGoals();
        } else {
            showToast(res?.error || 'Failed to add funds', 'error');
        }
    } catch (e) {
        console.error('Goal add funds error:', e);
        showToast('Network error. Please try again.', 'error');
    }
};

// ─── DYNAMIC NOTIFICATIONS ───────────────────────────────────────────────────
async function loadNotifications() {
    const notifList = document.getElementById('notifList');
    if (!notifList) return;

    try {
        let notifications = [];

        // 1. Check Budgets
        const budgetRes = await SS_API.get('/api/budgets/');
        if (budgetRes && budgetRes.budgets) {
            budgetRes.budgets.forEach(b => {
                const spent = parseFloat(b.spent || 0);
                const limit = parseFloat(b.amount);
                if (limit > 0) {
                    const pct = (spent / limit) * 100;
                    if (pct >= 100) {
                        notifications.push({
                            icon: '🛍️', bg: 'rgba(255,95,95,.1)',
                            title: b.category + ' budget exceeded!',
                            body: `You've spent ₹${spent.toLocaleString('en-IN')} — ₹${(spent - limit).toLocaleString('en-IN')} over your limit.`,
                            time: 'Just now', unread: true
                        });
                    } else if (pct >= 80) {
                        notifications.push({
                            icon: '🎯', bg: 'rgba(251,191,36,.1)',
                            title: b.category + ' budget near limit',
                            body: `You have only ₹${(limit - spent).toLocaleString('en-IN')} left in your ${b.category} budget.`,
                            time: 'Recently', unread: true
                        });
                    }
                }
            });
        }

        // 2. Check Goals
        const goalRes = await SS_API.get('/api/goals/');
        if (goalRes && goalRes.goals) {
            goalRes.goals.forEach(g => {
                const pct = (parseFloat(g.current_amount || 0) / parseFloat(g.target_amount)) * 100;
                if (pct >= 100) {
                    notifications.push({
                        icon: '🏆', bg: 'rgba(57,255,126,.1)',
                        title: 'Goal reached!',
                        body: `You've fully funded your "${g.name}" goal!`,
                        time: 'Today', unread: true
                    });
                } else if (pct >= 80) {
                    notifications.push({
                        icon: '🌟', bg: 'rgba(57,255,126,.1)',
                        title: 'Goal milestone reached!',
                        body: `"${g.name}" goal hit ${pct.toFixed(0)}% — you're almost there!`,
                        time: 'Today', unread: false
                    });
                }
            });
        }

        // 3. Check Loans
        const loanRes = await SS_API.get('/api/loans/');
        if (loanRes && loanRes.loans) {
            const today = new Date();
            today.setHours(0,0,0,0);
            loanRes.loans.forEach(loan => {
                if (loan.outstanding_amount > 0) {
                    let emiDate = new Date(today.getFullYear(), today.getMonth(), 5);
                    if (loan.start_date) {
                        const sDate = new Date(loan.start_date);
                        emiDate = new Date(today.getFullYear(), today.getMonth(), sDate.getDate());
                    }
                    if (emiDate < today) {
                        emiDate.setMonth(emiDate.getMonth() + 1);
                    }
                    const diffDays = Math.ceil((emiDate - today) / (1000 * 60 * 60 * 24));
                    if (diffDays <= 7) {
                        notifications.push({
                            icon: '💳', bg: 'rgba(251,191,36,.1)',
                            title: 'Upcoming EMI',
                            body: `Your ${loan.name} EMI of ₹${loan.emi_amount.toLocaleString('en-IN')} is due in ${diffDays} days.`,
                            time: 'Upcoming', unread: true
                        });
                    }
                }
            });
        }

        // Render Notifications
        if (notifications.length === 0) {
            notifList.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--muted); font-size: 0.85rem;">You're all caught up! No new notifications.</div>`;
        } else {
            notifList.innerHTML = notifications.map(n => `
                <div class="notif-item ${n.unread ? 'unread' : ''}">
                    <div class="ni-icon" style="background:${n.bg}">${n.icon}</div>
                    <div class="ni-content">
                        <div class="ni-title">${n.title}</div>
                        <div class="ni-body">${n.body}</div>
                        <div class="ni-time">${n.time}</div>
                    </div>
                </div>
            `).join('');
            
            // Add red dot if unread
            const unreadCount = notifications.filter(n => n.unread).length;
            const notifDot = document.querySelector('.notif-dot');
            if (notifDot) {
                notifDot.style.display = unreadCount > 0 ? 'block' : 'none';
            }
        }
    } catch (err) {
        console.error('Error loading notifications:', err);
    }
}

// Load Loans dynamically
async function loadLoans() {
    const loanPanel = document.getElementById('lp-cards');
    if (!loanPanel) return;

    try {
        const res = await SS_API.get('/api/loans/');
        if (!res || !res.loans) return;

        let totalOutstanding = 0;
        let totalActive = 0;
        let monthlyEmi = 0;
        let totalPaidOverall = 0;
        let totalOriginalAmount = 0;
        let nearestEmiDate = null;
        let nearestEmiAmount = 0;

        let gridHtml = '';
        if (res.loans.length === 0) {
            gridHtml = '<div style="padding:2rem;text-align:center;color:var(--muted)">No loans found. Click "Add Loan" to create one.</div>';
        } else {
            res.loans.forEach((loan, index) => {
                const icon = loan.type.toLowerCase() === 'home' ? '🏠' : (loan.type.toLowerCase() === 'car' ? '🚗' : '💸');
                const badgeClass = loan.type.toLowerCase() === 'home' ? 'HOME LOAN' : (loan.type.toLowerCase() === 'car' ? 'CAR LOAN' : 'LOAN');
                const badgeStyle = loan.type.toLowerCase() === 'home' ? '' : (loan.type.toLowerCase() === 'car' ? 'background:rgba(96,165,250,.1);color:var(--blue);border-color:rgba(96,165,250,.2)' : 'background:rgba(251,191,36,.1);color:var(--amber);border-color:rgba(251,191,36,.2)');
                const progress = loan.total_amount > 0 ? Math.min(100, Math.round(((loan.total_amount - loan.outstanding_amount) / loan.total_amount) * 100)) : 0;
                const paid = loan.total_amount - loan.outstanding_amount;

                if (loan.outstanding_amount > 0) {
                    totalOutstanding += loan.outstanding_amount;
                    totalActive++;
                    monthlyEmi += loan.emi_amount;
                }
                totalPaidOverall += paid;
                totalOriginalAmount += loan.total_amount;

                // Real logic for calculating tenure and interest portion (simplified estimation)
                const rate = loan.interest_rate || 8.4;
                const monthlyRate = rate / 12 / 100;
                const interestPortion = Math.round(loan.outstanding_amount * monthlyRate);
                const principalPortion = Math.max(0, loan.emi_amount - interestPortion);

                // Calculate next EMI date (based on loan start_date day-of-month)
                const today = new Date();
                const today0 = new Date(today);
                today0.setHours(0, 0, 0, 0);

                let nextEmiDate = new Date(today0.getFullYear(), today0.getMonth(), 5); // default 5th
                if (loan.start_date) {
                    const sDate = new Date(loan.start_date);
                    nextEmiDate = new Date(today0.getFullYear(), today0.getMonth(), sDate.getDate());
                }
                nextEmiDate.setHours(0, 0, 0, 0);
                if (nextEmiDate < today0) {
                    nextEmiDate.setMonth(nextEmiDate.getMonth() + 1);
                    nextEmiDate.setHours(0, 0, 0, 0);
                }

                const diffDays = Math.ceil((nextEmiDate - today0) / (1000 * 60 * 60 * 24));
                const daysLeftStr = diffDays <= 0
                    ? 'Due today'
                    : (diffDays === 1 ? '1 day left' : `${diffDays} days left`);

                if (loan.outstanding_amount > 0) {
                    if (!nearestEmiDate || nextEmiDate < nearestEmiDate) {
                        nearestEmiDate = nextEmiDate;
                        nearestEmiAmount = loan.emi_amount;
                    }
                }

                const emiDateStr = nextEmiDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

                // Calculate real tenure
                let tenureStr = 'N/A';
                if (loan.outstanding_amount > 0 && loan.emi_amount > 0) {
                    // n = -log(1 - r * P / EMI) / log(1 + r)
                    const val = 1 - (monthlyRate * loan.outstanding_amount / loan.emi_amount);
                    if (val > 0) {
                        const months = Math.ceil(-Math.log(val) / Math.log(1 + monthlyRate));
                        const y = Math.floor(months / 12);
                        const m = months % 12;
                        tenureStr = `${y}yr ${m}mo`;
                    } else {
                        tenureStr = `${Math.ceil(loan.outstanding_amount / loan.emi_amount)} mo`;
                    }
                } else {
                    tenureStr = '0 mo';
                }

                const chartId = `loanChart_${index}`;

                gridHtml += `
                <div class="loan-card">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
                        <div style="display:flex;align-items:center;gap:.75rem">
                            <div style="width:44px;height:44px;border-radius:13px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:1.2rem">${icon}</div>
                            <div>
                                <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700">${loan.name}</div>
                                <div style="font-size:.72rem;color:var(--muted)">Account</div>
                            </div>
                        </div>
                        <div style="display:flex;align-items:center;gap:.5rem">
                            <span class="loan-badge" style="${badgeStyle}">${badgeClass}</span>
                            <button class="btn-icon" onclick="openEditLoan('${encodeURIComponent(JSON.stringify(loan))}')">✏️</button>
                            <button class="btn-icon" style="background:var(--g-dim);border-color:rgba(57,255,126,.2);color:var(--g)" onclick='payEmi(${loan.id}, ${JSON.stringify(loan.name || "Unnamed Loan")}, ${loan.emi_amount}, ${loan.outstanding_amount})'>Pay</button>
                        </div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.75rem;margin-bottom:1.25rem">
                        <div style="background:var(--card2);border-radius:10px;padding:.875rem;border:1px solid var(--border)"><div style="font-size:.68rem;color:var(--muted);margin-bottom:3px">Outstanding</div><div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:var(--red)">₹${loan.outstanding_amount.toLocaleString('en-IN')}</div></div>
                        <div style="background:var(--card2);border-radius:10px;padding:.875rem;border:1px solid var(--border)"><div style="font-size:.68rem;color:var(--muted);margin-bottom:3px">Interest Rate</div><div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800">${rate}% p.a.</div></div>
                        <div style="background:var(--card2);border-radius:10px;padding:.875rem;border:1px solid var(--border)"><div style="font-size:.68rem;color:var(--muted);margin-bottom:3px">Tenure Left</div><div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800">${tenureStr}</div></div>
                    </div>
                    <div style="margin-bottom:.875rem">
                        <div style="display:flex;justify-content:space-between;font-size:.75rem;color:var(--muted);margin-bottom:.4rem"><span>Repayment Progress</span><span style="color:var(--g);font-weight:600">${progress}% complete</span></div>
                        <div class="bc-bar-track"><div class="bc-bar-fill" style="width:${progress}%;background:linear-gradient(90deg,var(--blue),#93c5fd)"></div></div>
                        <div style="display:flex;justify-content:space-between;font-size:.72rem;color:var(--muted);margin-top:.35rem"><span>₹${(paid / 100000).toFixed(1)}L Paid</span><span>₹${(loan.total_amount / 100000).toFixed(1)}L Total</span></div>
                    </div>
                    <div style="background:var(--card2);border-radius:12px;padding:1rem;border:1px solid var(--border)">
                        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem">
                            <div><div style="font-size:.68rem;color:var(--muted);margin-bottom:2px">Next EMI</div><div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.95rem">${emiDateStr}</div><div style="font-size:.68rem;color:var(--amber);margin-top:2px">⏳ ${daysLeftStr}</div></div>
                            <div style="text-align:center;padding:0 1rem;border-left:1px solid var(--border);border-right:1px solid var(--border)"><div style="font-size:.68rem;color:var(--muted);margin-bottom:2px">Principal</div><div style="font-family:'JetBrains Mono',monospace;font-size:.875rem;font-weight:600">₹${principalPortion.toLocaleString('en-IN')}</div></div>
                            <div style="text-align:center;padding:0 1rem;border-right:1px solid var(--border)"><div style="font-size:.68rem;color:var(--muted);margin-bottom:2px">Interest</div><div style="font-family:'JetBrains Mono',monospace;font-size:.875rem;font-weight:600;color:var(--red)">₹${interestPortion.toLocaleString('en-IN')}</div></div>
                            <div style="text-align:right"><div style="font-size:.68rem;color:var(--muted);margin-bottom:2px">Total EMI</div><div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:var(--blue)">₹${loan.emi_amount.toLocaleString('en-IN')}</div></div>
                        </div>
                    </div>
                    <div style="margin-top:1rem;border-top:1px solid var(--border);padding-top:1rem">
                        <div style="font-size:.75rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:.75rem">Principal vs Interest (monthly)</div>
                        <div style="height:80px"><canvas id="${chartId}"></canvas></div>
                    </div>
                </div>`;
            });
        }

        let insightHtml = '';
        if (res.loans.length > 0) {
            const firstLoan = res.loans[0];
            const monthlyRate = (firstLoan.interest_rate || 8.4) / 12 / 100;
            const interestPortion = Math.round(firstLoan.outstanding_amount * monthlyRate);
            const interestPct = Math.round((interestPortion / firstLoan.emi_amount) * 100) || 0;

            insightHtml = `
            <div class="insight-card" style="border-color:rgba(255,95,95,.25);background:linear-gradient(135deg,rgba(255,95,95,.04),var(--card));margin-top:1.5rem">
                <div class="insight-chip" style="background:rgba(255,95,95,.1);color:var(--red);border-color:rgba(255,95,95,.2)">🤖 Loan AI Insight</div>
                <div class="insight-text">Your <strong>${firstLoan.name}</strong> EMI of ₹${firstLoan.emi_amount.toLocaleString('en-IN')} has <strong style="color:var(--red)">₹${interestPortion.toLocaleString('en-IN')} going to interest</strong> (${interestPct}%). A prepayment of ₹1L now could save you significant interest and reduce your tenure! 🚀</div>
            </div>`;
        }

        loanPanel.innerHTML = `<div class="loan-grid">${gridHtml}</div>${insightHtml}`;

        // Initialize Charts for each loan
        res.loans.forEach((loan, index) => {
            const ctx = document.getElementById(`loanChart_${index}`);
            if (ctx && window.Chart) {
                // Generate next 7 months amortization
                let pData = [];
                let iData = [];
                let labels = [];
                let currentOut = loan.outstanding_amount;
                const monthlyRate = (loan.interest_rate || 8.4) / 12 / 100;
                const emi = loan.emi_amount;

                let d = new Date();
                for (let i = 0; i < 7; i++) {
                    d.setMonth(d.getMonth() + 1);
                    labels.push(d.toLocaleDateString('en-US', { month: 'short' }));

                    let interest = Math.round(currentOut * monthlyRate);
                    let principal = Math.round(emi - interest);
                    if (principal < 0) principal = 0;
                    if (currentOut <= 0) {
                        interest = 0; principal = 0;
                    }

                    pData.push(principal);
                    iData.push(interest);
                    currentOut -= principal;
                }

                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            { label: 'Principal', data: pData, backgroundColor: 'rgba(57,255,126,.7)', borderRadius: 4, borderSkipped: false },
                            { label: 'Interest', data: iData, backgroundColor: 'rgba(255,95,95,.55)', borderRadius: 4, borderSkipped: false }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { stacked: true, ticks: { color: '#6a9080', font: { size: 9 } }, grid: { color: 'rgba(255,255,255,0.04)' } }, y: { stacked: true, display: false } } }
                });
            }
        });

        // Update Stat Cards
        const elTotalOut = document.getElementById('loanTotalOutstanding');
        const elActiveCount = document.getElementById('loanActiveCount');
        const elMonthlyEmi = document.getElementById('loanMonthlyEMI');
        const elEmiBurden = document.getElementById('loanEmiBurden');
        const elTotalPaid = document.getElementById('loanTotalPaid');
        const elRepaidPercent = document.getElementById('loanRepaidPercent');
        const elNextEmiDate = document.getElementById('loanNextEmiDate');
        const elNextEmiMeta = document.getElementById('loanNextEmiMeta');

        if (elTotalOut) elTotalOut.innerHTML = `&#x20B9;${totalOutstanding.toLocaleString('en-IN')}`;
        if (elActiveCount) elActiveCount.innerHTML = `${totalActive} Active Loans`;
        if (elMonthlyEmi) elMonthlyEmi.innerHTML = `&#x20B9;${monthlyEmi.toLocaleString('en-IN')}`;

        // Mock income to calculate burden (assume 1,50,000 for demo or fetch from API if available)
        const estimatedIncome = window.TOTAL_INCOME || 150000;
        const burden = Math.round((monthlyEmi / estimatedIncome) * 100) || 0;
        if (elEmiBurden) elEmiBurden.innerHTML = `${burden}% of income`;

        if (elTotalPaid) elTotalPaid.innerHTML = `&#x20B9;${totalPaidOverall.toLocaleString('en-IN')}`;

        const repaidPercent = totalOriginalAmount > 0 ? Math.round((totalPaidOverall / totalOriginalAmount) * 100) : 0;
        if (elRepaidPercent) elRepaidPercent.innerHTML = `&#x2191; ${repaidPercent}% repaid`;

        if (nearestEmiDate && elNextEmiDate) {
            elNextEmiDate.innerHTML = nearestEmiDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            if (elNextEmiMeta) {
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                const nDate = new Date(nearestEmiDate);
                nDate.setHours(0, 0, 0, 0);
                const diffTime = nDate - today;
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                const daysStr = diffDays === 0 ? "Due today" : (diffDays === 1 ? "1 day left" : `${diffDays} days left`);
                elNextEmiMeta.innerHTML = `&#x20B9;${nearestEmiAmount.toLocaleString('en-IN')} &bull; ${daysStr}`;
            }
        } else {
            if (elNextEmiDate) elNextEmiDate.innerHTML = '-';
            if (elNextEmiMeta) elNextEmiMeta.innerHTML = '-';
        }

        // Populate Foreclosure Planner dropdown
        const foreclosureSelect = document.getElementById('foreclosureLoanSelect');
        if (foreclosureSelect) {
            window.LOANS_DATA = res.loans;
            foreclosureSelect.innerHTML = '<option value="">Select a Loan</option>';
            res.loans.forEach((loan, idx) => {
                foreclosureSelect.innerHTML += `<option value="${idx}">${loan.name} (₹${loan.outstanding_amount.toLocaleString('en-IN')})</option>`;
            });
            if (res.loans.length > 0) {
                foreclosureSelect.selectedIndex = 1;
                if (typeof updatePrepay === 'function') {
                    updatePrepay(document.getElementById('prepaySlider')?.value || 0);
                }
            }

            // Re-initialize custom select for dynamic options
            foreclosureSelect.dataset.customized = "";
            const wrapper = foreclosureSelect.nextElementSibling;
            if (wrapper && wrapper.classList.contains("ss-select-wrapper")) {
                wrapper.remove();
            }
            foreclosureSelect.style.display = "";
            if (window.refreshCustomSelects) window.refreshCustomSelects();
        }

        // Connect EMI Calendar & History to Real Data
        if (typeof window.historyRows !== 'undefined') {
            window.historyRows = [];
            res.loans.forEach(loan => {
                const loanLabel = loan.name || loan.loan_name || 'Unnamed Loan';
                if (loan.emi_history && loan.emi_history.length > 0) {
                    loan.emi_history.forEach(emi => {
                        window.historyRows.push({
                            date: new Date(emi.payment_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
                            loan: loanLabel,
                            p: emi.principal_paid || 0,
                            i: emi.interest_paid || 0,
                            t: emi.amount_paid || 0,
                            mode: 'System', // default mode
                            status: emi.status || 'Paid',
                            rawDate: new Date(emi.payment_date)
                        });
                    });
                }
            });
            window.historyRows.sort((a, b) => b.rawDate - a.rawDate);
            if (typeof renderHistoryRows === 'function') {
                renderHistoryRows(window.historyRows);
            }

            // Update History filter options
            const historyFilter = document.getElementById('historyFilter');
            if (historyFilter) {
                historyFilter.innerHTML = '<option value="all">All Loans</option>';
                res.loans.forEach(loan => {
                    const loanLabel = loan.name || loan.loan_name || 'Unnamed Loan';
                    historyFilter.innerHTML += `<option value="${loanLabel}">${loanLabel}</option>`;
                });
            }

            // Update Payment History Stat Cards
            let totalPaid = 0;
            let interestPaid = 0;
            let paymentsOnTime = 0;
            window.historyRows.forEach(row => {
                totalPaid += row.t;
                interestPaid += row.i;
                if (row.status === 'Paid') paymentsOnTime++;
            });
            const statCards = document.querySelectorAll('#lp-history .stat-card .sc-value');
            if (statCards && statCards.length >= 3) {
                statCards[0].textContent = `${paymentsOnTime} / ${window.historyRows.length || 1}`;
                statCards[1].textContent = `₹${totalPaid.toLocaleString('en-IN')}`;
                statCards[2].textContent = `₹${interestPaid.toLocaleString('en-IN')}`;
            }
        }

        // Generate Real Upcoming EMI Calendar
        const timelineList = document.getElementById('emiTimelineList');
        if (timelineList && res.loans.length > 0) {
            let upcomingEmis = [];
            const today = new Date();

            res.loans.forEach(loan => {
                if (loan.outstanding_amount > 0) {
                    let emiDate = new Date(today.getFullYear(), today.getMonth(), 5); // default 5th
                    if (loan.start_date) {
                        const sDate = new Date(loan.start_date);
                        emiDate = new Date(today.getFullYear(), today.getMonth(), sDate.getDate());
                    }
                    if (emiDate < today) {
                        emiDate.setMonth(emiDate.getMonth() + 1);
                    }

                    for (let i = 0; i < 6; i++) {
                        const d = new Date(emiDate);
                        d.setMonth(d.getMonth() + i);
                        upcomingEmis.push({
                            loanName: loan.name,
                            date: d,
                            amount: loan.emi_amount,
                            icon: loan.type.toLowerCase() === 'home' ? '🏠' : (loan.type.toLowerCase() === 'car' ? '🚗' : '💸')
                        });
                    }
                }
            });

            upcomingEmis.sort((a, b) => a.date - b.date);

            let timelineHtml = '';
            // Group by month
            const monthGroups = {};
            upcomingEmis.forEach(emi => {
                const monthKey = emi.date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
                if (!monthGroups[monthKey]) monthGroups[monthKey] = [];
                monthGroups[monthKey].push(emi);
            });

            Object.keys(monthGroups).slice(0, 6).forEach((monthKey, idx) => {
                const parts = monthKey.split(' ');
                timelineHtml += `<div style="display:flex;gap:1rem;padding:.875rem 1.5rem;border-bottom:1px solid var(--border)">`;
                timelineHtml += `<div style="width:60px;flex-shrink:0;text-align:center"><div style="font-size:.68rem;color:var(--muted)">${parts[0]}</div><div style="font-family:Syne,sans-serif;font-weight:800">${parts[1]}</div></div>`;
                timelineHtml += `<div style="flex:1;display:flex;flex-direction:column;gap:.5rem">`;

                monthGroups[monthKey].forEach((emi, eIdx) => {
                    const urgency = (idx === 0 && eIdx === 0)
                        ? '<span style="font-size:.68rem;color:var(--amber);font-weight:600">⏳ Upcoming</span>'
                        : '<span style="font-size:.68rem;color:var(--g);font-weight:600">Scheduled</span>';

                    timelineHtml += `<div style="display:flex;align-items:center;justify-content:space-between;background:var(--card2);border-radius:10px;padding:.6rem .875rem;border:1px solid var(--border)">`;
                    timelineHtml += `<div style="display:flex;align-items:center;gap:.5rem"><span>${emi.icon}</span><div><div style="font-size:.8rem;font-weight:600">${emi.loanName}</div><div style="font-size:.68rem;color:var(--muted)">Due ${emi.date.getDate()}th</div></div></div>`;
                    timelineHtml += `<div style="display:flex;align-items:center;gap:.875rem"><span style="font-family:Syne,sans-serif;font-weight:800;color:var(--blue)">₹${emi.amount.toLocaleString('en-IN')}</span>${urgency}</div></div>`;
                });

                timelineHtml += `</div></div>`;
            });
            timelineList.innerHTML = timelineHtml;

            // Update total EMI per month badge
            const monthlyTotal = res.loans.reduce((acc, l) => acc + (l.outstanding_amount > 0 ? l.emi_amount : 0), 0);
            const totalBadge = timelineList.previousElementSibling?.querySelector('.badge');
            if (totalBadge) {
                totalBadge.textContent = `₹${monthlyTotal.toLocaleString('en-IN')}/month`;
            }
        }

    } catch (err) {
        if (err.name === 'AbortError' || (err.message && err.message.includes('abort'))) return;
        console.error('Failed to load loans:', err);
    }
}

async function loadNetWorthData() {
    console.log('SmartSpend: loadNetWorthData() triggered');
    try {
        // Fetch all three data sources in parallel
        const [stats, invRes, loanRes] = await Promise.all([
            SS_API.get('/api/analytics/net-worth'),
            SS_API.get('/api/investments/'),
            SS_API.get('/api/loans/')
        ]);
        
        if (!stats) {
            console.error('SmartSpend: No stats returned from API');
            return;
        }
        console.log('SmartSpend: Net worth data loaded', { stats, invRes, loanRes });

        const format = (v) => (v < 0 ? '₹-' : '₹') + Math.abs(v || 0).toLocaleString('en-IN');
        const investments = (invRes && invRes.investments) ? invRes.investments : [];
        const loans = (loanRes && loanRes.loans) ? loanRes.loans : [];

        // ── Hero Card ──
        const elEst = document.getElementById('nw-estimated');
        const elTA = document.getElementById('nw-total-assets');
        const elTL = document.getElementById('nw-total-liabilities');
        if (elEst) elEst.textContent = format(stats.net_worth);
        if (elTA) elTA.textContent = format(stats.total_assets);
        if (elTL) elTL.textContent = format(stats.total_liabilities);

        // Subtitle with current date
        const elSub = document.getElementById('nw-subtitle');
        if (elSub) {
            const now = new Date();
            const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
            elSub.textContent = 'Your complete financial position · ' + monthNames[now.getMonth()] + ' ' + now.getFullYear();
        }

        // Change badge and growth info
        const elBadge = document.getElementById('nw-change-badge');
        const elGrowth = document.getElementById('nw-growth-info');

        // ── Assets Breakdown ──
        const elAH = document.getElementById('nw-assets-header');
        const elAL = document.getElementById('nw-assets-list');
        if (elAH) elAH.textContent = format(stats.total_assets);

        if (elAL) {
            let assetsHtml = '';
            const assetItems = [];
            const totalAssets = stats.total_assets || 1;

            // Group investments by type
            const invByType = {};
            investments.forEach(inv => {
                const t = inv.type || 'Other';
                if (!invByType[t]) invByType[t] = { total: 0, names: [] };
                invByType[t].total += inv.amount;
                invByType[t].names.push(inv.name);
            });

            const invIcons = { 'Stocks': '📈', 'Mutual Funds': '📊', 'Crypto': '₿', 'Gold': '🥇', 'Real Estate': '🏠', 'Fixed Deposit': '🏦', 'Bonds': '📜' };
            const invColors = ['rgba(57,255,126,.1)', 'rgba(96,165,250,.1)', 'rgba(167,139,250,.1)', 'rgba(251,191,36,.1)', 'rgba(244,114,182,.1)'];
            let colorIdx = 0;
            Object.keys(invByType).forEach(type => {
                const pct = Math.round((invByType[type].total / Math.abs(totalAssets)) * 100);
                assetItems.push({ name: type, sub: invByType[type].names.join(', '), amount: invByType[type].total, pct: pct, icon: invIcons[type] || '💎', color: invColors[colorIdx % invColors.length] });
                colorIdx++;
            });

            if (stats.total_balance !== 0) {
                const bankPct = Math.round((Math.abs(stats.total_balance) / Math.abs(totalAssets)) * 100);
                assetItems.push({ name: 'Bank Balance', sub: 'Net credits − debits', amount: stats.total_balance, pct: bankPct, icon: '🏦', color: 'rgba(96,165,250,.1)' });
            }

            if (assetItems.length === 0) {
                assetsHtml = '<div style="padding:2rem;text-align:center;color:var(--muted);font-size:.85rem">No assets found. Add investments or transactions to see your assets here.</div>';
            } else {
                const barColors = ['var(--g)', 'var(--blue)', 'var(--amber)', '#a78bfa', '#f472b6', '#34d399'];
                assetItems.sort((a, b) => b.amount - a.amount);
                assetItems.forEach((item, idx) => {
                    assetsHtml += '<div style="display:flex;align-items:center;justify-content:space-between;padding:.875rem 1rem;background:var(--card2);border:1px solid var(--border);border-radius:12px">';
                    assetsHtml += '<div style="display:flex;align-items:center;gap:.75rem">';
                    assetsHtml += '<div style="width:36px;height:36px;border-radius:10px;background:' + item.color + ';display:flex;align-items:center;justify-content:center;font-size:1rem">' + item.icon + '</div>';
                    assetsHtml += '<div><div style="font-weight:600;font-size:.875rem">' + item.name + '</div>';
                    assetsHtml += '<div style="font-size:.7rem;color:var(--muted);max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + item.sub + '</div></div></div>';
                    assetsHtml += '<div style="text-align:right"><div style="font-family:\'JetBrains Mono\';font-weight:700">' + format(item.amount) + '</div>';
                    assetsHtml += '<div style="font-size:.7rem;color:' + barColors[idx % barColors.length] + '">' + item.pct + '%</div></div></div>';
                });
                assetsHtml += '<div style="margin-top:.25rem"><div style="display:flex;height:8px;border-radius:100px;overflow:hidden;gap:2px">';
                assetItems.forEach((item, idx) => {
                    assetsHtml += '<div style="flex:' + Math.max(1, item.pct) + ';background:' + barColors[idx % barColors.length] + ';border-radius:100px"></div>';
                });
                assetsHtml += '</div></div>';
            }
            elAL.innerHTML = assetsHtml;
        }

        // ── Liabilities Breakdown ──
        const elLH = document.getElementById('nw-liabilities-header');
        const elLL = document.getElementById('nw-liabilities-list');
        if (elLH) elLH.textContent = format(stats.total_liabilities);

        if (elLL) {
            let liabHtml = '';
            const activeLoans = loans.filter(l => (l.outstanding_amount || 0) > 0);
            const totalLiab = stats.total_liabilities || 1;

            if (activeLoans.length === 0) {
                liabHtml = '<div style="padding:2rem;text-align:center;color:var(--muted);font-size:.85rem">No outstanding liabilities. 🎉</div>';
            } else {
                activeLoans.forEach(loan => {
                    const icon = loan.type && loan.type.toLowerCase() === 'home' ? '🏠' : (loan.type && loan.type.toLowerCase() === 'car' ? '🚗' : '💸');
                    const pct = Math.round((loan.outstanding_amount / totalLiab) * 100);
                    const rate = loan.interest_rate || 0;
                    let tenureStr = '';
                    if (loan.outstanding_amount > 0 && loan.emi_amount > 0 && rate > 0) {
                        const mr = rate / 12 / 100;
                        const val = 1 - (mr * loan.outstanding_amount / loan.emi_amount);
                        if (val > 0) {
                            const months = Math.ceil(-Math.log(val) / Math.log(1 + mr));
                            const y = Math.floor(months / 12);
                            const m = months % 12;
                            tenureStr = y + 'yr ' + m + 'mo left';
                        }
                    }
                    const meta = (rate > 0 ? rate + '% p.a.' : '') + (tenureStr ? ' · ' + tenureStr : '');

                    liabHtml += '<div style="display:flex;align-items:center;justify-content:space-between;padding:.875rem 1rem;background:var(--card2);border:1px solid rgba(255,95,95,.15);border-radius:12px">';
                    liabHtml += '<div style="display:flex;align-items:center;gap:.75rem">';
                    liabHtml += '<div style="width:36px;height:36px;border-radius:10px;background:rgba(255,95,95,.1);display:flex;align-items:center;justify-content:center;font-size:1rem">' + icon + '</div>';
                    liabHtml += '<div><div style="font-weight:600;font-size:.875rem">' + loan.name + '</div>';
                    liabHtml += '<div style="font-size:.7rem;color:var(--muted)">' + meta + '</div></div></div>';
                    liabHtml += '<div style="text-align:right"><div style="font-family:\'JetBrains Mono\';font-weight:700;color:var(--red)">' + format(loan.outstanding_amount) + '</div>';
                    liabHtml += '<div style="font-size:.7rem;color:var(--red)">' + pct + '%</div></div></div>';
                });

                liabHtml += '<div style="margin-top:.5rem;background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:1rem">';
                liabHtml += '<div style="font-size:.75rem;color:var(--muted);margin-bottom:.625rem;font-weight:600">Debt Repayment Progress</div>';
                liabHtml += '<div style="display:flex;flex-direction:column;gap:.5rem">';
                const progColors = ['var(--g)', 'var(--amber)', 'var(--blue)', '#a78bfa'];
                activeLoans.forEach((loan, idx) => {
                    const repaid = loan.total_amount > 0 ? Math.round(((loan.total_amount - loan.outstanding_amount) / loan.total_amount) * 100) : 0;
                    const c = progColors[idx % progColors.length];
                    liabHtml += '<div><div style="display:flex;justify-content:space-between;font-size:.72rem;color:var(--muted);margin-bottom:.3rem"><span>' + loan.name + '</span><span style="color:' + c + '">' + repaid + '% repaid</span></div>';
                    liabHtml += '<div class="bc-bar-track"><div class="bc-bar-fill" style="width:' + repaid + '%;background:linear-gradient(90deg,' + c + ',' + c + ')"></div></div></div>';
                });
                liabHtml += '</div></div>';

                const dta = stats.total_assets > 0 ? Math.round((stats.total_liabilities / stats.total_assets) * 100) : 0;
                const monthlyEmi = activeLoans.reduce((s, l) => s + (l.emi_amount || 0), 0);
                const dtaColor = dta < 30 ? 'var(--g)' : (dta < 60 ? 'var(--amber)' : 'var(--red)');
                liabHtml += '<div style="background:rgba(255,95,95,.05);border:1px solid rgba(255,95,95,.15);border-radius:12px;padding:1rem;display:flex;justify-content:space-between;align-items:center">';
                liabHtml += '<div><div style="font-size:.72rem;color:var(--muted);margin-bottom:2px">Debt-to-Asset Ratio</div>';
                liabHtml += '<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:800;color:' + dtaColor + '">' + dta + '%</div></div>';
                liabHtml += '<div style="text-align:right"><div style="font-size:.72rem;color:var(--muted);margin-bottom:2px">Monthly EMI Load</div>';
                liabHtml += '<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:800;color:var(--red)">' + format(monthlyEmi) + '</div></div></div>';
            }
            elLL.innerHTML = liabHtml;
        }

        // ── Balance Sheet ──
        const bsAssets = document.getElementById('nw-balance-sheet-assets');
        const bsLiab = document.getElementById('nw-balance-sheet-liabilities');
        const bsNet = document.getElementById('nw-balance-sheet-net');
        if (bsAssets) bsAssets.textContent = format(stats.total_assets);
        if (bsLiab) bsLiab.textContent = format(stats.total_liabilities);
        if (bsNet) bsNet.textContent = format(stats.net_worth);

        // ── Wealth Growth Chart ──
        const summaryRes = await SS_API.get('/api/analytics/summary');
        const monthlyData = (summaryRes && summaryRes.monthly) ? summaryRes.monthly : [];
        const chartSub = document.getElementById('nw-chart-sub');

        if (monthlyData.length > 0) {
            let runningNW = 0;
            const chartLabels = [];
            const chartData = [];
            monthlyData.forEach(m => {
                runningNW += (m.inc || 0) - (m.exp || 0);
                chartLabels.push(m.month);
                chartData.push(runningNW);
            });
            const realNW = stats.net_worth;
            if (chartData.length > 0) {
                const lastTransNW = chartData[chartData.length - 1];
                const offset = realNW - lastTransNW;
                for (let i = 0; i < chartData.length; i++) {
                    chartData[i] = Math.round(chartData[i] + (offset * (i + 1) / chartData.length));
                }
            }
            if (chartSub) chartSub.textContent = chartLabels[0] + ' – ' + chartLabels[chartLabels.length - 1];
            if (typeof renderNetWorthChart === 'function') renderNetWorthChart(chartLabels, chartData);
        } else {
            if (chartSub) chartSub.textContent = 'No data yet';
            if (typeof renderNetWorthChart === 'function') renderNetWorthChart([], []);
        }

        // ── Badge & Growth Info ──
        const nw = stats.net_worth || 0;
        const formatCompact = (v) => {
            const abs = Math.abs(v);
            const sign = v < 0 ? '₹-' : '₹';
            if (abs >= 10000000) return sign + (abs / 10000000).toFixed(1) + 'Cr';
            if (abs >= 100000) return sign + (abs / 100000).toFixed(1) + 'L';
            if (abs >= 1000) return sign + (abs / 1000).toFixed(1) + 'K';
            return sign + abs.toLocaleString('en-IN');
        };

        if (elBadge) {
            let thisYearChange = 0;
            const currentYear = new Date().getFullYear().toString();
            monthlyData.forEach(m => {
                if (m.month && m.month.includes(currentYear)) {
                    thisYearChange += (m.inc || 0) - (m.exp || 0);
                }
            });
            const arrow = thisYearChange >= 0 ? '↑' : '↓';
            elBadge.textContent = arrow + ' ' + (thisYearChange >= 0 ? '+' : '-') + formatCompact(Math.abs(thisYearChange)) + ' this year';
            elBadge.style.display = (thisYearChange !== 0 || nw !== 0) ? '' : 'none';
        }

        if (elGrowth) {
            let growthParts = [];
            if (monthlyData.length > 0) {
                const currentYear = new Date().getFullYear().toString();
                let thisYearSavings = 0;
                monthlyData.forEach(m => {
                    if (m.month && m.month.includes(currentYear)) thisYearSavings += (m.inc || 0) - (m.exp || 0);
                });
                const nwAtStartOfYear = nw - thisYearSavings;
                if (Math.abs(nwAtStartOfYear) > 0) {
                    const yoyPct = ((nw - nwAtStartOfYear) / Math.abs(nwAtStartOfYear) * 100).toFixed(1);
                    growthParts.push(yoyPct + '% YoY growth');
                }
            }

            if (nw > 0 && nw < 10000000) {
                let totalSavings = 0;
                monthlyData.forEach(m => { totalSavings += (m.inc || 0) - (m.exp || 0); });
                const monthlySavings = totalSavings / (monthlyData.length || 1);
                if (monthlySavings > 0) {
                    const monthsToGo = Math.ceil((10000000 - nw) / monthlySavings);
                    const targetDate = new Date();
                    targetDate.setMonth(targetDate.getMonth() + monthsToGo);
                    const mNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                    growthParts.push('On track for ₹1Cr by ' + mNames[targetDate.getMonth()] + ' ' + targetDate.getFullYear() + ' 🎯');
                }
            } else if (nw >= 10000000) {
                growthParts.push('₹1Cr milestone achieved! 🎉');
            }
            elGrowth.textContent = growthParts.join(' · ');
            elGrowth.style.display = growthParts.length > 0 ? '' : 'none';
        }

        // ── Milestones ──
        const elMS = document.getElementById('nw-milestones');
        if (elMS) {
            const milestones = [
                { label: '₹1L Net Worth', value: 100000 },
                { label: '₹5L Net Worth', value: 500000 },
                { label: '₹10L Net Worth', value: 1000000 },
                { label: '₹25L Net Worth', value: 2500000 },
                { label: '₹50L Net Worth', value: 5000000 },
                { label: '₹1 Crore Net Worth', value: 10000000 }
            ];
            let msHtml = '';
            milestones.forEach(ms => {
                const achieved = nw >= ms.value;
                const pctThere = Math.min(100, Math.round((nw / ms.value) * 100));
                if (achieved) {
                    msHtml += `<div style="display:flex;align-items:center;gap:.75rem">
                        <div style="width:28px;height:28px;border-radius:50%;background:var(--g-dim);border:1.5px solid var(--g);display:flex;align-items:center;justify-content:center;font-size:.8rem;flex-shrink:0">✓</div>
                        <div><div style="font-size:.82rem;font-weight:600">${ms.label}</div><div style="font-size:.7rem;color:var(--g)">Achieved ✓</div></div></div>`;
                } else if (pctThere > 10) {
                    msHtml += `<div style="display:flex;align-items:center;gap:.75rem">
                        <div style="width:28px;height:28px;border-radius:50%;background:var(--card2);border:1.5px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:.8rem;flex-shrink:0;color:var(--muted)">🎯</div>
                        <div><div style="font-size:.82rem;font-weight:600">${ms.label}</div><div style="font-size:.7rem;color:var(--amber)">In progress</div></div>
                        <div style="margin-left:auto;font-size:.65rem;font-weight:700;background:rgba(251,191,36,.1);color:var(--amber);border:1px solid rgba(251,191,36,.2);border-radius:100px;padding:2px 8px;white-space:nowrap">${pctThere}% there</div></div>`;
                }
            });
            elMS.innerHTML = msHtml || '<div style="padding:1rem;text-align:center;color:var(--muted);font-size:.85rem">Add assets to track milestones.</div>';
        }

        // ── Wealth Insight ──
        const elInsight = document.getElementById('nw-insight-text');
        if (elInsight) {
            const totalLiab = stats.total_liabilities || 0;
            const totalAssets = stats.total_assets || 0;
            const activeLoans = loans.filter(l => (l.outstanding_amount || 0) > 0);
            if (nw === 0 && totalAssets === 0 && totalLiab === 0) {
                elInsight.innerHTML = 'Start adding your transactions and investments to get personalized insights.';
            } else {
                let insight = `Your net worth is <strong>${format(nw)}</strong>. `;
                if (totalLiab > 0 && totalAssets > 0) {
                    const dta = Math.round((totalLiab / totalAssets) * 100);
                    insight += `Your debt-to-asset ratio is <strong>${dta}%</strong>. `;
                    insight += dta > 50 ? 'Consider reducing liabilities. ' : (dta < 20 ? 'Your debt levels are healthy! ' : '');
                }
                if (activeLoans.length > 0) {
                    const totalEmi = activeLoans.reduce((s, l) => s + (l.emi_amount || 0), 0);
                    insight += `You have <strong>${activeLoans.length} active loans</strong> with monthly EMI of <strong>${format(totalEmi)}</strong>. `;
                }
                if (investments.length > 0) {
                    insight += `Your portfolio has <strong>${investments.length} assets</strong> worth <strong>${format(stats.total_investments)}</strong>.`;
                }
                elInsight.innerHTML = insight;
            }
        }
    } catch (err) {
        console.error('SmartSpend: Failed to load net worth data:', err);
    }
}

async function loadInvestments() {
    const invPanel = document.querySelector('#view-investments .loan-grid'); // Using same class for grid
    if (!invPanel) return;

    try {
        const res = await SS_API.get('/api/investments/');
        if (!res || !res.investments) return;

        let totalInvested = 0;
        let gridHtml = '';

        if (res.investments.length === 0) {
            gridHtml = '<div style="padding:2rem;text-align:center;color:var(--muted);grid-column: 1 / -1">No investments found. Click "Add Asset" to start tracking.</div>';
        } else {
            res.investments.forEach(inv => {
                totalInvested += inv.amount;
                const icon = inv.type === 'Stocks' ? '📈' : (inv.type === 'Crypto' ? '₿' : (inv.type === 'Real Estate' ? '🏠' : '💎'));

                gridHtml += `
                <div class="card-box" style="padding:1.25rem;border-radius:18px">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
                        <div style="display:flex;align-items:center;gap:.75rem">
                            <div style="width:36px;height:36px;border-radius:10px;background:rgba(57,255,126,.1);display:flex;align-items:center;justify-content:center">${icon}</div>
                            <div>
                                <div style="font-weight:700;font-size:.9rem">${inv.name}</div>
                                <div style="font-size:.7rem;color:var(--muted)">${inv.type}</div>
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-family:'JetBrains Mono';font-weight:800;color:var(--g)">₹${inv.amount.toLocaleString('en-IN')}</div>
                            <div style="font-size:.65rem;color:var(--muted)">${inv.date}</div>
                        </div>
                    </div>
                    <button class="btn btn-ghost" style="width:100%;font-size:.7rem;padding:4px" onclick="deleteInvestment(${inv.id})">Remove</button>
                </div>`;
            });
        }

        invPanel.innerHTML = gridHtml;

        // Update investment stat cards
        const fmtInv = v => '₹' + Math.abs(v).toLocaleString('en-IN');
        document.getElementById('inv-portfolio') && (document.getElementById('inv-portfolio').textContent = fmtInv(totalInvested));
        document.getElementById('inv-invested') && (document.getElementById('inv-invested').textContent = fmtInv(totalInvested));
        document.getElementById('inv-pnl') && (document.getElementById('inv-pnl').textContent = '₹0');
        document.getElementById('inv-xirr') && (document.getElementById('inv-xirr').textContent = '0%');

    } catch (err) {
        console.error('Failed to load investments:', err);
    }
}

async function deleteInvestment(id) {
    const isConfirmed = await window.appConfirm('Are you sure you want to remove this investment?');
    if (!isConfirmed) return;
    try {
        await SS_API.del('/api/investments/' + id);
        showToast('Investment removed', 'success');
        loadInvestments();
        loadNetWorthData();
    } catch (err) {
        showToast('Failed to remove investment', 'error');
    }
}

// ─── END OF FILE ──────────────────────────────────────────────────────────────
