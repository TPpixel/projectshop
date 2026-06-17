const origFetch = window.fetch;
window.fetch = function(url, opts) {
    return origFetch(url, opts).then(res => {
        if (res.status === 401) {
            showToast('Необходимо войти в систему', 'warning');
        } else if (res.status === 403) {
            showToast('Недостаточно прав', 'danger');
        }
        return res;
    });
};

function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
}

function showToast(message, type) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const colors = { success: '#198754', danger: '#dc3545', warning: '#ffc107', info: '#0dcaf0' };
    const bg = colors[type] || colors.info;
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-white border-0 show';
    toast.style.background = bg;
    toast.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 4000);
}

function addToCart(productId) {
    const form = document.getElementById('add-to-cart-form');
    const url = form ? form.action : `/cart/add/${productId}/`;
    const csrf = getCSRFToken();
    fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `product_id=${productId}`,
    })
    .then(res => {
        if (res.redirected) {
            showToast('Товар добавлен в корзину!', 'success');
        } else if (res.status === 403) {
            showToast('Войдите, чтобы добавить товар в корзину', 'warning');
        } else {
            showToast('Ошибка при добавлении товара', 'danger');
        }
    })
    .catch(() => showToast('Ошибка сети', 'danger'));
}

function updateCartItem(itemId) {
    const form = document.querySelector(`form[data-item-id="${itemId}"]`);
    if (!form) return;
    const formData = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() },
        body: new URLSearchParams(formData),
    })
    .then(res => {
        if (res.redirected) { window.location.href = res.url; }
        else { showToast('Ошибка обновления', 'danger'); }
    })
    .catch(() => showToast('Ошибка сети', 'danger'));
}

function removeFromCart(itemId) {
    const form = document.querySelector(`form[data-remove-id="${itemId}"]`);
    if (!form) return;
    fetch(form.action, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() },
    })
    .then(res => {
        if (res.redirected) { window.location.href = res.url; }
        else { showToast('Ошибка удаления', 'danger'); }
    })
    .catch(() => showToast('Ошибка сети', 'danger'));
}

function loadProducts(url) {
    const container = document.getElementById('product-grid');
    const spinner = document.getElementById('loading-spinner');
    if (!container) return;
    if (spinner) spinner.classList.add('active');
    fetch(url)
        .then(res => { if (!res.ok) throw new Error('HTTP ' + res.status); return res.json(); })
        .then(data => {
            container.innerHTML = '';
            const products = data.results || data;
            if (products.length === 0) {
                container.innerHTML = '<p class="text-muted">Товары не найдены.</p>';
                return;
            }
            products.forEach(p => {
                const col = document.createElement('div');
                col.className = 'col-sm-6 col-md-4 col-lg-4 mb-4';
                const imgUrl = p.фото_товара || '/static/images/placeholder.svg';
                const inStock = p.количество_на_складе > 0;
                col.innerHTML = `
                    <div class="card h-100 ${inStock ? '' : 'out-of-stock'}">
                        <img src="${imgUrl}" class="card-img-top product-img" alt="${p.название}" loading="lazy">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${p.название}</h5>
                            <p class="text-muted small mb-1">${p.категория_название || ''}</p>
                            <p class="fw-bold fs-5 mt-auto">${p.цена} BYN</p>
                            <div class="d-flex gap-2">
                                <a href="/catalog/${p.id}/" class="btn btn-outline-info btn-sm flex-grow-1">Подробнее</a>
                                ${inStock ? `<button class="btn btn-success btn-sm flex-grow-1" onclick="addToCart(${p.id})">В корзину</button>`
                                          : `<button class="btn btn-secondary btn-sm flex-grow-1" disabled>Нет в наличии</button>`}
                            </div>
                        </div>
                    </div>`;
                container.appendChild(col);
            });
        })
        .catch(err => {
            if (container) container.innerHTML = `<div class="alert alert-danger">Ошибка загрузки: ${err.message}</div>`;
        })
        .finally(() => { if (spinner) spinner.classList.remove('active'); });
}
