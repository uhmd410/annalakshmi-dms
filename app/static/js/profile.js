/**
 * profile.js — Chef Profile page
 * Endpoint: GET  /annalakshmis/{id}
 * Archive:  PATCH /annalakshmis/{id}/archive
 */

document.addEventListener('DOMContentLoaded', async () => {
    const recordIdEl = document.getElementById('recordId');
    if (!recordIdEl) return;
    const recordId = recordIdEl.value;

    const profileLoading = document.getElementById('profileLoading');
    const profileContent = document.getElementById('profileContent');
    const archiveBtn     = document.getElementById('archiveBtn');

    try {
        const data = await apiFetch(`/annalakshmis/${recordId}`);

        // ── Header ──────────────────────────────────────────
        const profileName = document.getElementById('profileName');
        if (profileName) profileName.textContent = data.full_name;

        // Status badge in header
        const profileStatus = document.getElementById('profileStatus');
        if (profileStatus) {
            if (data.status === 'active') {
                profileStatus.textContent = '● Active';
            } else {
                profileStatus.textContent = '● Inactive';
                if (archiveBtn) archiveBtn.style.display = 'none';
            }
        }

        // Veg/Non-veg badge in header
        const profileVeg = document.getElementById('profileVeg');
        if (profileVeg) {
            if (data.veg_or_nonveg === 'veg') {
                profileVeg.textContent = '🌿 Vegetarian';
            } else {
                profileVeg.textContent = '🍗 Non-Vegetarian';
            }
        }

        // ── Detail Fields ───────────────────────────────────
        const fieldMap = {
            'field-fullname':   data.full_name,
            'field-mobile':     data.mobile_number,
            'field-email':      data.email,
            'field-address':    data.address,
            'field-area':       data.area,
            'field-city':       data.city,
            'field-state':      data.state,
            'field-pincode':    data.pin_code,
            'field-cuisine':    data.cuisine_specialization,
            'field-dishes':     data.signature_dishes,
            'field-veg':        data.veg_or_nonveg === 'veg' ? 'Vegetarian' : 'Non-Vegetarian',
            'field-timings':    data.available_timings,
            'field-maxorders':  data.max_orders_per_day,
        };

        for (const [id, value] of Object.entries(fieldMap)) {
            const el = document.getElementById(id);
            if (el) {
                el.textContent = (value !== null && value !== undefined && value !== '') ? value : '—';
            }
        }

        // Status field in body
        const statusEl = document.getElementById('field-status');
        if (statusEl) {
            if (data.status === 'active') {
                statusEl.innerHTML = '<span class="badge badge-active">Active</span>';
            } else {
                statusEl.innerHTML = '<span class="badge badge-inactive">Inactive</span>';
            }
        }

        // Date fields
        const djEl = document.getElementById('field-datejoined');
        if (djEl) djEl.textContent = formatDate(data.date_joined);

        const caEl = document.getElementById('field-createdat');
        if (caEl) caEl.textContent = formatDateTime(data.created_at);

        const uaEl = document.getElementById('field-updatedat');
        if (uaEl) uaEl.textContent = formatDateTime(data.updated_at);

        // Edit link
        const editLink = document.getElementById('editLink');
        if (editLink) editLink.href = `/pages/edit/${recordId}`;

        // ── Show content ────────────────────────────────────
        if (profileLoading) profileLoading.style.display = 'none';
        if (profileContent) {
            profileContent.style.display = '';
            profileContent.classList.add('animate-in');
        }

        // ── Archive handler ─────────────────────────────────
        if (archiveBtn) {
            archiveBtn.addEventListener('click', async () => {
                if (!confirm(`Are you sure you want to archive "${data.full_name}"?`)) return;

                archiveBtn.disabled = true;
                archiveBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Archiving…';

                try {
                    await apiFetch(`/annalakshmis/${recordId}/archive`, { method: 'PATCH' });
                    showToast(`${data.full_name} has been archived.`, 'success');
                    // Reload to reflect updated status
                    setTimeout(() => window.location.reload(), 800);
                } catch (error) {
                    showToast(error.message || 'Failed to archive.', 'danger');
                    archiveBtn.disabled = false;
                    archiveBtn.innerHTML = '<i class="bi bi-archive me-2"></i>Archive';
                }
            });
        }

    } catch (error) {
        showToast(error.message || 'Failed to load profile.', 'danger');
        if (profileLoading) {
            profileLoading.innerHTML = `
                <div class="text-center py-5">
                    <div class="text-danger mb-3"><i class="bi bi-exclamation-triangle fs-1"></i></div>
                    <h5 class="fw-bold">Failed to load profile</h5>
                    <p class="text-warm-muted">${escapeHtml(error.message)}</p>
                    <a href="/pages/records" class="btn btn-primary mt-3">Back to Records</a>
                </div>`;
        }
    }
});
