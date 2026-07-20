/**
 * records.js — View Records page
 * Single fetch() feeds search, filter, and pagination.
 * Endpoint: GET /annalakshmis/?name=&mobile=&area=&status=&page=&page_size=
 * Response: { total, page, page_size, total_pages, items: [...] }
 */

document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1;
    const PAGE_SIZE = 10;

    // DOM refs
    const searchInput       = document.getElementById('searchInput');
    const areaFilter        = document.getElementById('areaFilter');
    const foodTypeFilter    = document.getElementById('foodTypeFilter');
    const statusFilter      = document.getElementById('statusFilter');
    const clearFiltersBtn   = document.getElementById('clearFilters');
    const tableLoading      = document.getElementById('tableLoading');
    const recordsTable      = document.getElementById('recordsTable');
    const recordsBody       = document.getElementById('recordsBody');
    const emptyState        = document.getElementById('emptyState');
    const paginationControls = document.getElementById('paginationControls');
    const totalBadge        = document.getElementById('totalBadge');



    // ── Main Fetch ──────────────────────────────────────────
    async function fetchRecords() {
        // Show loading, hide others
        tableLoading.style.display = '';
        recordsTable.style.display = 'none';
        emptyState.style.display   = 'none';
        paginationControls.innerHTML = '';

        // Build query params
        const params = new URLSearchParams();
        const q = searchInput.value.trim();
        if (q) {
            // If the query is all digits, search by mobile; otherwise name
            if (/^\d+$/.test(q)) {
                params.set('mobile', q);
            } else {
                params.set('name', q);
            }
        }
        if (areaFilter.value)   params.set('area', areaFilter.value);
        if (foodTypeFilter.value) params.set('food_type', foodTypeFilter.value);
        if (statusFilter.value) params.set('status', statusFilter.value);
        params.set('page', currentPage);
        params.set('page_size', PAGE_SIZE);

        try {
            const data = await apiFetch(`/annalakshmis/?${params.toString()}`);

            totalBadge.textContent = data.total ?? 0;

            if (!data.items || data.items.length === 0) {
                tableLoading.style.display = 'none';
                emptyState.style.display = '';
                return;
            }

            // Render rows
            recordsBody.innerHTML = '';
            data.items.forEach((item, idx) => {
                const tr = document.createElement('tr');
                tr.classList.add('animate-in');
                tr.style.animationDelay = `${idx * 0.04}s`;

                const rowNum = (currentPage - 1) * PAGE_SIZE + idx + 1;

                const vegBadge = item.veg_or_nonveg === 'veg'
                    ? `<span class="badge badge-veg"><i class="bi bi-circle-fill me-1" style="font-size:7px;"></i>Veg</span>`
                    : `<span class="badge badge-nonveg"><i class="bi bi-circle-fill me-1" style="font-size:7px;"></i>Non-Veg</span>`;

                const statusBadge = item.status === 'active'
                    ? `<span class="badge badge-active">Active</span>`
                    : `<span class="badge badge-inactive">Inactive</span>`;

                const archiveBtn = item.status === 'active'
                    ? `<button class="btn btn-sm btn-outline-danger archive-btn" data-id="${item.id}" data-name="${escapeHtml(item.full_name)}" title="Archive">
                           <i class="bi bi-archive"></i>
                       </button>`
                    : '';

                tr.innerHTML = `
                    <td class="ps-4 text-warm-muted">${rowNum}</td>
                    <td>
                        <div class="fw-semibold">${escapeHtml(item.full_name)}</div>
                        <div class="small text-warm-muted d-md-none">${escapeHtml(item.mobile_number)}</div>
                    </td>
                    <td class="d-none d-md-table-cell">${escapeHtml(item.mobile_number)}</td>
                    <td class="d-none d-lg-table-cell">${escapeHtml(item.area)}</td>
                    <td class="d-none d-lg-table-cell text-warm-muted">${escapeHtml(item.cuisine_specialization)}</td>
                    <td>${vegBadge}</td>
                    <td>${statusBadge}</td>
                    <td class="text-end pe-4">
                        <div class="btn-group btn-group-sm">
                            <a href="/pages/profile/${item.id}" class="btn btn-sm btn-outline-primary" title="View"><i class="bi bi-eye"></i></a>
                            <a href="/pages/edit/${item.id}" class="btn btn-sm btn-outline-secondary" title="Edit"><i class="bi bi-pencil"></i></a>
                            ${archiveBtn}
                        </div>
                    </td>
                `;
                recordsBody.appendChild(tr);
            });

            // Bind archive buttons
            recordsBody.querySelectorAll('.archive-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    handleArchive(btn.dataset.id, btn.dataset.name);
                });
            });

            // Show table, hide loading
            tableLoading.style.display = 'none';
            recordsTable.style.display = '';

            // Render pagination
            renderPagination(data.page, data.total_pages, data.total);

        } catch (error) {
            showToast(error.message || 'Failed to fetch records.', 'danger');
            tableLoading.style.display = 'none';
            emptyState.style.display = '';
            emptyState.querySelector('h3').textContent = 'Error loading records';
            emptyState.querySelector('p').textContent = error.message || 'An unexpected error occurred.';
        }
    }

    // ── Pagination ──────────────────────────────────────────
    function renderPagination(page, totalPages, totalRecords) {
        paginationControls.innerHTML = '';
        if (totalPages <= 1) {
            if (totalRecords > 0) {
                paginationControls.innerHTML = `<span class="pagination-info">Showing all ${totalRecords} record${totalRecords !== 1 ? 's' : ''}</span>`;
            }
            return;
        }

        // Info text
        const from = (page - 1) * PAGE_SIZE + 1;
        const to   = Math.min(page * PAGE_SIZE, totalRecords);
        const info = document.createElement('span');
        info.className = 'pagination-info';
        info.textContent = `Showing ${from}–${to} of ${totalRecords}`;
        paginationControls.appendChild(info);

        // Pagination buttons
        const ul = document.createElement('ul');
        ul.className = 'pagination pagination-custom mb-0';

        // Prev
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${page === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `<button class="page-link" data-page="${page - 1}" aria-label="Previous"><i class="bi bi-chevron-left"></i></button>`;
        ul.appendChild(prevLi);

        // Page numbers (window of 5)
        let start = Math.max(1, page - 2);
        let end   = Math.min(totalPages, start + 4);
        if (end - start < 4) start = Math.max(1, end - 4);

        for (let i = start; i <= end; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${i === page ? 'active' : ''}`;
            li.innerHTML = `<button class="page-link" data-page="${i}">${i}</button>`;
            ul.appendChild(li);
        }

        // Next
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${page === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `<button class="page-link" data-page="${page + 1}" aria-label="Next"><i class="bi bi-chevron-right"></i></button>`;
        ul.appendChild(nextLi);

        paginationControls.appendChild(ul);

        // Bind clicks
        ul.querySelectorAll('button.page-link').forEach(btn => {
            btn.addEventListener('click', () => {
                const target = parseInt(btn.dataset.page, 10);
                if (target && target !== page && target >= 1 && target <= totalPages) {
                    currentPage = target;
                    fetchRecords();
                    // Scroll to top of table
                    recordsTable.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }

    // ── Archive ─────────────────────────────────────────────
    async function handleArchive(id, name) {
        if (!confirm(`Are you sure you want to archive "${name}"?`)) return;

        try {
            await apiFetch(`/annalakshmis/${id}/archive`, { method: 'PATCH' });
            showToast(`${name} has been archived.`, 'success');
            fetchRecords(); // Refresh
        } catch (error) {
            showToast(error.message || 'Failed to archive record.', 'danger');
        }
    }

    // ── Event Bindings ──────────────────────────────────────
    searchInput.addEventListener('input', debounce(() => {
        currentPage = 1;
        fetchRecords();
    }, 300));

    areaFilter.addEventListener('input', debounce(() => {
        currentPage = 1;
        fetchRecords();
    }, 300));

    foodTypeFilter.addEventListener('change', () => {
        currentPage = 1;
        fetchRecords();
    });

    statusFilter.addEventListener('change', () => {
        currentPage = 1;
        fetchRecords();
    });

    clearFiltersBtn.addEventListener('click', () => {
        searchInput.value = '';
        areaFilter.value = '';
        foodTypeFilter.value = '';
        statusFilter.value = '';
        currentPage = 1;
        fetchRecords();
    });

    // ── Init ────────────────────────────────────────────────
    fetchRecords();
});
