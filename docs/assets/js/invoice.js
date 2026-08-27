/* Tarifa Pro - Proposal & Invoice Builder Engine */
function updateInvoiceTotals() {
  const rows = document.querySelectorAll('#invoice-items tr');
  let subtotal = 0;

  rows.forEach(row => {
    const qty = parseFloat(row.querySelector('.item-qty')?.value) || 0;
    const price = parseFloat(row.querySelector('.item-price')?.value) || 0;
    const total = qty * price;
    const totalCell = row.querySelector('.item-total');
    if (totalCell) totalCell.innerText = `$${total.toFixed(2)}`;
    subtotal += total;
  });

  const taxPct = (parseFloat(document.getElementById('inv-tax-pct')?.value) || 0) / 100;
  const taxAmount = subtotal * taxPct;
  const grandTotal = subtotal + taxAmount;

  const elSub = document.getElementById('inv-subtotal');
  const elTax = document.getElementById('inv-tax-amount');
  const elTotal = document.getElementById('inv-grand-total');

  if (elSub) elSub.innerText = `$${subtotal.toFixed(2)}`;
  if (elTax) elTax.innerText = `$${taxAmount.toFixed(2)}`;
  if (elTotal) elTotal.innerText = `$${grandTotal.toFixed(2)}`;
}

function addInvoiceRow() {
  const tbody = document.getElementById('invoice-items');
  if (!tbody) return;
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td><input type="text" value="Servicio profesional adicional" style="width: 100%;"></td>
    <td><input type="number" class="item-qty" value="1" min="1" style="width: 60px;"></td>
    <td><input type="number" class="item-price" value="150" min="0" style="width: 90px;"></td>
    <td class="item-total" style="font-weight: 700;">$150.00</td>
    <td><button onclick="this.closest('tr').remove(); updateInvoiceTotals();" style="background: none; border: none; color: #ef4444; cursor: pointer; font-weight: bold;">✕</button></td>
  `;
  tbody.appendChild(tr);
  tr.querySelectorAll('input').forEach(i => i.addEventListener('input', updateInvoiceTotals));
  updateInvoiceTotals();
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.item-qty, .item-price, #inv-tax-pct').forEach(i => {
    i.addEventListener('input', updateInvoiceTotals);
  });
  updateInvoiceTotals();
});
