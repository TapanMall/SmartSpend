import codecs
import re
import traceback

try:
    with codecs.open('templates/Dashboard.html', 'r', 'utf-8') as f:
        content = f.read()

    # 1. switchView addition
    if "if (viewId === 'budget')" not in content:
        switch_view_code = """
            if (viewId === 'budget') renderBudgets();
            if (viewId === 'goals') renderGoals();
            if (viewId === 'dashboard') renderDashboardDoughnut();
        """
        content = content.replace("if (viewId === 'dashboard') renderDashboardDoughnut();", switch_view_code)

    # 2. Main Budget/Goal JS Block
    budget_goals_js = """
        let BUDGETS = [];
        let GOALS = [];

        async function loadBudgets() {
            const data = await SS_API.get('/api/budgets/');
            if (!data) return;
            BUDGETS = data.budgets || [];
            const countEl = document.getElementById('budCountTotal');
            if (countEl) countEl.textContent = BUDGETS.length;
            renderBudgets();
        }

        function renderBudgets() {
            const dashGrid = document.getElementById('dashBudgetList');
            if (dashGrid) {
                if (BUDGETS.length === 0) {
                    dashGrid.innerHTML = '<div style="padding:2rem;text-align:center;color:var(--muted);font-size:0.8rem">No active budgets</div>';
                } else {
                    dashGrid.innerHTML = '<div style="padding:1rem;text-align:center;color:var(--muted);font-size:0.8rem">' + BUDGETS.length + ' budgets active</div>';
                }
            }

            const grid = document.getElementById('budgetGrid');
            if (!grid) return;
            
            // Set style
            grid.style.display = 'grid';
            if (BUDGETS.length === 0) {
                grid.style.display = 'block';
                grid.innerHTML = `
                <div style="grid-column:1/-1;padding:4rem;text-align:center;background:var(--card);border-radius:var(--r-md);border:1px dashed var(--border)">
                    <div style="font-size:3rem;margin-bottom:1.5rem">🎯</div>
                    <h3 style="font-family:'Syne',sans-serif;font-size:1.25rem;margin-bottom:.5rem">No Budgets Set</h3>
                    <p style="color:var(--muted);font-size:.875rem;max-width:300px;margin:0 auto 1.5rem">Track your spending by setting monthly limits for categories.</p>
                    <button class="btn btn-primary" style="margin:0 auto" id="createFirstBudgetBtn" onclick="addBudget()">+ Create Your First Budget</button>
                </div>`;
                return;
            }

            const cats = {};
            TRANSACTIONS.forEach(t => {
                const tType = (t.type || '').toLowerCase();
                const amt = t.amount || t.amt || 0;
                const cat = t.category || t.cat || '';
                if (tType === 'expense' || tType === 'debit') {
                    cats[cat] = (cats[cat] || 0) + Math.abs(amt);
                }
            });

            let totalBud = 0;
            let totalSpent = 0;

            grid.innerHTML = BUDGETS.map(b => {
                const limit = parseFloat(b.amount);
                const spent = cats[b.category] || 0;
                totalBud += limit;
                totalSpent += spent;
                const pct = Math.min(100, (spent / limit) * 100);
                const color = pct > 90 ? 'var(--red)' : (pct > 75 ? 'var(--amber)' : 'var(--g)');
                
                return `
                <div class="budget-item" style="background:var(--card);padding:1.5rem;border-radius:var(--r-md);border:1px solid var(--border)">
                    <div class="budget-top" style="display:flex;justify-content:space-between;margin-bottom:1rem">
                        <div class="budget-cat" style="font-weight:600">${b.category}</div>
                        <div class="budget-nums" style="font-family:'Syne',sans-serif;font-size:1.1rem">₹${spent.toLocaleString('en-IN')} / ₹${limit.toLocaleString('en-IN')}</div>
                    </div>
                    <div class="progress-track" style="height:8px;background:var(--card2);border-radius:4px;overflow:hidden">
                        <div class="progress-fill" style="width:${pct}%;background:${color};height:100%;border-radius:4px;transition:width 0.5s ease"></div>
                    </div>
                </div>`;
            }).join('');

            const bt = document.getElementById('budTotal');
            const bs = document.getElementById('budSpent');
            const br = document.getElementById('budRemTotal');
            if (bt) bt.textContent = '₹' + totalBud.toLocaleString('en-IN');
            if (bs) bs.textContent = '₹' + totalSpent.toLocaleString('en-IN');
            
            const rem = totalBud - totalSpent;
            if (br) br.textContent = '₹' + (rem > 0 ? rem : 0).toLocaleString('en-IN');
        }

        async function addBudget() {
            const cat = prompt("Enter Budget Category (e.g., Food & Dining, Travel, Shopping):");
            if (!cat) return;
            const amtStr = prompt("Enter Monthly Limit Amount (₹):");
            if (!amtStr) return;
            const amt = parseFloat(amtStr);
            if (isNaN(amt) || amt <= 0) {
                showToast("Invalid amount. Please enter a valid number.", "error"); return;
            }
            
            try {
                const req = await SS_API.post('/api/budgets/', { category: cat, amount: amt });
                if (req && req.budget) {
                    showToast("Budget created successfully!", "success");
                    await loadBudgets();
                    await loadSummary();
                } else {
                    showToast(req?.error || "Failed to create budget", "error");
                }
            } catch (e) {
                showToast("Network error creating budget", "error");
            }
        }

        async function loadGoals() {
            const data = await SS_API.get('/api/goals/');
            if (!data) return;
            GOALS = data.goals || [];
            const countEl = document.getElementById('goalCountTotal');
            if (countEl) countEl.textContent = GOALS.length;
            renderGoals();
        }

        function renderGoals() {
            const grid = document.getElementById('goalGrid');
            if (!grid) return;
            
            grid.style.display = 'grid';
            grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
            grid.style.gap = '1rem';
            grid.style.padding = '0';
            grid.style.background = 'transparent';
            grid.style.border = 'none';
            grid.style.textAlign = 'left';

            if (GOALS.length === 0) {
                grid.style.display = 'block';
                grid.style.padding = '4rem';
                grid.style.textAlign = 'center';
                grid.style.background = 'var(--card)';
                grid.style.border = '1px dashed var(--border)';
                grid.innerHTML = `
                    <div style="font-size:3rem;margin-bottom:1.5rem">🏆</div>
                    <h3 style="font-family:'Syne',sans-serif;font-size:1.25rem;margin-bottom:.5rem">No Goals Set</h3>
                    <p style="color:var(--muted);font-size:.875rem;max-width:300px;margin:0 auto 1.5rem">Set savings goals to stay motivated.</p>
                    <button class="btn btn-primary" style="margin:0 auto" id="createFirstGoalBtn" onclick="addGoal()">+ Create Your First Goal</button>
                `;
                return;
            }

            grid.innerHTML = GOALS.map(g => {
                const target = parseFloat(g.target_amount);
                const current = parseFloat(g.current_amount || 0);
                const pct = Math.min(100, (current / target) * 100);
                return `
                <div class="goal-card" style="background:var(--card);padding:1.5rem;border-radius:var(--r-md);border:1px solid var(--border)">
                    <div style="font-weight:600;font-size:1.1rem;margin-bottom:4px">${g.name}</div>
                    <div style="color:var(--muted);font-size:0.85rem;margin-bottom:1rem">Target: ₹${target.toLocaleString('en-IN')}</div>
                    
                    <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:6px">
                        <div style="font-family:'Syne',sans-serif;font-weight:700;color:var(--g)">₹${current.toLocaleString('en-IN')} Saved</div>
                        <div style="font-size:0.85rem;font-weight:700">${pct.toFixed(0)}%</div>
                    </div>
                    
                    <div class="progress-track" style="height:10px;background:var(--card2);border-radius:5px;overflow:hidden;margin-bottom:1rem">
                        <div class="progress-fill" style="width:${pct}%;background:var(--g);height:100%;border-radius:5px;transition:width 0.5s ease"></div>
                    </div>
                    
                    <button class="btn btn-secondary" style="width:100%;font-size:0.8rem;padding:0.4rem" onclick="addGoalProgress(${g.id}, '${g.name}')">Add Funds to Goal</button>
                </div>`;
            }).join('');
        }

        async function addGoal() {
            const name = prompt("Enter Goal Name (e.g., Vacation, Emergency Fund):");
            if (!name) return;
            const targetStr = prompt("Enter Target Amount (₹):");
            if (!targetStr) return;
            const target = parseFloat(targetStr);
            if (isNaN(target) || target <= 0) {
                showToast("Invalid target amount.", "error"); return;
            }
            
            try {
                const req = await SS_API.post('/api/goals/', { name: name, target_amount: target });
                if (req && req.goal) {
                    showToast("Goal created successfully!", "success");
                    await loadGoals();
                } else {
                    showToast(req?.error || "Failed to create goal", "error");
                }
            } catch (e) {
                showToast("Network error creating goal", "error");
            }
        }

        async function addGoalProgress(goalId, goalName) {
            const addStr = prompt(`Add funds to "${goalName}":\\nEnter amount to add (₹):`);
            if (!addStr) return;
            const amt = parseFloat(addStr);
            if (isNaN(amt) || amt <= 0) {
                showToast("Invalid amount.", "error"); return;
            }
            
            try {
                const req = await SS_API.post('/api/goals/' + goalId + '/add', { amount: amt });
                if (req && req.message) {
                    showToast("Progress updated successfully!", "success");
                    await loadGoals();
                } else {
                    showToast(req?.error || "Failed to update progress", "error");
                }
            } catch (e) {
                showToast("Network error updating goal", "error");
            }
        }
"""
    if "let BUDGETS =" not in content:
        content = content.replace("async function loadTransactions() {", budget_goals_js + "\n        async function loadTransactions() {")

    # 3. Add to init
    if "loadBudgets();" not in content:
        load_init_code = """
            loadSummary().then(success => {
                if (success || true) { // allow loading buds even if summary fails (resilient)
                    loadBudgets();
                    loadGoals();
                    loadTransactions();
                }
"""
        content = content.replace("""
            loadSummary().then(success => {
                if (success) {
                    loadTransactions();
""", load_init_code)

        # Fallback if the previous exact match isn't there
        content = content.replace("""
            loadSummary().then(success => {
                if (success || true) { // resilient load
                    loadTransactions();
""", load_init_code)

    # 4. Buttons
    if 'id="newBudgetBtn">' in content:
        content = content.replace('id="newBudgetBtn">', 'id="newBudgetBtn" onclick="addBudget()">')
    if 'id="newGoalBtn">' in content:
        content = content.replace('id="newGoalBtn">', 'id="newGoalBtn" onclick="addGoal()">')

    # Fix ALL old budget calc inside loadTransactions etc (the `if (t.type === 'debit')` instances)
    content = content.replace(
        "if (t.type === 'debit') {",
        "const tType = (t.type || '').toLowerCase();\\n                if (tType === 'debit' || tType === 'expense') {"
    )

    with codecs.open('templates/Dashboard.html', 'w', 'utf-8') as f:
        f.write(content)
        
    print("Dashboard.html injected successfully.")
except Exception as e:
    traceback.print_exc()

