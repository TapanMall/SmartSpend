// SmartSpend - Main JavaScript

// API Helper
const SS_API = {
    token: () => localStorage.getItem('ss_token') || '',
    
    activeRequests: 0,
    
    showLoader() {
        this.activeRequests++;
        let loader = document.getElementById('global-loader');
        if (!loader) {
            loader = document.createElement('div');
            loader.id = 'global-loader';
            loader.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.5); z-index: 9999;
                display: flex; justify-content: center; align-items: center;
                backdrop-filter: blur(2px);
            `;
            loader.innerHTML = '<div style="width:40px;height:40px;border:4px solid var(--g);border-top-color:transparent;border-radius:50%;animation:spin 1s linear infinite;"></div><style>@keyframes spin { 100% { transform: rotate(360deg); } }</style>';
            document.body.appendChild(loader);
        }
        loader.style.display = 'flex';
    },
    
    hideLoader() {
        this.activeRequests--;
        if (this.activeRequests <= 0) {
            this.activeRequests = 0;
            const loader = document.getElementById('global-loader');
            if (loader) loader.style.display = 'none';
        }
    },
    
    headers() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token()}`
        };
    },
    
    async get(path) {
        this.showLoader();
        try {
            const r = await fetch(path, { 
                headers: this.headers(),
                cache: 'no-store'
            });
            if (r.status === 401) {
                window.location.href = '/?auth=login';
                return null;
            }
            return r.json();
        } catch (e) {
            console.error('API Error:', e);
            return null;
        } finally {
            this.hideLoader();
        }
    },
    
    async post(path, body) {
        this.showLoader();
        try {
            const isFormData = body instanceof FormData;
            const headers = this.headers();
            if (isFormData) {
                delete headers['Content-Type'];
            }
            const r = await fetch(path, {
                method: 'POST',
                headers: headers,
                body: isFormData ? body : JSON.stringify(body)
            });
            if (r.status === 401) {
                window.location.href = '/?auth=login';
                return null;
            }
            return r.json();
        } catch (e) {
            console.error('API Error:', e);
            return null;
        } finally {
            this.hideLoader();
        }
    },
    
    async delete(path) {
        this.showLoader();
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
        } finally {
            this.hideLoader();
        }
    }
};

// Toast Notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const iconSpan = document.createElement('span');
    iconSpan.className = 'toast-icon';
    iconSpan.textContent = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
    
    const msgSpan = document.createElement('span');
    msgSpan.textContent = message;
    
    toast.appendChild(iconSpan);
    toast.appendChild(msgSpan);
    
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
