/* Proposal arithmetic; amounts and tax assumptions belong to the user. */
function calculateProposalTotals(items, taxPercent) {
  if (!Number.isFinite(taxPercent) || taxPercent < 0 || taxPercent > 100) {
    throw new RangeError('Introduce un porcentaje de impuesto entre 0 y 100; confirma el aplicable antes de enviar.');
  }
  const lineCents = items.map((item, index) => {
    if (!Number.isFinite(item.quantity) || item.quantity <= 0 || !Number.isFinite(item.price) || item.price < 0) {
      throw new RangeError(`Fila ${index + 1}: introduce una cantidad mayor que cero y un precio igual o mayor que cero.`);
    }
    const cents = Math.round((item.quantity * item.price + Number.EPSILON) * 100);
    if (!Number.isSafeInteger(cents)) throw new RangeError('Las cifras son demasiado grandes para calcular un presupuesto válido.');
    return cents;
  });
  const subtotalCents = lineCents.reduce((sum, cents) => sum + cents, 0);
  const taxCents = Math.round(subtotalCents * taxPercent / 100);
  const totalCents = subtotalCents + taxCents;
  if (![subtotalCents, taxCents, totalCents].every(Number.isSafeInteger)) throw new RangeError('Las cifras son demasiado grandes para calcular un presupuesto válido.');
  return { lineTotals: lineCents.map(cents => cents / 100), subtotal: subtotalCents / 100, taxAmount: taxCents / 100, total: totalCents / 100 };
}

function updateInvoiceTotals() {
  const rows = [...document.querySelectorAll('#invoice-items tr')];
  const read = element => element?.value?.trim() ? Number(element.value) : NaN;
  const status = document.getElementById('invoice-error');
  const printButton = document.getElementById('invoice-print');
  let amounts;
  try {
    if (!rows.length) throw new RangeError('Añade al menos un servicio antes de imprimir el presupuesto.');
    amounts = calculateProposalTotals(rows.map(row => ({
      quantity: read(row.querySelector('.item-qty')),
      price: read(row.querySelector('.item-price'))
    })), read(document.getElementById('inv-tax-pct')));
  } catch (error) {
    if (status) status.textContent = error.message;
    if (printButton) printButton.disabled = true;
    rows.forEach(row => { row.querySelector('.item-total').textContent = '—'; });
    ['inv-subtotal', 'inv-tax-amount', 'inv-grand-total'].forEach(id => {
      const element = document.getElementById(id);
      if (element) element.textContent = '—';
    });
    return;
  }
  if (status) status.textContent = '';
  if (printButton) printButton.disabled = false;
  const currency = document.getElementById('inv-currency')?.value || 'USD';
  const format = value => `${currency} ${value.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  rows.forEach((row, index) => { row.querySelector('.item-total').textContent = format(amounts.lineTotals[index]); });
  document.getElementById('inv-subtotal').textContent = format(amounts.subtotal);
  document.getElementById('inv-tax-amount').textContent = format(amounts.taxAmount);
  document.getElementById('inv-grand-total').textContent = format(amounts.total);
}

function addInvoiceRow() {
  const tbody = document.getElementById('invoice-items');
  if (!tbody) return;
  const row = document.createElement('tr');
  row.innerHTML = `
    <td><input type="text" aria-label="Descripción del servicio" value="Servicio adicional: indica el alcance" style="width:100%;"></td>
    <td><input type="number" aria-label="Cantidad" class="item-qty" value="1" min="0.01" step="0.01" style="width:60px;"></td>
    <td><input type="number" aria-label="Precio unitario" class="item-price" value="0" min="0" step="0.01" style="width:90px;"></td>
    <td class="item-total" style="font-weight:700;">—</td>
    <td><button type="button" aria-label="Eliminar servicio" onclick="this.closest('tr').remove(); updateInvoiceTotals();" style="background:none;border:none;color:#ef4444;cursor:pointer;">✕</button></td>`;
  tbody.appendChild(row);
  row.querySelectorAll('input').forEach(input => input.addEventListener('input', updateInvoiceTotals));
  updateInvoiceTotals();
}

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.item-qty, .item-price, #inv-tax-pct, #inv-currency').forEach(input => input.addEventListener('input', updateInvoiceTotals));
    const date = document.getElementById('inv-date');
    if (date && !date.value) {
      const today = new Date();
      date.value = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    }
    updateInvoiceTotals();
  });
}
if (typeof module !== 'undefined') module.exports = { calculateProposalTotals };
