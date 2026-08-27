/* Tarifa Pro - Interactive Freelance Rate Calculator Engine */
function calculateRate() {
  const expenses = parseFloat(document.getElementById('c-expenses')?.value) || 1200;
  const billableHours = parseFloat(document.getElementById('c-hours')?.value) || 25;
  const vacationWeeks = parseFloat(document.getElementById('c-vacations')?.value) || 4;
  const savingsPct = (parseFloat(document.getElementById('c-savings')?.value) || 20) / 100;
  const taxPct = (parseFloat(document.getElementById('c-taxes')?.value) || 15) / 100;
  const currencySymbol = document.getElementById('c-currency')?.value || '$';

  // Calculations
  const workingWeeks = Math.max(1, 52 - vacationWeeks);
  const totalBillableHoursYear = workingWeeks * billableHours;
  const annualExpenses = expenses * 12;
  const targetNetAnnual = annualExpenses * (1 + savingsPct);
  const targetGrossAnnual = targetNetAnnual / Math.max(0.01, (1 - taxPct));

  const hourlyRate = Math.round(targetGrossAnnual / totalBillableHoursYear);
  const dayRate = Math.round(hourlyRate * 7.5);
  const retainerRate = Math.round(hourlyRate * billableHours * 4.2);

  // Update UI
  const elHour = document.getElementById('res-hourly');
  const elDay = document.getElementById('res-daily');
  const elRetainer = document.getElementById('res-retainer');
  const elAnnual = document.getElementById('res-annual');

  if (elHour) elHour.innerText = `${currencySymbol}${hourlyRate} / h`;
  if (elDay) elDay.innerText = `${currencySymbol}${dayRate}`;
  if (elRetainer) elRetainer.innerText = `${currencySymbol}${retainerRate} / mes`;
  if (elAnnual) elAnnual.innerText = `${currencySymbol}${Math.round(targetGrossAnnual).toLocaleString()}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('#c-expenses, #c-hours, #c-vacations, #c-savings, #c-taxes, #c-currency');
  inputs.forEach(i => i.addEventListener('input', calculateRate));
  calculateRate();
});
