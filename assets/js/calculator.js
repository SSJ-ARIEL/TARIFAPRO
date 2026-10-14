/* Calculadora orientativa: usa los datos elegidos, sin tarifas ni divisas externas. */
function calculateFreelanceScenario({ expenses, billableHours, vacationWeeks, savingsPercent, taxPercent }) {
  const errors = [];
  if (!Number.isFinite(expenses) || expenses < 0) errors.push('Introduce gastos válidos, iguales o superiores a cero.');
  if (!Number.isFinite(billableHours) || billableHours <= 0 || billableHours > 168) errors.push('Las horas facturables deben ser mayores que cero y no superar 168 por semana.');
  if (!Number.isFinite(vacationWeeks) || vacationWeeks < 0 || vacationWeeks >= 52) errors.push('El descanso debe ser igual o mayor que cero y menor que 52 semanas.');
  if (!Number.isFinite(savingsPercent) || savingsPercent < 0 || savingsPercent > 300) errors.push('El margen de ahorro debe estar entre 0 y 300 %.');
  if (!Number.isFinite(taxPercent) || taxPercent < 0 || taxPercent >= 100) errors.push('El porcentaje supuesto de impuestos debe estar entre 0 y menos de 100 %.');
  if (errors.length) throw new RangeError(errors.join(' '));

  const workingWeeks = 52 - vacationWeeks;
  const annualBillableHours = workingWeeks * billableHours;
  const annualExpenses = expenses * 12;
  const netAnnualTarget = annualExpenses * (1 + savingsPercent / 100);
  const grossAnnualTarget = netAnnualTarget / (1 - taxPercent / 100);
  const hourlyRate = grossAnnualTarget / annualBillableHours;
  const result = {
    workingWeeks, annualBillableHours, annualExpenses, netAnnualTarget,
    grossAnnualTarget, hourlyRate,
    dailyRate: hourlyRate * 8,
    // Average over all twelve months, including the chosen weeks off.
    monthlyAverage: grossAnnualTarget / 12
  };
  if (!Object.values(result).every(Number.isFinite)) throw new RangeError('Las cifras son demasiado grandes para calcular un resultado válido.');
  return result;
}

function calculateRate() {
  const read = (id) => {
    const value = document.getElementById(id)?.value?.trim();
    return value === '' || value == null ? NaN : Number(value);
  };
  const resultIds = ['res-hourly', 'res-daily', 'res-retainer', 'res-annual'];
  const resultCard = document.querySelector('.result-card');
  let status = document.getElementById('calc-error');
  let explanation = document.getElementById('calc-breakdown');
  if (resultCard && !status) {
    status = document.createElement('p');
    status.id = 'calc-error';
    status.setAttribute('role', 'status');
    status.style.cssText = 'margin-top:16px;color:#fbbf24;line-height:1.6;';
    resultCard.appendChild(status);
  }
  if (resultCard && !explanation) {
    explanation = document.createElement('p');
    explanation.id = 'calc-breakdown';
    explanation.style.cssText = 'margin-top:16px;line-height:1.6;color:#94a3b8;';
    resultCard.appendChild(explanation);
  }

  let scenario;
  try {
    scenario = calculateFreelanceScenario({
      expenses: read('c-expenses'), billableHours: read('c-hours'),
      vacationWeeks: read('c-vacations'), savingsPercent: read('c-savings'),
      taxPercent: read('c-taxes')
    });
  } catch (error) {
    if (status) status.textContent = error.message;
    if (explanation) explanation.textContent = '';
    resultIds.forEach(id => {
      const element = document.getElementById(id);
      if (element) element.textContent = '—';
    });
    return;
  }
  if (status) status.textContent = '';
  const currencySymbol = document.getElementById('c-currency')?.value || '$';
  const number = value => value.toLocaleString('es-ES', { maximumFractionDigits: 2, minimumFractionDigits: 2 });
  const format = value => currencySymbol + number(value);
  const values = {
    'res-hourly': format(scenario.hourlyRate) + ' / h',
    'res-daily': format(scenario.dailyRate),
    'res-retainer': format(scenario.monthlyAverage) + ' / mes',
    'res-annual': format(scenario.grossAnnualTarget)
  };
  Object.entries(values).forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
  });
  if (explanation) explanation.textContent = `${number(scenario.workingWeeks)} semanas × ${number(read('c-hours'))} horas = ${number(scenario.annualBillableHours)} horas facturables al año. Objetivo bruto ${format(scenario.grossAnnualTarget)} ÷ horas = ${format(scenario.hourlyRate)} / h. La media mensual divide el objetivo anual entre 12.`;
}

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#c-expenses, #c-hours, #c-vacations, #c-savings, #c-taxes, #c-currency').forEach(input => input.addEventListener('input', calculateRate));
    calculateRate();
  });
}
if (typeof module !== 'undefined') module.exports = { calculateFreelanceScenario };
