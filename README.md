# Enamel math

Three vitreous-enamel calculators as a small static site - exact arithmetic, every
borrowed number labeled:

- **Powder estimate** - piece width x height, coats per side and sides enameled ->
  grams of powder at a labeled sifting norm (1.2 g per 100 cm2 per coat), with jar
  bands. Counter-enamel counts as a second side.
- **Copper blank weight** - disc diameter and thickness -> grams at 8.96 g/cm3
  (a physical constant), with weight bands.
- **Kiln batch planner** - shelf width x depth, piece footprint, pieces to fire and
  minutes per cycle -> pieces per batch (best orientation), batches and wall-clock
  kiln time, with a day band.

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 48 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```
