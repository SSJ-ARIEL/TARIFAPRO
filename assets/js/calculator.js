/* Calculadora orientativa: no consulta tarifas ni tipos de cambio en tiempo real. */
function calculateRate() {
  const read = (id) => {
    const element = document.getElementById(id);
    const value = element?.value?.trim();
    return value === '' || value == null ? NaN : Number(value);
  };

  const expenses = read('c-expenses');
  const billableHours = read('c-hours');
  const vacationWeeks = read('c-vacations');
  const savingsPercent = read('c-savings');
  const taxPercent = read('c-taxes');
  const currencySymbol = document.getElementById('c-currency')?.value || '$';

  const resultIds = ['res-hourly', 'res-daily', 'res-retainer', 'res-annual'];
  const errors = [];
  if (!Number.isFinite(expenses) || expenses < 0) errors.push('Introduce gastos válidos, iguales o superiores a cero.');
  if (!Number.isFinite(billableHours) || billableHours <= 0 || billableHours > 168) errors.push('Las horas facturables deben ser mayores que cero y no superar 168 por semana.');
  if (!Number.isFinite(vacationWeeks) || vacationWeeks < 0 || vacationWeeks >= 52) errors.push('Las semanas de descanso deben estar entre 0 y 51.');
  if (!Number.isFinite(savingsPercent) || savingsPercent < 0 || savingsPercent > 300) errors.push('El margen de ahorro debe estar entre 0 y 300%.');
  if (!Number.isFinite(taxPercent) || taxPercent < 0 || taxPercent >= 100) errors.push('El porcentaje estimado de impuestos debe estar entre 0 y menos de 100%.');

  const resultCard = document.querySelector('.result-card');
  let status = document.getElementById('calc-error');
  if (resultCard && !status) {
    status = document.createElement('p');
    status.id = 'calc-error';
    status.setAttribute('role', 'status');
    status.style.cssText = 'margin-top:16px;color:#fbbf24;line-height:1.6;';
    resultCard.appendChild(status);
  }
  if (status) status.textContent = errors.join(' ');

  if (errors.length) {
    resultIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.textContent = '—';
    });
    return;
  }

  const workingWeeks = 52 - vacationWeeks;
  const totalBillableHoursYear = workingWeeks * billableHours;
  const annualExpenses = expenses * 12;
  const targetNetAnnual = annualExpenses * (1 + savingsPercent / 100);
  const targetGrossAnnual = targetNetAnnual / (1 - taxPercent / 100);
  const hourlyRate = targetGrossAnnual / totalBillableHoursYear;
  const dayRate = hourlyRate * 8;
  const retainerRate = hourlyRate * billableHours * 4.2;

  const format = (value) => currencySymbol + value.toLocaleString('es-ES', { maximumFractionDigits: 2, minimumFractionDigits: 2 });
  const values = {
    'res-hourly': format(hourlyRate) + ' / h',
    'res-daily': format(dayRate),
    'res-retainer': format(retainerRate) + ' / mes',
    'res-annual': format(targetGrossAnnual)
  };
  Object.entries(values).forEach(([id, value]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('#c-expenses, #c-hours, #c-vacations, #c-savings, #c-taxes, #c-currency');
  inputs.forEach((input) => input.addEventListener('input', calculateRate));
  calculateRate();
});
