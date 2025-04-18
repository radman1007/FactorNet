// script.js

function addItem() {
    const container = document.getElementById('itemsContainer');
    const itemDiv = document.createElement('div');
    itemDiv.innerHTML = `
      <input type="text" placeholder="نام آیتم" required>
      <textarea placeholder="توضیحات"></textarea>
      <input type="number" placeholder="تعداد" value="1" oninput="calculateTotal()" class="quantity">
      <input type="number" placeholder="قیمت واحد" oninput="calculateTotal()" class="price">
      <hr>
    `;
    container.appendChild(itemDiv);
    calculateTotal();
  }
  
  function calculateTotal() {
    const prices = document.querySelectorAll('.price');
    const quantities = document.querySelectorAll('.quantity');
    let subtotal = 0;
    for (let i = 0; i < prices.length; i++) {
      const price = parseFloat(prices[i].value) || 0;
      const quantity = parseInt(quantities[i].value) || 0;
      subtotal += price * quantity;
    }
  
    const discount = parseFloat(document.getElementById('discount').value) || 0;
    const tax = parseFloat(document.getElementById('tax').value) || 0;
    const taxAmount = ((subtotal - discount) * tax) / 100;
    const total = subtotal - discount + taxAmount;
  
    document.getElementById('totalAmount').innerText = total.toLocaleString();
  }
  
  
  // امضای دیجیتال با canvas
  const canvas = document.getElementById('signaturePad');
  const ctx = canvas.getContext('2d');
  let drawing = false;
  
  canvas.addEventListener('mousedown', () => drawing = true);
  canvas.addEventListener('mouseup', () => drawing = false);
  canvas.addEventListener('mousemove', draw);
  
  function draw(e) {
    if (!drawing) return;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#1b1f3b';
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
  }
  
  function clearSignature() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }