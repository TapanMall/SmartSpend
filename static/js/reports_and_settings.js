document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('ss_token');
    
    // Auth Headers Helper
    const getAuthHeaders = () => ({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    });

    const userStr = localStorage.getItem('ss_user');
    if (userStr) {
        try {
            const userObj = JSON.parse(userStr);
            const pName = document.getElementById('profileFullNameInput');
            const pEmail = document.getElementById('profileEmailInput');
            const pPhone = document.getElementById('profilePhoneInput');
            const pCurr = document.getElementById('profileCurrencyInput');
            if (pName && userObj.full_name) pName.value = userObj.full_name;
            if (pEmail && userObj.email) pEmail.value = userObj.email;
            if (pPhone && userObj.phone) pPhone.value = userObj.phone;
            if (pCurr && userObj.currency) pCurr.value = userObj.currency;
        } catch(e) {}
    }

    // Helper to download blob
    const downloadBlob = async (url, filename) => {
        try {
            const btn = event.target;
            const originalText = btn.innerHTML;
            btn.innerHTML = `<span class="spin" style="width:14px;height:14px;display:inline-block;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite"></span> Downloading...`;
            
            const response = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
            if (!response.ok) throw new Error("Failed to download");
            const blob = await response.blob();
            const a = document.createElement('a');
            a.href = window.URL.createObjectURL(blob);
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            btn.innerHTML = originalText;
        } catch (err) {
            console.error(err);
            alert("Error downloading file: " + err.message);
        }
    };

    // --- SECURITY ---
    const saveSecurityBtn = document.getElementById('saveSecurityBtn');
    if (saveSecurityBtn) {
        saveSecurityBtn.addEventListener('click', async () => {
            const currentObj = document.getElementById('profileCurrentPasswordInput');
            const newObj = document.getElementById('profileNewPasswordInput');
            const confObj = document.getElementById('profileConfirmPasswordInput');
            
            if (newObj.value !== confObj.value) {
                alert("New passwords do not match!");
                return;
            }
            
            if (newObj.value.length < 8) {
                alert("Password must be at least 8 characters long.");
                return;
            }
            
            try {
                const res = await fetch('/api/auth/security', {
                    method: 'PUT',
                    headers: getAuthHeaders(),
                    body: JSON.stringify({ 
                        current_password: currentObj.value, 
                        new_password: newObj.value 
                    })
                });
                const data = await res.json();
                if (res.ok) {
                    alert("Password updated successfully!");
                    currentObj.value = ""; newObj.value = ""; confObj.value = "";
                } else alert(data.error || "Failed to update password");
            } catch (err) { alert("Error occurred: " + err.message); }
        });
    }

    // --- DATA & PRIVACY ---
    const exportJsonBtn = document.getElementById('exportJsonBtn');
    if (exportJsonBtn) {
        exportJsonBtn.addEventListener('click', () => downloadBlob('/api/reports/export_json', 'SmartSpend_Data_Export.json'));
    }

    // --- DATA & PRIVACY (Custom Modal) ---
    const deleteAccountBtn = document.getElementById('deleteAccountBtn');
    const deleteModal = document.getElementById('deleteAccountModalOverlay');
    const confirmDeleteBtn = document.getElementById('confirmDeleteAccountBtn');

    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', () => {
            if (deleteModal) {
                deleteModal.classList.add('open');
                document.body.style.overflow = 'hidden';
            }
        });
    }

    window.closeDeleteAccountModal = () => {
        if (deleteModal) {
            deleteModal.classList.remove('open');
            document.body.style.overflow = '';
        }
    };

    window.handleDeleteAccountOverlay = (e) => {
        if (e.target === deleteModal) closeDeleteAccountModal();
    };

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', async () => {
            const originalText = confirmDeleteBtn.innerHTML;
            confirmDeleteBtn.innerHTML = `<span class="spin" style="width:14px;height:14px;display:inline-block;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite"></span> Deleting...`;
            confirmDeleteBtn.disabled = true;

            try {
                const res = await fetch('/api/auth/account', {
                    method: 'DELETE',
                    headers: getAuthHeaders()
                });
                if (res.ok) {
                    if (window.showToast) window.showToast("Your account has been deleted.", "error");
                    else alert("Your account has been deleted.");
                    
                    localStorage.clear();
                    setTimeout(() => {
                        window.location.replace('/?auth=login');
                    }, 1000);
                } else {
                    alert("Failed to delete account");
                    confirmDeleteBtn.innerHTML = originalText;
                    confirmDeleteBtn.disabled = false;
                }
            } catch (err) {
                alert("Error occurred: " + err.message);
                confirmDeleteBtn.innerHTML = originalText;
                confirmDeleteBtn.disabled = false;
            }
        });
    }

    // --- SUBSCRIPTION ---
    const cancelSubModal = document.getElementById('cancelSubscriptionModalOverlay');
    const confirmCancelBtn = document.getElementById('confirmCancelSubscriptionBtn');

    window.openCancelSubscriptionModal = () => {
        if (cancelSubModal) {
            cancelSubModal.classList.add('open');
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeCancelSubscriptionModal = () => {
        if (cancelSubModal) {
            cancelSubModal.classList.remove('open');
            document.body.style.overflow = '';
        }
    };

    window.handleCancelSubscriptionOverlay = (e) => {
        if (e.target === cancelSubModal) closeCancelSubscriptionModal();
    };

    if (confirmCancelBtn) {
        confirmCancelBtn.addEventListener('click', async () => {
            const originalText = confirmCancelBtn.innerHTML;
            confirmCancelBtn.innerHTML = `<span class="spin" style="width:14px;height:14px;display:inline-block;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite"></span> Canceling...`;
            confirmCancelBtn.disabled = true;
            
            try {
                const res = await fetch('/api/billing/cancel', {
                    method: 'POST',
                    headers: getAuthHeaders()
                });
                const data = await res.json();
                if (res.ok) {
                    if (window.showToast) window.showToast("Subscription canceled successfully.", "success");
                    else alert("Subscription canceled successfully.");
                    closeCancelSubscriptionModal();
                } else {
                    alert(data.error || "Failed to cancel subscription");
                }
            } catch (err) { 
                alert("Error occurred: " + err.message); 
            } finally {
                confirmCancelBtn.innerHTML = originalText;
                confirmCancelBtn.disabled = false;
            }
        });
    }

    // --- CSV EXPORTS ---
    const dlCsvBtn = document.getElementById('downloadCsvBtn');
    if (dlCsvBtn) dlCsvBtn.addEventListener('click', () => downloadBlob('/api/reports/export_raw_csv', 'Transactions.csv'));
    
    const expBudgetCsvBtn = document.getElementById('exportBudgetCsvBtn');
    if (expBudgetCsvBtn) expBudgetCsvBtn.addEventListener('click', () => downloadBlob('/api/reports/export_budget_csv', 'Budgets.csv'));
    
    const expGoalsCsvBtn = document.getElementById('exportGoalsCsvBtn');
    if (expGoalsCsvBtn) expGoalsCsvBtn.addEventListener('click', () => downloadBlob('/api/reports/export_goals_csv', 'Goals.csv'));

    // --- PDF EXPORTS (THEMED) ---
    const generatePdf = async (type, btnId) => {
        const btn = document.getElementById(btnId);
        const originalText = btn.innerHTML;
        btn.innerHTML = `<span class="spin" style="width:14px;height:14px;display:inline-block;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite"></span> Generating...`;
        
        try {
            // Fetch the user's data to display in the PDF
            const res = await fetch('/api/reports/export_json', { headers: { 'Authorization': `Bearer ${token}` }});
            const data = await res.json();
            
            // Create a visually rich HTML template identical to the proper dashboard theme
            const containerDiv = document.createElement('div');
            containerDiv.style.position = 'absolute';
            containerDiv.style.left = '-9999px';
            containerDiv.style.top = '0';
            containerDiv.style.width = '800px'; // fixed width for predictable PDF
            containerDiv.style.background = 'white';
            document.body.appendChild(containerDiv);
            
            const user = data.user || {};
            const txs = data.transactions || [];
            
            let totalInc = txs.filter(t=>t.type==='credit').reduce((a,b)=>a+(b.amount||0), 0);
            let totalExp = txs.filter(t=>t.type==='debit').reduce((a,b)=>a+(b.amount||0), 0);
            
            let contentBody = '';
            
            if (type === 'monthly' || type === 'annual') {
                contentBody = `
                    <div style="font-family: 'Syne', sans-serif; padding: 40px; color: #060d12; background: linear-gradient(135deg, #e4f9ee 0%, #f4fdf8 100%); min-height: 1122px; width: 800px; box-sizing: border-box;">
                        
                        <!-- Header -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 40px;">
                            <div>
                                <h1 style="margin: 0; font-size: 42px; font-weight: 800; color: #060d12; line-height: 1.1;">
                                    Your<br>Money.<br>
                                    <span style="color: #39ff7e; text-shadow: 0 4px 20px rgba(57,255,126,0.4);">Smarter</span><br>
                                    than<br>Ever<br>Before.
                                </h1>
                            </div>
                            <div style="text-align: right; background: rgba(255,255,255,0.8); padding: 15px 20px; border-radius: 16px; border: 1px solid rgba(57,255,126,0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.03);">
                                <h3 style="margin: 0 0 5px 0; font-size: 16px; font-weight: 700; color: #060d12;">${type === 'monthly' ? 'Monthly Report' : 'Annual Summary'}</h3>
                                <p style="margin: 0; font-size: 12px; color: #64748b; font-family: 'Inter', sans-serif;">Generated: ${new Date().toLocaleDateString()}</p>
                                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.05); text-align: left; font-family: 'Inter', sans-serif;">
                                    <div style="font-size: 11px; color: #64748b; font-weight:600; text-transform:uppercase;">Account</div>
                                    <div style="font-size: 13px; font-weight: 600; color: #060d12;">${user.full_name || 'User'}</div>
                                    <div style="font-size: 11px; color: #64748b;">${user.email || ''}</div>
                                </div>
                            </div>
                        </div>

                        <!-- Main Dashboard Card -->
                        <div style="background: rgba(255,255,255,0.9); border: 1px solid rgba(255,255,255,0.5); border-radius: 24px; padding: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.04); position: relative;">
                            
                            <!-- Overview Tag -->
                            <div style="position: absolute; top: 30px; right: 30px; background: #e4f9ee; color: #10b981; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 20px;">
                                ${new Date().toLocaleString('default', { month: 'short', year: 'numeric' })}
                            </div>

                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">💼 Overview</div>
                            <div style="font-size: 48px; font-weight: 800; color: #39ff7e; text-shadow: 0 4px 15px rgba(57,255,126,0.3); line-height: 1;">₹${(totalInc - totalExp).toLocaleString('en-IN', {minimumFractionDigits:0})}</div>
                            <div style="font-size: 13px; color: #64748b; font-weight: 500; margin-top: 5px;">Total Balance / Net Savings</div>

                            <div style="display: flex; gap: 15px; margin-top: 25px;">
                                <div style="flex: 1; background: white; border-radius: 16px; padding: 15px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid #f1f5f9;">
                                    <div style="font-size: 11px; color: #64748b; font-weight: 600; display: flex; align-items: center; gap: 5px;">
                                        <span style="color:#10b981">↑</span> Income
                                    </div>
                                    <div style="font-size: 20px; font-weight: 800; color: #10b981; margin-top: 5px;">₹${totalInc.toLocaleString('en-IN', {minimumFractionDigits:0})}</div>
                                </div>
                                <div style="flex: 1; background: white; border-radius: 16px; padding: 15px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid #f1f5f9;">
                                    <div style="font-size: 11px; color: #64748b; font-weight: 600; display: flex; align-items: center; gap: 5px;">
                                        <span style="color:#ef4444">↓</span> Expenses
                                    </div>
                                    <div style="font-size: 20px; font-weight: 800; color: #ef4444; margin-top: 5px;">₹${totalExp.toLocaleString('en-IN', {minimumFractionDigits:0})}</div>
                                </div>
                            </div>
                            
                            <!-- Graph Mockup -->
                            <div style="margin-top: 30px; height: 80px; position: relative;">
                                <svg viewBox="0 0 400 80" style="width: 100%; height: 100%; overflow: visible;">
                                    <path d="M0,50 C50,40 100,70 150,55 C200,40 250,20 300,30 C350,40 400,10 400,10" fill="none" stroke="#39ff7e" stroke-width="3" />
                                    <path d="M0,70 C50,65 100,75 150,68 C200,60 250,62 300,55 C350,48 400,40 400,40" fill="none" stroke="#ef4444" stroke-width="2" opacity="0.5"/>
                                </svg>
                            </div>

                            <!-- Transaction List -->
                            <div style="margin-top: 25px; display: flex; flex-direction: column; gap: 10px; font-family: 'Inter', sans-serif;">
                                ${txs.slice(0, 5).map(t => `
                                    <div style="background: white; border-radius: 16px; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid #f1f5f9;">
                                        <div style="display: flex; align-items: center; gap: 15px;">
                                            <div style="width: 36px; height: 36px; background: #e4f9ee; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px;">
                                                ${t.type==='credit' ? '💰' : '🏷️'}
                                            </div>
                                            <div>
                                                <div style="font-weight: 700; color: #060d12; font-size: 14px;">${t.name}</div>
                                                <div style="font-size: 11px; color: #64748b; margin-top: 2px;">${t.category} • ${new Date(t.date).toLocaleDateString()}</div>
                                            </div>
                                        </div>
                                        <div style="font-weight: 800; font-size: 14px; color: ${t.type==='credit'?'#10b981':'#ef4444'}">
                                            ${t.type==='credit'?'+':'-'}₹${(t.amount||0).toLocaleString('en-IN')}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>

                    </div>
                `;
            } else if (type === 'tax') {
                 contentBody = `
                    <div style="font-family: 'Syne', sans-serif; padding: 40px; color: #060d12; background: linear-gradient(135deg, #e4f9ee 0%, #f4fdf8 100%); min-height: 1122px; width: 800px; box-sizing: border-box;">
                        
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 40px; border-bottom: 2px solid rgba(57,255,126,0.3); padding-bottom: 20px;">
                            <div>
                                <h1 style="margin: 0; font-size: 36px; font-weight: 800; color: #060d12;"><span style="color: #39ff7e;">Tax</span> Filing<br>Overview</h1>
                                <p style="margin: 5px 0 0; font-size: 14px; color: #64748b; font-weight: 600;">Financial Year 2025-2026</p>
                            </div>
                            <div style="font-size: 42px;">🏛️</div>
                        </div>
                        
                        <div style="background: rgba(255,255,255,0.9); border-radius: 20px; padding: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.04); margin-bottom: 30px;">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">Taxpayer Information</div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-family: 'Inter', sans-serif;">
                                <div>
                                    <div style="font-size: 11px; color: #94a3b8; font-weight: 600;">Name</div>
                                    <div style="font-size: 15px; font-weight: 700; color: #060d12; margin-top: 4px;">${user.full_name || 'User'}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #94a3b8; font-weight: 600;">Email</div>
                                    <div style="font-size: 15px; font-weight: 700; color: #060d12; margin-top: 4px;">${user.email || ''}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #94a3b8; font-weight: 600;">Phone</div>
                                    <div style="font-size: 15px; font-weight: 700; color: #060d12; margin-top: 4px;">${user.phone || 'N/A'}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #94a3b8; font-weight: 600;">Currency Base</div>
                                    <div style="font-size: 15px; font-weight: 700; color: #060d12; margin-top: 4px;">${user.currency || 'INR'}</div>
                                </div>
                            </div>
                        </div>
                        
                        <div style="background: #060d12; border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(57,255,126,0.15); text-align: center; margin-bottom: 30px; position:relative; overflow:hidden;">
                            <div style="position: absolute; top:-50%; left:-20%; width: 200px; height: 200px; background: #39ff7e; filter: blur(100px); opacity:0.1;"></div>
                            <div style="position: absolute; bottom:-50%; right:-20%; width: 200px; height: 200px; background: #10b981; filter: blur(100px); opacity:0.1;"></div>
                            
                            <div style="font-size: 14px; font-weight: 700; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 2px;">Gross Taxable Income</div>
                            <div style="font-size: 56px; font-weight: 800; color: #39ff7e; margin-top: 10px; line-height: 1;">₹${totalInc.toLocaleString('en-IN', {minimumFractionDigits:0})}</div>
                            <div style="font-size: 13px; color: rgba(255,255,255,0.5); font-weight: 500; margin-top: 15px;">Computed from sum of all aggregated credits</div>
                        </div>

                        <div style="background: #e4f9ee; padding: 25px; border-radius: 16px; border: 1px solid rgba(57,255,126,0.3);">
                            <div style="display:flex; align-items:center; gap: 10px; margin-bottom: 10px;">
                                <span style="font-size: 20px;">✓</span>
                                <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #060d12;">Verified Data Declaration</h4>
                            </div>
                            <p style="margin: 0; font-size: 13px; color: #475569; line-height: 1.6; font-family: 'Inter', sans-serif;">This report is automatically synthesized strictly from your input tracking and ledger logic verified under SmartSpend protocols. Please consult your localized chartered accountant prior to filing actual IT returns utilizing this output proxy.</p>
                        </div>
                    </div>
                `;
            }

            containerDiv.innerHTML = contentBody;
            
            // html2pdf options
            const opt = {
                margin:       [0, 0, 0, 0],
                filename:     `SmartSpend_${type}_Report.pdf`,
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true },
                jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' }
            };

            await html2pdf().set(opt).from(containerDiv).save();
            document.body.removeChild(containerDiv);
            
            btn.innerHTML = originalText;
        } catch (err) {
            console.error(err);
            alert("Error generating PDF: " + err.message);
            btn.innerHTML = originalText;
        }
    };

    const monthlyPdfBtn = document.getElementById('monthlyPdfBtn');
    if(monthlyPdfBtn) monthlyPdfBtn.addEventListener('click', () => generatePdf('monthly', 'monthlyPdfBtn'));
    
    const annualPdfBtn = document.getElementById('annualPdfBtn');
    if(annualPdfBtn) annualPdfBtn.addEventListener('click', () => generatePdf('annual', 'annualPdfBtn'));
    
    const taxPdfBtn = document.getElementById('taxPdfBtn');
    if(taxPdfBtn) taxPdfBtn.addEventListener('click', () => generatePdf('tax', 'taxPdfBtn'));
});
