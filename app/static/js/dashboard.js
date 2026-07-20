/**
 * dashboard.js — Loads summary stats into the three stat cards
 * Endpoint: GET /dashboard/summary → { total, active, inactive }
 */

document.addEventListener('DOMContentLoaded', async () => {
    const skeletons = document.querySelectorAll('.skeleton-card');
    const cards     = {
        total:    document.getElementById('card-total'),
        active:   document.getElementById('card-active'),
        inactive: document.getElementById('card-inactive'),
    };
    const stats = {
        total:    document.getElementById('stat-total'),
        active:   document.getElementById('stat-active'),
        inactive: document.getElementById('stat-inactive'),
    };

    try {
        const data = await apiFetch('/dashboard/summary');

        // Populate numbers
        if (stats.total)    stats.total.textContent    = data.total    ?? 0;
        if (stats.active)   stats.active.textContent   = data.active   ?? 0;
        if (stats.inactive) stats.inactive.textContent = data.inactive ?? 0;

        // Hide skeletons, show cards with animation
        skeletons.forEach(el => el.style.display = 'none');
        Object.values(cards).forEach((card, i) => {
            if (card) {
                card.style.display = '';
                card.style.animationDelay = `${i * 0.1}s`;
                card.classList.add('animate-in');
            }
        });

    } catch (error) {
        showToast(error.message || 'Failed to load dashboard statistics.', 'danger');
        skeletons.forEach(el => {
            el.classList.remove('shimmer');
            el.innerHTML = `
                <div class="d-flex align-items-center justify-content-center h-100 text-danger">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    <span class="small fw-medium">Failed to load</span>
                </div>`;
        });
    }
});
