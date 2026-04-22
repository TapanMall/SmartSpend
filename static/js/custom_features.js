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
    </style>
    `;
    document.body.insertAdjacentHTML('beforeend', modalsHtml);
})();

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
    const modal = document.getElementById('budgetModal');
    if (modal) modal.classList.add('open');
    
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
    if (modal) modal.classList.remove('open');
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
            document.getElementById('createFirstBudgetBtn')?.addEventListener('click', openBudgetModal);
            return;
        }
        
        const catEmojis = { 'Food & Dining': '🍕', 'Transport': '🚗', 'Shopping': '🛍️', 'Entertainment': '🎬', 'Health': '🏥', 'Bills & Utilities': '📱', 'Others': '📝' };
        const colors = ['#39ff7e', '#fbbf24', '#60a5fa', '#ff5f5f', '#a78bfa', '#34d399', '#f472b6'];
        
        grid.innerHTML = budgets.map((b, i) => {
            const emoji = catEmojis[b.category] || '📊';
            const color = colors[i % colors.length];
            const spent = 0; // Would need transactions data per category
            const limit = parseFloat(b.amount);
            const pct = Math.min(100, (spent / limit) * 100);
            const remaining = limit - spent;
            
            return `
            <div class="budget-card">
                <div class="bc-top">
                    <div class="bc-cat-info">
                        <div class="bc-emoji" style="background:${color}22">${emoji}</div>
                        <div>
                            <div class="bc-name">${b.category}</div>
                            <div style="font-size:.7rem;color:var(--muted)">Monthly</div>
                        </div>
                    </div>
                    <div class="bc-pct" style="color:${pct > 80 ? 'var(--red)' : 'var(--g)'}">${pct.toFixed(0)}%</div>
                </div>
                <div class="bc-bar-track">
                    <div class="bc-bar-fill" style="width:${pct}%;background:${pct > 80 ? 'var(--red)' : color}"></div>
                </div>
                <div class="bc-amounts">
                    <div>
                        <div class="bc-spent" style="color:${pct > 80 ? 'var(--red)' : 'var(--text)'}">₹${spent.toLocaleString('en-IN')} spent</div>
                        <div class="bc-remaining">₹${remaining.toLocaleString('en-IN')} remaining</div>
                    </div>
                    <div class="bc-limit">₹${limit.toLocaleString('en-IN')}</div>
                </div>
            </div>`;
        }).join('');

        // Update budget summary totals
        const totalBudget = budgets.reduce((s, b) => s + parseFloat(b.amount), 0);
        const budTotalEl = document.getElementById('budTotal');
        const budRemEl = document.getElementById('budRemTotal');
        if (budTotalEl) budTotalEl.textContent = '₹' + totalBudget.toLocaleString('en-IN');
        if (budRemEl) budRemEl.textContent = '₹' + totalBudget.toLocaleString('en-IN');
        
    } catch (err) {
        console.error('Load budgets error:', err);
    }
}

// ─── GOAL MODAL ──────────────────────────────────────────────────────────────
function openGoalModal() {
    const modal = document.getElementById('goalModal');
    if (modal) modal.classList.add('open');
    document.getElementById('goalNameInput')?.focus();
}
function closeGoalModal() {
    const modal = document.getElementById('goalModal');
    if (modal) modal.classList.remove('open');
    ['goalNameInput', 'goalTargetInput', 'goalCurrentInput'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
    });
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
        
        grid.innerHTML = `<div class="goals-grid">` + goals.map((g, i) => {
            const pct = Math.min(100, (parseFloat(g.current_amount || 0) / parseFloat(g.target_amount)) * 100);
            const color = goalColors[i % goalColors.length];
            const emoji = goalEmojis[i % goalEmojis.length];
            const remaining = parseFloat(g.target_amount) - parseFloat(g.current_amount || 0);
            
            return `
            <div class="goal-card">
                <div class="gc-header">
                    <div class="gc-icon" style="background:${color}22">${emoji}</div>
                    <div>
                        <div class="gc-name">${g.name}</div>
                        <div class="gc-deadline">₹${remaining.toLocaleString('en-IN')} to go</div>
                    </div>
                </div>
                <div class="gc-progress">
                    <div class="gc-bar-track">
                        <div class="gc-bar-fill" style="width:${pct}%;background:${color}"></div>
                    </div>
                    <div class="gc-amounts">
                        <div class="gc-current" style="color:${color}">₹${parseFloat(g.current_amount||0).toLocaleString('en-IN')}</div>
                        <div class="gc-target" style="color:var(--muted)">₹${parseFloat(g.target_amount).toLocaleString('en-IN')}</div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;justify-content:space-between;margin-top:.75rem">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:700;color:${color}">${pct.toFixed(1)}%</div>
                    <div style="font-size:.72rem;color:var(--muted)">Complete</div>
                </div>
            </div>`;
        }).join('') + `</div>`;
        
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
    }
});

// Load Loans dynamically
async function loadLoans() {
    const loanPanel = document.getElementById('lp-cards');
    if (!loanPanel) return;
    
    try {
        const res = await SS_API.get('/api/loans/');
        if (!res || !res.loans) return;
        
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
                
                // Real logic for calculating tenure and interest portion (simplified estimation)
                const rate = loan.interest_rate || 8.4;
                const monthlyRate = rate / 12 / 100;
                const interestPortion = Math.round(loan.outstanding_amount * monthlyRate);
                const principalPortion = Math.max(0, loan.emi_amount - interestPortion);
                
                let tenureMonths = 0;
                if (principalPortion > 0) {
                    tenureMonths = Math.log(loan.emi_amount / (loan.emi_amount - loan.outstanding_amount * monthlyRate)) / Math.log(1 + monthlyRate);
                }
                const yearsLeft = Math.floor(tenureMonths / 12) || 0;
                const monthsLeft = Math.round(tenureMonths % 12) || 0;
                const tenureStr = yearsLeft > 0 ? `${yearsLeft}yr ${monthsLeft}mo` : `${monthsLeft}mo`;
                
                const nextEmiDate = new Date();
                nextEmiDate.setDate(nextEmiDate.getDate() + 15); // mock 15 days left
                const emiDateStr = nextEmiDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                
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
                            <button class="btn-icon" style="background:var(--g-dim);border-color:rgba(57,255,126,.2);color:var(--g)" onclick="payEmi(${loan.id}, '${loan.name}', ${loan.emi_amount}, ${loan.outstanding_amount})">Pay</button>
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
                        <div style="display:flex;justify-content:space-between;font-size:.72rem;color:var(--muted);margin-top:.35rem"><span>₹${(paid/100000).toFixed(1)}L Paid</span><span>₹${(loan.total_amount/100000).toFixed(1)}L Total</span></div>
                    </div>
                    <div style="background:var(--card2);border-radius:12px;padding:1rem;border:1px solid var(--border)">
                        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem">
                            <div><div style="font-size:.68rem;color:var(--muted);margin-bottom:2px">Next EMI</div><div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.95rem">${emiDateStr}</div><div style="font-size:.68rem;color:var(--amber);margin-top:2px">⏳ 15 days left</div></div>
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
                const principalData = [13700, 13800, 13900, 14000, 14100, 14200, 14300];
                const interestData = [29100, 29000, 28900, 28800, 28700, 28600, 28500];
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr'],
                        datasets: [
                            { label: 'Principal', data: principalData, backgroundColor: 'rgba(57,255,126,.7)', borderRadius: 4, borderSkipped: false },
                            { label: 'Interest', data: interestData, backgroundColor: 'rgba(255,95,95,.55)', borderRadius: 4, borderSkipped: false }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { stacked: true, ticks: { color: '#6a9080', font: { size: 9 } }, grid: { color: 'rgba(255,255,255,0.04)' } }, y: { stacked: true, display: false } } }
                });
            }
        });

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
        
    } catch (err) {
        if (err.name === 'AbortError' || (err.message && err.message.includes('abort'))) return;
        console.error('Failed to load loans:', err);
    }
}
