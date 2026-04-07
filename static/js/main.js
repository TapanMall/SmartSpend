// SmartSpend - Main JavaScript

// API Helper
const SS_API = {
    token: () => localStorage.getItem('ss_token') || '',
    
    headers() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token()}`
        };
    },
    
    async get(path) {
        try {
            const r = await fetch(path, { headers: this.headers() });
            if (r.status === 401) {
                window.location.href = '/?auth=login';
                return null;
            }
            return r.json();
        } catch (e) {
            console.error('API Error:', e);
            return null;
        }
    },
    
    async post(path, body) {
        try {
            const r = await fetch(path, {
                method: 'POST',
                headers: this.headers(),
                body: JSON.stringify(body)
            });
            if (r.status === 401) {
                window.location.href = '/?auth=login';
                return null;
            }
            return r.json();
        } catch (e) {
            console.error('API Error:', e);
            return null;
        }
    },
    
    async delete(path) {
        try {
            const r = await fetch(path, {
                method: 'DELETE',
                headers: this.headers()
            });
            if (r.status === 401) {
                window.location.href = '/?auth=login';
                return null;
            }
            return r.json();
        } catch (e) {
            console.error('API Error:', e);
            return null;
        }
    }
};

// Toast Notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
        <span>${message}</span>
    `;
    
    toast.style.cssText = `
        background: var(--card);
        border: 1px solid var(--border);
        border-left: 3px solid ${type === 'success' ? 'var(--primary)' : type === 'error' ? 'var(--error)' : 'var(--info)'};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        animation: slideInRight 0.3s ease;
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Format Currency
function formatCurrency(amount) {
    return '₹' + Math.abs(amount).toLocaleString('en-IN');
}

// Format Date
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    });
}

// Debounce Function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Local Storage Helpers
const Storage = {
    get(key) {
        try {
            return JSON.parse(localStorage.getItem(key));
        } catch {
            return null;
        }
    },
    set(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    },
    remove(key) {
        localStorage.removeItem(key);
    }
};

// Check Authentication
function checkAuth() {
    const token = localStorage.getItem('ss_token');
    if (!token && !window.location.pathname.includes('login')) {
        window.location.href = '/?auth=login';
        return false;
    }
    return true;
}

// Logout Function
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('ss_token');
        localStorage.removeItem('ss_user');
        window.location.href = '/?auth=login';
    }
}

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    // Check auth on protected pages
    if (document.querySelector('.dashboard, .app')) {
        checkAuth();
    }
});

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SS_API, showToast, formatCurrency, formatDate, debounce, Storage, logout };
}
