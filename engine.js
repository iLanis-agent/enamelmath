/* Enamel math - exact arithmetic, labeled norms.
   Labeled norms shown in the UI: sifted enamel ~1.2 g per 100 cm2 per coat;
   copper density 8.96 g/cm3 (a physical constant, not a norm); kiln cycle 30 min. */
(function (root) {
  'use strict';

  var POWDER_PER_100CM2 = 1.2; // g, labeled sifting norm
  var COPPER_DENSITY = 8.96;   // g/cm3, physical constant

  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }

  function powderGrams(w, h, coats, sides) {
    w = num(w, 'piece width'); h = num(h, 'piece height');
    if (w <= 0 || h <= 0) throw new Error('piece dimensions must be positive');
    if (!Number.isInteger(coats) || coats < 1 || coats > 6) throw new Error('coats run 1 to 6 (labeled)');
    if (!Number.isInteger(sides) || sides < 1 || sides > 2) throw new Error('sides are 1 or 2 (counter-enamel counts)');
    var grams = Math.round(w * h / 100 * coats * sides * POWDER_PER_100CM2 * 10) / 10;
    var verdict = grams < 5 ? 'a thimble' : grams < 30 ? 'a small vial' : grams < 100 ? 'a jar' : 'stock up';
    return { grams: grams, verdict: verdict };
  }

  function copperGrams(diameter, thicknessMm) {
    diameter = num(diameter, 'disc diameter'); thicknessMm = num(thicknessMm, 'thickness');
    if (diameter <= 0 || thicknessMm <= 0) throw new Error('disc dimensions must be positive');
    var grams = Math.round(Math.PI * (diameter / 2) * (diameter / 2) * (thicknessMm / 10) * COPPER_DENSITY * 10) / 10;
    var verdict = grams < 15 ? 'feather' : grams < 60 ? 'workable' : 'hefty';
    return { grams: grams, verdict: verdict };
  }

  function kilnBatch(shelfW, shelfD, pieceW, pieceD, pieces, cycleMin) {
    shelfW = num(shelfW, 'shelf width'); shelfD = num(shelfD, 'shelf depth');
    pieceW = num(pieceW, 'piece width'); pieceD = num(pieceD, 'piece depth');
    if (shelfW <= 0 || shelfD <= 0) throw new Error('shelf dimensions must be positive');
    if (pieceW <= 0 || pieceD <= 0) throw new Error('piece dimensions must be positive');
    if (!Number.isInteger(pieces) || pieces < 1) throw new Error('need at least 1 whole piece');
    cycleMin = num(cycleMin, 'cycle minutes');
    if (cycleMin <= 0) throw new Error('cycle minutes must be positive');
    var a = Math.floor(shelfW / pieceW) * Math.floor(shelfD / pieceD);
    var b = Math.floor(shelfW / pieceD) * Math.floor(shelfD / pieceW);
    var perBatch = Math.max(a, b);
    if (perBatch === 0) throw new Error('the piece is bigger than the shelf (labeled)');
    var batches = Math.ceil(pieces / perBatch);
    var minutes = batches * cycleMin;
    var verdict = batches === 1 ? 'one firing' : batches <= 3 ? 'a morning' : 'a full day';
    return { per_batch: perBatch, batches: batches, minutes: minutes, verdict: verdict };
  }

  var api = { powderGrams: powderGrams, copperGrams: copperGrams, kilnBatch: kilnBatch,
              NORMS: { POWDER_PER_100CM2: POWDER_PER_100CM2, COPPER_DENSITY: COPPER_DENSITY } };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.EnamelMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
