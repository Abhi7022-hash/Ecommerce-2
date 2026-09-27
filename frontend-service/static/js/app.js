// ===== STATE =====
let currentUser = null;
let token = null;
let cart = JSON.parse(localStorage.getItem("cart") || "[]");
let allProducts = [];

// ===== INIT =====
document.addEventListener("DOMContentLoaded", () => {
  const savedToken = localStorage.getItem("token");
  const savedUser = localStorage.getItem("user");
  if (savedToken && savedUser) {
    token = savedToken;
    currentUser = JSON.parse(savedUser);
    updateAuthUI();
  }
  updateCartBadge();
  showPage("home");
});

// ===== NAVIGATION =====
function showPage(page) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
  const el = document.getElementById("page-" + page);
  if (el) el.classList.add("active");

  // mark active nav link
  document.querySelectorAll(".nav-link").forEach(l => {
    if (l.getAttribute("onclick") && l.getAttribute("onclick").includes(`'${page}'`)) {
      l.classList.add("active");
    }
  });

  if (page === "products") loadProducts();
  if (page === "cart") renderCart();
  if (page === "orders") {
    if (!token) { showToast("Please login to view orders", "error"); showPage("login"); return; }
    loadOrders();
  }
}

// ===== TOAST =====
function showToast(msg, type = "") {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "toast show" + (type ? " " + type : "");
  setTimeout(() => { t.className = "toast"; }, 3000);
}

// ===== AUTH =====
async function register() {
  const name = document.getElementById("regName").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value;
  if (!name || !email || !password) return showToast("All fields required", "error");

  try {
    const res = await fetch(`${USER_SERVICE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });
    const data = await res.json();
    if (!res.ok) return showToast(data.error || "Registration failed", "error");
    showToast("Account created! Please login.", "success");
    showPage("login");
  } catch (e) {
    showToast("Cannot reach user service", "error");
  }
}

async function login() {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value;
  if (!email || !password) return showToast("All fields required", "error");

  try {
    const res = await fetch(`${USER_SERVICE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) return showToast(data.error || "Login failed", "error");

    token = data.token;
    currentUser = data.user;
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(currentUser));
    updateAuthUI();
    showToast("Welcome back, " + currentUser.name + "!", "success");
    showPage("home");
  } catch (e) {
    showToast("Cannot reach user service", "error");
  }
}

function logout() {
  token = null;
  currentUser = null;
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  updateAuthUI();
  showToast("Logged out successfully");
  showPage("home");
}

function updateAuthUI() {
  const authButtons = document.getElementById("authButtons");
  const userInfo = document.getElementById("userInfo");
  const ordersLink = document.getElementById("ordersLink");

  if (currentUser) {
    authButtons.style.display = "none";
    userInfo.style.display = "flex";
    document.getElementById("userGreeting").textContent = "Hi, " + currentUser.name;
    ordersLink.style.display = "";
  } else {
    authButtons.style.display = "flex";
    userInfo.style.display = "none";
    ordersLink.style.display = "none";
  }
}

// ===== PRODUCTS =====
async function loadProducts() {
  const grid = document.getElementById("productGrid");
  grid.innerHTML = '<div class="loading">Loading products...</div>';
  const category = document.getElementById("categoryFilter").value;
  const url = category
  ? `${PRODUCT_SERVICE}?category=${encodeURIComponent(category)}`
  : PRODUCT_SERVICE;
  try {
    const res = await fetch(url);
    allProducts = await res.json();
    renderProducts(allProducts);
  } catch (e) {
    grid.innerHTML = '<div class="empty-state">⚠️ Cannot reach product service.</div>';
  }
}

function filterProducts() {
  loadProducts();
}

function renderProducts(products) {
  const grid = document.getElementById("productGrid");
  if (!products.length) {
    grid.innerHTML = '<div class="empty-state">No products found.</div>';
    return;
  }
  grid.innerHTML = products.map(p => `
    <div class="product-card">
      <div class="product-emoji">${p.image || "📦"}</div>
      <div class="product-category">${p.category}</div>
      <div class="product-name">${p.name}</div>
      <div class="product-desc">${p.description}</div>
      <div class="product-footer">
        <div>
          <div class="product-price">₹${p.price.toLocaleString()}</div>
          <div class="product-stock">In stock: ${p.stock}</div>
        </div>
        <button class="btn btn-primary" onclick="addToCart('${p._id}', '${p.name.replace(/'/g,"\\'")}', ${p.price}, '${p.image || "📦"}')">
          Add +
        </button>
      </div>
    </div>
  `).join("");
}

// ===== CART =====
function addToCart(id, name, price, image) {
  const existing = cart.find(i => i.id === id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ id, name, price, image, quantity: 1 });
  }
  saveCart();
  updateCartBadge();
  showToast(name + " added to cart!", "success");
}

function removeFromCart(id) {
  cart = cart.filter(i => i.id !== id);
  saveCart();
  updateCartBadge();
  renderCart();
}

function changeQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.quantity += delta;
  if (item.quantity <= 0) return removeFromCart(id);
  saveCart();
  updateCartBadge();
  renderCart();
}

function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
}

function updateCartBadge() {
  const total = cart.reduce((sum, i) => sum + i.quantity, 0);
  document.getElementById("cartBadge").textContent = total;
}

function renderCart() {
  const content = document.getElementById("cartContent");
  if (!cart.length) {
    content.innerHTML = '<div class="empty-state">🛒 Your cart is empty. <a href="#" onclick="showPage(\'products\')">Shop now</a></div>';
    return;
  }
  const total = cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
  content.innerHTML = `
    <div class="cart-table">
      ${cart.map(item => `
        <div class="cart-item">
          <div class="cart-item-emoji">${item.image}</div>
          <div>
            <div class="cart-item-name">${item.name}</div>
            <div style="color:var(--text-light);font-size:.85rem;">₹${item.price.toLocaleString()} each</div>
          </div>
          <div class="qty-control">
            <button class="qty-btn" onclick="changeQty('${item.id}', -1)">−</button>
            <span class="qty-num">${item.quantity}</span>
            <button class="qty-btn" onclick="changeQty('${item.id}', 1)">+</button>
          </div>
          <div class="cart-item-price">₹${(item.price * item.quantity).toLocaleString()}</div>
          <button class="btn btn-danger" onclick="removeFromCart('${item.id}')" style="padding:.4rem .8rem;font-size:.8rem;">Remove</button>
        </div>
      `).join("")}
    </div>
    <div class="cart-footer">
      <div class="cart-total">Total: <span>₹${total.toLocaleString()}</span></div>
      <button class="btn btn-primary btn-lg" onclick="openCheckout()">Proceed to Checkout →</button>
    </div>
  `;
}

// ===== CHECKOUT =====
function openCheckout() {
  if (!token) {
    showToast("Please login to checkout", "error");
    showPage("login");
    return;
  }
  if (!cart.length) return showToast("Your cart is empty", "error");

  const total = cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const summary = document.getElementById("orderSummary");
  summary.innerHTML = `
    ${cart.map(i => `<div class="row"><span>${i.name} × ${i.quantity}</span><span>₹${(i.price * i.quantity).toLocaleString()}</span></div>`).join("")}
    <div class="row total"><span>Total</span><span>₹${total.toLocaleString()}</span></div>
  `;
  document.getElementById("checkoutModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("checkoutModal").style.display = "none";
}

async function placeOrder() {
  const address = document.getElementById("deliveryAddress").value.trim();
  if (!address) return showToast("Please enter delivery address", "error");

  const items = cart.map(i => ({ product_id: i.id, quantity: i.quantity }));
  try {
    const res = await fetch(`${ORDER_SERVICE}/orders`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
      },
      body: JSON.stringify({ items, address }),
    });
    const data = await res.json();
    if (!res.ok) return showToast(data.error || "Order failed", "error");

    cart = [];
    saveCart();
    updateCartBadge();
    closeModal();
    showToast("🎉 Order placed successfully!", "success");
    showPage("orders");
  } catch (e) {
    showToast("Cannot reach order service", "error");
  }
}

// ===== ORDERS =====
async function loadOrders() {
  const content = document.getElementById("ordersContent");
  content.innerHTML = '<div class="loading">Loading your orders...</div>';
  try {
    const res = await fetch(`${ORDER_SERVICE}/orders`, {
      headers: { "Authorization": "Bearer " + token },
    });
    const orders = await res.json();
    if (!res.ok) {
      content.innerHTML = '<div class="empty-state">Could not load orders.</div>';
      return;
    }
    if (!orders.length) {
      content.innerHTML = '<div class="empty-state">📦 No orders yet. <a href="#" onclick="showPage(\'products\')">Start shopping</a></div>';
      return;
    }
    content.innerHTML = orders.reverse().map(order => `
      <div class="order-card">
        <div class="order-header">
          <div>
            <div style="font-weight:700;font-size:1rem;">Order</div>
            <div class="order-id">#${order._id.slice(-8).toUpperCase()}</div>
          </div>
          <div style="text-align:right;">
            <span class="order-status status-${order.status}">${order.status}</span>
            <div class="order-date" style="margin-top:.3rem;">${new Date(order.created_at).toLocaleDateString()}</div>
          </div>
        </div>
        <div class="order-items">
          ${order.items.map(i => `
            <div class="order-item-row">
              <span>${i.name} × ${i.quantity}</span>
              <span>₹${i.subtotal.toLocaleString()}</span>
            </div>
          `).join("")}
          <div class="order-total-row">
            <span>Total</span>
            <span>₹${order.total.toLocaleString()}</span>
          </div>
          <div style="margin-top:.75rem;font-size:.85rem;color:var(--text-light);">📍 ${order.address}</div>
        </div>
      </div>
    `).join("");
  } catch (e) {
    content.innerHTML = '<div class="empty-state">⚠️ Cannot reach order service.</div>';
  }
}

// Close modal on overlay click
document.getElementById("checkoutModal").addEventListener("click", function(e) {
  if (e.target === this) closeModal();
});
