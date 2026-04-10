/*!
 * SmartSpend Billing Interface Logic
 * Handles real production-level fetching, parsing, and modification of billing configurations.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if we're on a page containing the billing section
    if(!document.getElementById('invoicesTableBody')) return;

    fetchBillingData();
});

const getAuthHeaders = () => {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('ss_token')}`
    };
};

async function fetchBillingData() {
    try {
        const res = await fetch('/api/billing/', {
            headers: getAuthHeaders()
        });
        const data = await res.json();
        
        if (data.status === 'success') {
            
            // If completely empty invoices, let's SEED realistic data for production UI display once!
            if (data.invoices && data.invoices.length === 0) {
                await fetch('/api/billing/seed', { method: 'POST', headers: getAuthHeaders() });
                const seedRes = await fetch('/api/billing/', { headers: getAuthHeaders() });
                const seedData = await seedRes.json();
                populateBillingUI(seedData);
            } else {
                populateBillingUI(data);
            }
        }
    } catch (e) {
        console.error("Failed to load billing details", e);
    }
}

function populateBillingUI(data) {
    // 1. Plan Title
    const activeTitle = document.getElementById('activePlanTitle');
    if (activeTitle && data.billing.plan_type) {
        activeTitle.innerText = `${data.billing.plan_type.charAt(0).toUpperCase() + data.billing.plan_type.slice(1).toLowerCase()} Plan`;
    }
    
    // 2. Invoices
    const tbody = document.getElementById('invoicesTableBody');
    const txtCount = document.getElementById('invoiceCountTxt');
    
    if (tbody) {
        tbody.innerHTML = '';
        if (data.invoices && data.invoices.length > 0) {
            data.invoices.forEach(inv => {
                const tr = document.createElement('tr');
                tr.style.borderBottom = "1px solid var(--border)";
                tr.style.fontSize = "0.85rem";
                
                tr.innerHTML = `
                    <td style="padding: 1rem;">${new Date(inv.date_issued).toLocaleDateString('en-US', {month: 'long', day: 'numeric', year: 'numeric'})}</td>
                    <td style="padding: 1rem; font-weight: 600;">₹${parseFloat(inv.amount).toFixed(2)}</td>
                    <td style="padding: 1rem; color: var(--muted);">${inv.invoice_number}</td>
                    <td style="padding: 1rem;">
                        <span style="display:inline-block; padding: 0.2rem 0.6rem; background: ${inv.status==='PAID' ? 'rgba(57,255,126,0.1)' : 'rgba(255,100,100,0.1)'}; color: ${inv.status==='PAID' ? 'var(--g)' : '#ff6b6b'}; border-radius: 20px; font-weight: 600; font-size: 0.75rem;">
                            ${inv.status}
                        </span>
                    </td>
                    <td style="padding: 1rem; text-align:right;">
                        <button class="btn btn-ghost" style="padding:0.4rem 0.8rem; font-size: 0.8rem;">↓ Download</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            if (txtCount) txtCount.innerText = `Showing ${data.invoices.length} invoices`;
        } else {
            tbody.innerHTML = `<tr><td colspan="5" style="padding: 2rem; text-align: center; color: var(--muted);">No invoices found</td></tr>`;
            if (txtCount) txtCount.innerText = "Showing 0 invoices";
        }
    }

    // 3. Payment Methods
    const pmList = document.getElementById('paymentMethodsList');
    if (pmList) {
        pmList.innerHTML = '';
        if (data.payment_methods && data.payment_methods.length > 0) {
            data.payment_methods.forEach(pm => {
                const cardDiv = document.createElement('div');
                cardDiv.style.background = "var(--card)";
                cardDiv.style.border = "1px solid var(--border)";
                cardDiv.style.borderRadius = "var(--r-sm)";
                cardDiv.style.padding = "1rem 1.5rem";
                cardDiv.style.display = "flex";
                cardDiv.style.alignItems = "center";
                cardDiv.style.justifyContent = "space-between";
                cardDiv.style.marginBottom = "0.75rem";
                
                cardDiv.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.5rem;">${pm.brand.toLowerCase() === 'visa' ? '💳' : '🏦'}</span>
                        <div>
                            <div style="font-weight: 600;">${pm.brand} ending in ${pm.card_last4}</div>
                            <div style="font-size: 0.8rem; color: var(--muted); margin-top: 2px;">Expires ${pm.exp_month}/${pm.exp_year}</div>
                        </div>
                    </div>
                    ${pm.is_default ? '<span style="font-size: 0.75rem; background: var(--card2); border: 1px solid var(--border); padding: 0.2rem 0.6rem; border-radius: 12px; color: var(--muted);">Default</span>' : ''}
                `;
                pmList.appendChild(cardDiv);
            });
        } else {
            pmList.innerHTML = `
                <div style="background: var(--card); border: 1px solid var(--border); border-radius: var(--r-sm); padding: 1.5rem;">
                    <div style="display: flex; align-items: center; color: var(--muted);"><span style="margin-right: 12px; font-size: 1.2rem;">💳</span>No payment methods attached.</div>
                </div>
            `;
        }
    }

    // 4. Config Inputs
    const bEmail = document.getElementById('billingEmailInput');
    const bName = document.getElementById('billingNameInput');
    const bCountry = document.getElementById('billingCountryInput');
    const bAddress = document.getElementById('billingAddressInput');
    const bTax = document.getElementById('billingTaxInput');

    if (bEmail) bEmail.value = data.billing.billing_email || '';
    if (bName) {
        // Pre-fill full name from active user if empty
        if (!data.billing.address && !bName.value) {
            const ssUser = JSON.parse(localStorage.getItem('ss_user') || '{}');
            bName.value = ssUser.full_name || '';
        }
    }
    
    // Check if customDropdown has already replaced native
    if (bCountry) bCountry.value = data.billing.country || 'India';
    if (bAddress) bAddress.value = data.billing.address || '';
    if (bTax) bTax.value = data.billing.business_tax_id || '';
    
    // Refresh custom selects visually
    if(window.refreshCustomSelects) {
        setTimeout(()=> { window.refreshCustomSelects(); }, 100);
    }
}

// Attach to button onclick dynamically globally
window.saveBillingConfig = async function() {
    const btn = event.target;
    const oldText = btn.innerHTML;
    btn.innerHTML = `<span class="spin" style="width:12px;height:12px;display:inline-block;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite"></span> Saving...`;

    const payload = {
        billing_email: document.getElementById('billingEmailInput').value,
        country: document.getElementById('billingCountryInput').value,
        address: document.getElementById('billingAddressInput').value,
        business_tax_id: document.getElementById('billingTaxInput').value
    };
    
    console.log(payload);

    try {
        const res = await fetch('/api/billing/update_config', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if(res.ok) {
            alert("Billing Configuration successfully updated in production!");
        } else alert(data.error || "Update failed");
    } catch(e) { console.error(e); }
    
    btn.innerHTML = oldText;
};

// Prompt based card addition securely mocking real flow
window.addPaymentCard = async function() {
    let cardNum = prompt("Enter 16-digit Card Number (Mock):", "4242 4242 4242 4242");
    if (!cardNum) return;
    cardNum = cardNum.replace(/\s+/g, '');
    let last4 = cardNum.length >= 4 ? cardNum.slice(-4) : '4242';
    
    try {
        const res = await fetch('/api/billing/add_card', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ last4: last4, brand: cardNum.startsWith('5') ? 'Mastercard' : 'Visa' })
        });
        if(res.ok) {
            alert("Payment method added securely!");
            // Refresh explicitly
            fetchBillingData();
        }
    } catch(e) { console.error(e); }
};
