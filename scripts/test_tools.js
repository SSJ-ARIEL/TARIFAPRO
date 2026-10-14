/* Regression checks for monetary arithmetic and the examples published on site. */
const assert = require('node:assert/strict');
const { calculateFreelanceScenario } = require('../assets/js/calculator.js');
const { calculateProposalTotals } = require('../assets/js/invoice.js');
const close = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-9, `${actual} should equal ${expected}`);

const base = { expenses: 1200, billableHours: 20, vacationWeeks: 4, savingsPercent: 15, taxPercent: 10 };
const scenario = calculateFreelanceScenario(base);
close(scenario.annualBillableHours, 960);
close(scenario.netAnnualTarget, 16560);
close(scenario.grossAnnualTarget, 18400);
close(scenario.hourlyRate, 18400 / 960);
close(scenario.dailyRate, 18400 / 120);
close(scenario.monthlyAverage * 12, scenario.grossAnnualTarget);
close(scenario.hourlyRate * scenario.annualBillableHours, scenario.grossAnnualTarget);
close(scenario.grossAnnualTarget * (1 - base.taxPercent / 100), scenario.netAnnualTarget);
close(calculateFreelanceScenario({ ...base, billableHours: 15 }).hourlyRate, 18400 / 720);
close(calculateFreelanceScenario({ ...base, billableHours: 25 }).hourlyRate, 18400 / 1200);
assert.ok(calculateFreelanceScenario({ ...base, vacationWeeks: 8 }).hourlyRate > scenario.hourlyRate);
close(calculateFreelanceScenario({ expenses: 1000, billableHours: 20, vacationWeeks: 4, savingsPercent: 0, taxPercent: 0 }).hourlyRate, 12.5);
assert.equal(calculateFreelanceScenario({ ...base, expenses: 0 }).grossAnnualTarget, 0);
for (const invalid of [
  { expenses: NaN }, { expenses: -1 }, { expenses: 1e308 },
  { billableHours: 0 }, { billableHours: Infinity }, { billableHours: 169 },
  { vacationWeeks: 52 }, { vacationWeeks: -1 },
  { savingsPercent: -1 }, { taxPercent: 100 }, { taxPercent: -1 }
]) assert.throws(() => calculateFreelanceScenario({ ...base, ...invalid }), RangeError);

assert.deepEqual(calculateProposalTotals([{ quantity: 1, price: 650 }, { quantity: 1, price: 200 }], 16), {
  lineTotals: [650, 200], subtotal: 850, taxAmount: 136, total: 986
});
assert.deepEqual(calculateProposalTotals([{ quantity: 0.5, price: 0.03 }, { quantity: 0.5, price: 0.03 }], 0), {
  lineTotals: [0.02, 0.02], subtotal: 0.04, taxAmount: 0, total: 0.04
});
assert.deepEqual(calculateProposalTotals([{ quantity: 1, price: 19.99 }], 15), {
  lineTotals: [19.99], subtotal: 19.99, taxAmount: 3, total: 22.99
});
assert.equal(calculateProposalTotals([{ quantity: 2.5, price: 20 }], 0).total, 50);
assert.equal(calculateProposalTotals([{ quantity: 1, price: 0 }], 0).total, 0);
for (const [items, tax] of [
  [[{ quantity: -1, price: 1 }], 0], [[{ quantity: 0, price: 1 }], 0],
  [[{ quantity: 1, price: -1 }], 0], [[{ quantity: NaN, price: 1 }], 0],
  [[{ quantity: 1, price: Infinity }], 0], [[{ quantity: 1, price: 1e308 }], 0],
  [[{ quantity: 1, price: 1 }], -1], [[{ quantity: 1, price: 1 }], 101],
  [[{ quantity: 1, price: 1 }], NaN]
]) assert.throws(() => calculateProposalTotals(items, tax), RangeError);

console.log('Published scenarios, yearly/monthly consistency, cent rounding and invalid inputs verified.');
