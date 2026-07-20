/**
 * app.js — Shared utilities for Annalakshmi DMS
 * Loaded on every page via base.html
 */

/* ── API Fetch Wrapper ───────────────────────────────────── */
async function apiFetch(url, options = {}) {
    const defaultHeaders = { 'Content-Type': 'application/json' };
    options.headers = { ...defaultHeaders, ...options.headers };

    try {
        const response = await fetch(url, options);
        let data;

        if (response.status !== 204) {
            data = await response.json();
        } else {
            data = {};
        }

        if (!response.ok) {
            let errorMsg = data.message || 'Something went wrong';
            let errorDetails = data.details || null;

            if (data.detail) {
                if (typeof data.detail === 'string') {
                    errorMsg = data.detail;
                } else if (Array.isArray(data.detail)) {
                    errorMsg = 'Validation Error';
                    errorDetails = data.detail.map(d => ({
                        field: d.loc && d.loc.length > 0 ? d.loc[d.loc.length - 1] : null,
                        message: d.msg
                    }));
                }
            }

            const error = new Error(errorMsg);
            error.status = response.status;
            error.details = errorDetails;
            throw error;
        }

        return data;
    } catch (error) {
        if (!error.status) {
            // Network-level failure
            error.status = 0;
            error.message = 'Network error — please check your connection and try again.';
        }
        throw error;
    }
}

/* ── Toast Notifications ─────────────────────────────────── */
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const icons = {
        success: 'bi-check-circle-fill',
        danger:  'bi-exclamation-triangle-fill',
        warning: 'bi-info-circle-fill',
    };

    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-toast alert-dismissible fade show d-flex align-items-center mb-2`;
    toast.role = 'alert';
    toast.innerHTML = `
        <i class="bi ${icons[type] || icons.success} me-2 fs-5"></i>
        <div class="flex-grow-1">${escapeHtml(message)}</div>
        <button type="button" class="btn-close ms-2" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    container.appendChild(toast);

    // Auto-dismiss after 4s
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 200);
    }, 4000);
}

/* ── HTML Escaping ────────────────────────────────────────── */
function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

/* ── Debounce ─────────────────────────────────────────────── */
function debounce(fn, delay = 300) {
    let timerId;
    return function (...args) {
        clearTimeout(timerId);
        timerId = setTimeout(() => fn.apply(this, args), delay);
    };
}

/* ── Date Formatting ──────────────────────────────────────── */
function formatDate(dateStr) {
    if (!dateStr) return '—';
    const d = new Date(dateStr);
    if (isNaN(d)) return '—';
    return d.toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatDateTime(dateStr) {
    if (!dateStr) return '—';
    const d = new Date(dateStr);
    if (isNaN(d)) return '—';
    return d.toLocaleString('en-IN', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit',
    });
}

/* ── Active Nav Link Highlighting ─────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    const pageInput = document.getElementById('currentPage');
    if (pageInput) {
        const navItem = document.getElementById(`nav-${pageInput.value}`);
        if (navItem) navItem.classList.add('active');
    }
});
