/**
 * form.js — Handles Add & Edit forms
 * Add  → POST /annalakshmis/
 * Edit → GET  /annalakshmis/{id} (pre-fill) + PUT /annalakshmis/{id} (save)
 *
 * Works with <select> for veg_or_nonveg (not radio buttons).
 * Targets submit button by id="submitBtn" or falls back to form's [type=submit].
 */

document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('addForm') || document.getElementById('editForm');
    if (!form) return;

    const isEdit        = form.id === 'editForm';
    const recordIdEl    = document.getElementById('recordId');
    const recordId      = recordIdEl ? recordIdEl.value : null;
    const formLoading   = document.getElementById('formLoading');
    const formContent   = document.getElementById('formContent');
    const submitBtn     = document.getElementById('submitBtn') || form.querySelector('[type="submit"]');

    // ── Pre-fill on Edit ────────────────────────────────────
    if (isEdit && recordId) {
        try {
            const data = await apiFetch(`/annalakshmis/${recordId}`);

            // Text / textarea fields
            const textFields = [
                'full_name', 'mobile_number', 'email', 'address',
                'area', 'city', 'state', 'pin_code',
                'cuisine_specialization', 'signature_dishes', 'available_timings',
            ];
            textFields.forEach(f => {
                const el = document.getElementById(f);
                if (el) el.value = data[f] ?? '';
            });

            // Number
            const maxOrd = document.getElementById('max_orders_per_day');
            if (maxOrd) maxOrd.value = data.max_orders_per_day ?? 10;

            // Date
            const dateEl = document.getElementById('date_joined');
            if (dateEl && data.date_joined) dateEl.value = data.date_joined;

            // Select: veg_or_nonveg
            const vegSel = document.getElementById('veg_or_nonveg');
            if (vegSel && data.veg_or_nonveg) vegSel.value = data.veg_or_nonveg;

            // Select: status
            const statusSel = document.getElementById('status');
            if (statusSel && data.status) statusSel.value = data.status;

            // Display name in header
            const nameDisp = document.getElementById('editNameDisplay');
            if (nameDisp) nameDisp.textContent = data.full_name;

            // Swap skeleton → form
            if (formLoading) formLoading.style.display = 'none';
            if (formContent) {
                formContent.style.display = '';
                formContent.classList.add('animate-in');
            }
        } catch (error) {
            showToast(error.message || 'Failed to load record.', 'danger');
            if (formLoading) {
                formLoading.innerHTML = `
                    <div class="text-center py-5">
                        <div class="text-danger mb-3"><i class="bi bi-exclamation-triangle fs-1"></i></div>
                        <h5 class="fw-bold">Failed to load record</h5>
                        <p class="text-warm-muted">${escapeHtml(error.message)}</p>
                        <a href="/pages/records" class="btn btn-primary mt-2">Back to Records</a>
                    </div>`;
            }
        }
    } else {
        // Add form — no loading needed
        if (formLoading) formLoading.style.display = 'none';
        if (formContent) formContent.style.display = '';
    }

    // ── Field-Error Helpers ─────────────────────────────────
    function showFieldError(fieldId, message) {
        const el = document.getElementById(fieldId);
        if (!el) return;

        el.classList.add('is-invalid');

        // Find or create the feedback element
        let feedback = el.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
        }
    }

    function clearAllErrors() {
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    }

    // ── Client-Side Validation ──────────────────────────────
    function validateForm() {
        clearAllErrors();
        let valid = true;

        const requireMinLen = (id, min) => {
            const el = document.getElementById(id);
            if (!el) return;
            const val = el.value.trim();
            if (!val || val.length < min) {
                showFieldError(id, `Required (min ${min} characters).`);
                valid = false;
            }
        };

        // Required string fields
        requireMinLen('full_name', 2);
        requireMinLen('address', 5);
        requireMinLen('area', 2);
        requireMinLen('city', 2);
        requireMinLen('state', 2);
        requireMinLen('cuisine_specialization', 2);

        // Mobile: 10 digits starting 6-9
        const mobileEl = document.getElementById('mobile_number');
        if (mobileEl && !/^[6-9]\d{9}$/.test(mobileEl.value.trim())) {
            showFieldError('mobile_number', 'Must be 10 digits starting with 6–9.');
            valid = false;
        }

        // PIN: exactly 6 digits
        const pinEl = document.getElementById('pin_code');
        if (pinEl && !/^\d{6}$/.test(pinEl.value.trim())) {
            showFieldError('pin_code', 'Must be exactly 6 digits.');
            valid = false;
        }

        // Email (optional but must be valid if filled)
        const emailEl = document.getElementById('email');
        if (emailEl && emailEl.value.trim()) {
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailEl.value.trim())) {
                showFieldError('email', 'Invalid email format.');
                valid = false;
            }
        }

        // Max orders: integer 1–200
        const maxEl = document.getElementById('max_orders_per_day');
        if (maxEl) {
            const v = parseInt(maxEl.value, 10);
            if (isNaN(v) || v <= 0 || v > 200) {
                showFieldError('max_orders_per_day', 'Must be between 1 and 200.');
                valid = false;
            }
        }

        // Date joined: required, not in the future
        const djEl = document.getElementById('date_joined');
        if (djEl) {
            if (!djEl.value) {
                showFieldError('date_joined', 'Date joined is required.');
                valid = false;
            } else if (new Date(djEl.value) > new Date()) {
                showFieldError('date_joined', 'Cannot be in the future.');
                valid = false;
            }
        }

        // veg_or_nonveg select required
        const vegEl = document.getElementById('veg_or_nonveg');
        if (vegEl && !vegEl.value) {
            showFieldError('veg_or_nonveg', 'Please select food type.');
            valid = false;
        }

        // Status
        const statusEl = document.getElementById('status');
        if (statusEl && !statusEl.value) {
            showFieldError('status', 'Please select a status.');
            valid = false;
        }

        return valid;
    }

    // ── Clear individual error on input ──────────────────────
    form.querySelectorAll('input, textarea, select').forEach(el => {
        el.addEventListener('input', () => el.classList.remove('is-invalid'));
        el.addEventListener('change', () => el.classList.remove('is-invalid'));
    });

    // ── Form Submit ─────────────────────────────────────────
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!validateForm()) return;

        const origHTML = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Saving…';

        const payload = {
            full_name:               document.getElementById('full_name').value.trim(),
            mobile_number:           document.getElementById('mobile_number').value.trim(),
            email:                   document.getElementById('email').value.trim() || null,
            address:                 document.getElementById('address').value.trim(),
            area:                    document.getElementById('area').value.trim(),
            city:                    document.getElementById('city').value.trim(),
            state:                   document.getElementById('state').value.trim(),
            pin_code:                document.getElementById('pin_code').value.trim(),
            cuisine_specialization:  document.getElementById('cuisine_specialization').value.trim(),
            veg_or_nonveg:           document.getElementById('veg_or_nonveg').value,
            signature_dishes:        document.getElementById('signature_dishes').value.trim() || null,
            available_timings:       document.getElementById('available_timings').value.trim() || null,
            max_orders_per_day:      parseInt(document.getElementById('max_orders_per_day').value, 10),
            date_joined:             document.getElementById('date_joined').value,
            status:                  document.getElementById('status').value,
        };

        try {
            if (isEdit) {
                await apiFetch(`/annalakshmis/${recordId}`, {
                    method: 'PUT',
                    body: JSON.stringify(payload),
                });
                showToast('Record updated successfully!', 'success');
                setTimeout(() => { window.location.href = `/pages/profile/${recordId}`; }, 800);
            } else {
                const created = await apiFetch('/annalakshmis/', {
                    method: 'POST',
                    body: JSON.stringify(payload),
                });
                showToast('Record created successfully!', 'success');
                setTimeout(() => { window.location.href = `/pages/profile/${created.id}`; }, 800);
            }
        } catch (error) {
            showToast(error.message || 'Failed to save record.', 'danger');

            // Show per-field inline errors from 422 details
            if (error.status === 422 && error.details && Array.isArray(error.details)) {
                error.details.forEach(d => {
                    if (d.field && d.message) {
                        showFieldError(d.field, d.message);
                    }
                });
            }

            // Show inline error if mobile number is already registered
            if (error.status === 400 && error.message && error.message.toLowerCase().includes('mobile number')) {
                showFieldError('mobile_number', error.message);
            }

            submitBtn.disabled = false;
            submitBtn.innerHTML = origHTML;
        }
    });
});
