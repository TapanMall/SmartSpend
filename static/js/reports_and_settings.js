document.addEventListener('DOMContentLoaded', () => {
    console.log("Reports & Settings Script Initialized");
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
    const downloadBlob = async (e, url, filename) => {
        try {
            let btn = null;
            let originalText = '';
            if (e && e.currentTarget) {
                btn = e.currentTarget;
                originalText = btn.innerHTML;
                btn.innerHTML = `<span class="spin" style="width:14px;height:14px;display:inline-block;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite"></span> Downloading...`;
            }
            
            const response = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
            if (!response.ok) throw new Error("Failed to download");
            const blob = await response.blob();
            const a = document.createElement('a');
            a.href = window.URL.createObjectURL(blob);
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            if (btn) btn.innerHTML = originalText;
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
        exportJsonBtn.addEventListener('click', (e) => downloadBlob(e, '/api/reports/export_json', 'SmartSpend_Data_Export.json'));
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
    if (dlCsvBtn) dlCsvBtn.addEventListener('click', (e) => downloadBlob(e, '/api/reports/export_raw_csv', 'Transactions.csv'));
    
    const expBudgetCsvBtn = document.getElementById('exportBudgetCsvBtn');
    if (expBudgetCsvBtn) expBudgetCsvBtn.addEventListener('click', (e) => downloadBlob(e, '/api/reports/export_budget_csv', 'Budgets.csv'));
    
    const expGoalsCsvBtn = document.getElementById('exportGoalsCsvBtn');
    if (expGoalsCsvBtn) expGoalsCsvBtn.addEventListener('click', (e) => downloadBlob(e, '/api/reports/export_goals_csv', 'Goals.csv'));

    // --- PDF EXPORTS (jsPDF Direct - No html2canvas needed) ---
    const generatePdf = async (type, btnId) => {
        const btn = document.getElementById(btnId);
        const originalText = btn.innerHTML;
        btn.innerHTML = `<span class="spin" style="width:14px;height:14px;display:inline-block;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite"></span> Generating...`;
        
        try {
            const res = await fetch('/api/reports/export_json', { headers: { 'Authorization': `Bearer ${token}` }});
            const data = await res.json();
            
            const user = data.user || {};
            const txs = data.transactions || [];
            
            const isIncome = (t) => {
                const tp = (t.type||'').toLowerCase();
                return tp === 'credit' || tp === 'income';
            };
            
            let totalInc = txs.filter(isIncome).reduce((a,b) => a + (parseFloat(b.amount)||0), 0);
            let totalExp = txs.filter(t => !isIncome(t)).reduce((a,b) => a + (parseFloat(b.amount)||0), 0);
            const balance = totalInc - totalExp;
            const fmt = (v) => 'Rs. ' + Math.abs(v).toLocaleString('en-IN');

            const { jsPDF } = window.jspdf;
            const doc = new jsPDF({ unit: 'mm', format: 'a4' });
            const W = 210, H = 297;
            let y = 0;

            // Helper functions
            const setColor = (hex) => {
                const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
                doc.setTextColor(r, g, b);
            };
            const setFill = (hex) => {
                const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
                doc.setFillColor(r, g, b);
            };
            const setDraw = (hex) => {
                const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
                doc.setDrawColor(r, g, b);
            };

            // -- Background --
            setFill('#e4f9ee');
            doc.rect(0, 0, W, H, 'F');
            setFill('#f4fdf8');
            doc.rect(0, H/2, W, H/2, 'F');

            if (type === 'monthly' || type === 'annual') {
                // -- Title --
                y = 25;
                doc.setFont('helvetica', 'bold');
                doc.setFontSize(28);
                setColor('#060d12');
                doc.text('Your Money.', 20, y);
                y += 10;
                setColor('#10b981');
                doc.text('Smarter', 20, y);
                y += 10;
                setColor('#060d12');
                doc.text('than Ever Before.', 20, y);

                // -- Report Info Box --
                setFill('#ffffff');
                doc.roundedRect(120, 15, 75, 40, 3, 3, 'F');
                setDraw('#d1fae5');
                doc.roundedRect(120, 15, 75, 40, 3, 3, 'S');
                
                doc.setFontSize(11);
                doc.setFont('helvetica', 'bold');
                setColor('#060d12');
                doc.text(type === 'monthly' ? 'Monthly Report' : 'Annual Summary', 125, 25);
                doc.setFontSize(8);
                doc.setFont('helvetica', 'normal');
                setColor('#64748b');
                doc.text('Generated: ' + new Date().toLocaleDateString(), 125, 30);
                doc.setFontSize(7);
                setColor('#64748b');
                doc.text('ACCOUNT', 125, 38);
                doc.setFontSize(9);
                doc.setFont('helvetica', 'bold');
                setColor('#060d12');
                doc.text(user.full_name || 'User', 125, 43);
                doc.setFont('helvetica', 'normal');
                doc.setFontSize(7);
                setColor('#64748b');
                doc.text(user.email || '', 125, 48);

                // -- Main Card --
                y = 70;
                setFill('#ffffff');
                doc.roundedRect(15, y, W - 30, 65, 4, 4, 'F');
                setDraw('#e2e8f0');
                doc.roundedRect(15, y, W - 30, 65, 4, 4, 'S');

                // Date tag
                setFill('#e4f9ee');
                doc.roundedRect(155, y + 5, 30, 8, 2, 2, 'F');
                doc.setFontSize(7);
                doc.setFont('helvetica', 'bold');
                setColor('#10b981');
                doc.text(new Date().toLocaleString('default', { month: 'short', year: 'numeric' }), 158, y + 10);

                // Overview
                doc.setFontSize(7);
                setColor('#64748b');
                doc.text('OVERVIEW', 22, y + 12);
                doc.setFontSize(26);
                doc.setFont('helvetica', 'bold');
                setColor('#10b981');
                doc.text(fmt(balance), 22, y + 25);
                doc.setFontSize(8);
                doc.setFont('helvetica', 'normal');
                setColor('#64748b');
                doc.text('Total Balance / Net Savings', 22, y + 32);

                // Income Box
                setFill('#ffffff');
                doc.roundedRect(22, y + 38, 75, 20, 3, 3, 'F');
                setDraw('#f1f5f9');
                doc.roundedRect(22, y + 38, 75, 20, 3, 3, 'S');
                doc.setFontSize(7);
                setColor('#64748b');
                doc.text('Income', 27, y + 46);
                doc.setFontSize(14);
                doc.setFont('helvetica', 'bold');
                setColor('#10b981');
                doc.text(fmt(totalInc), 27, y + 54);

                // Expense Box
                setFill('#ffffff');
                doc.roundedRect(105, y + 38, 75, 20, 3, 3, 'F');
                setDraw('#f1f5f9');
                doc.roundedRect(105, y + 38, 75, 20, 3, 3, 'S');
                doc.setFontSize(7);
                doc.setFont('helvetica', 'normal');
                setColor('#64748b');
                doc.text('Expenses', 110, y + 46);
                doc.setFontSize(14);
                doc.setFont('helvetica', 'bold');
                setColor('#ef4444');
                doc.text(fmt(totalExp), 110, y + 54);

                // -- Transaction Table --
                y = 145;
                doc.setFontSize(11);
                doc.setFont('helvetica', 'bold');
                setColor('#060d12');
                doc.text('Recent Transactions', 20, y);
                y += 6;

                // Table Header
                setFill('#f8fafc');
                doc.rect(15, y, W - 30, 8, 'F');
                doc.setFontSize(7);
                doc.setFont('helvetica', 'bold');
                setColor('#64748b');
                doc.text('Transaction', 20, y + 5);
                doc.text('Category', 75, y + 5);
                doc.text('Date', 120, y + 5);
                doc.text('Amount', 185, y + 5, { align: 'right' });
                y += 10;

                // Rows
                doc.setFont('helvetica', 'normal');
                doc.setFontSize(8);
                const showTxs = txs.slice(0, 20);
                showTxs.forEach((t, i) => {
                    if (y > 270) return;
                    
                    if (i % 2 === 0) {
                        setFill('#f8fafc');
                        doc.rect(15, y - 3, W - 30, 8, 'F');
                    }
                    
                    setColor('#060d12');
                    doc.setFont('helvetica', 'bold');
                    doc.text((t.name || 'N/A').substring(0, 25), 20, y + 2);
                    doc.setFont('helvetica', 'normal');
                    setColor('#64748b');
                    doc.text((t.category || 'N/A').substring(0, 18), 75, y + 2);
                    doc.text(t.date ? new Date(t.date).toLocaleDateString('en-IN') : 'N/A', 120, y + 2);
                    
                    const inc = isIncome(t);
                    setColor(inc ? '#10b981' : '#ef4444');
                    doc.setFont('helvetica', 'bold');
                    doc.text((inc ? '+' : '-') + fmt(parseFloat(t.amount)||0), 185, y + 2, { align: 'right' });
                    
                    y += 8;
                });

            } else if (type === 'tax') {
                // -- Tax Report --
                y = 25;
                doc.setFont('helvetica', 'bold');
                doc.setFontSize(24);
                setColor('#10b981');
                doc.text('Tax', 20, y);
                setColor('#060d12');
                doc.text('Filing Overview', 42, y);
                y += 8;
                doc.setFontSize(10);
                doc.setFont('helvetica', 'normal');
                setColor('#64748b');
                doc.text('Financial Year 2025-2026', 20, y);
                y += 4;
                setDraw('#d1fae5');
                doc.line(15, y, W - 15, y);

                // Taxpayer Info
                y += 10;
                setFill('#ffffff');
                doc.roundedRect(15, y, W - 30, 35, 3, 3, 'F');
                doc.setFontSize(7);
                doc.setFont('helvetica', 'bold');
                setColor('#64748b');
                doc.text('TAXPAYER INFORMATION', 22, y + 8);
                
                doc.setFontSize(8);
                setColor('#94a3b8');
                doc.text('Name', 22, y + 16);
                doc.text('Email', 110, y + 16);
                doc.text('Phone', 22, y + 26);
                doc.text('Currency', 110, y + 26);
                
                doc.setFont('helvetica', 'bold');
                setColor('#060d12');
                doc.text(user.full_name || 'User', 22, y + 21);
                doc.text(user.email || '', 110, y + 21);
                doc.text(user.phone || 'N/A', 22, y + 31);
                doc.text(user.currency || 'INR', 110, y + 31);

                // Gross Income (dark card)
                y += 45;
                setFill('#060d12');
                doc.roundedRect(15, y, W - 30, 45, 4, 4, 'F');
                doc.setFontSize(9);
                doc.setFont('helvetica', 'bold');
                setColor('#94a3b8');
                doc.text('GROSS TAXABLE INCOME', W/2, y + 12, { align: 'center' });
                doc.setFontSize(28);
                setColor('#10b981');
                doc.text(fmt(totalInc), W/2, y + 28, { align: 'center' });
                doc.setFontSize(8);
                doc.setFont('helvetica', 'normal');
                setColor('#64748b');
                doc.text('Computed from sum of all aggregated credits', W/2, y + 36, { align: 'center' });

                // Disclaimer
                y += 55;
                setFill('#e4f9ee');
                doc.roundedRect(15, y, W - 30, 30, 3, 3, 'F');
                setDraw('#d1fae5');
                doc.roundedRect(15, y, W - 30, 30, 3, 3, 'S');
                doc.setFontSize(10);
                doc.setFont('helvetica', 'bold');
                setColor('#060d12');
                doc.text('Verified Data Declaration', 22, y + 10);
                doc.setFontSize(7);
                doc.setFont('helvetica', 'normal');
                setColor('#475569');
                const disclaimer = 'This report is automatically synthesized from your input tracking and ledger logic verified under SmartSpend protocols. Please consult your chartered accountant prior to filing actual IT returns.';
                const lines = doc.splitTextToSize(disclaimer, W - 40);
                doc.text(lines, 22, y + 16);
            }

            // -- Footer --
            doc.setFontSize(7);
            doc.setFont('helvetica', 'normal');
            setColor('#94a3b8');
            doc.text('SmartSpend  |  Generated on ' + new Date().toLocaleDateString() + '  |  Page 1', W/2, H - 10, { align: 'center' });

            doc.save(`SmartSpend_${type}_Report.pdf`);
            
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
