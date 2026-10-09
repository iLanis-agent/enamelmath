#!/usr/bin/env python3
# Oracle for enamelmath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

POWDER = 1.2
COPPER = 8.96

def powderGrams(w, h, coats, sides):
    grams = math.floor(w * h / 100 * coats * sides * POWDER * 10 + 0.5) / 10
    verdict = 'a thimble' if grams < 5 else 'a small vial' if grams < 30 else 'a jar' if grams < 100 else 'stock up'
    return {'grams': grams, 'verdict': verdict}

def copperGrams(diameter, thicknessMm):
    grams = math.floor(math.pi * (diameter / 2) * (diameter / 2) * (thicknessMm / 10) * COPPER * 10 + 0.5) / 10
    verdict = 'feather' if grams < 15 else 'workable' if grams < 60 else 'hefty'
    return {'grams': grams, 'verdict': verdict}

def kilnBatch(shelfW, shelfD, pieceW, pieceD, pieces, cycleMin):
    a = math.floor(shelfW / pieceW) * math.floor(shelfD / pieceD)
    b = math.floor(shelfW / pieceD) * math.floor(shelfD / pieceW)
    perBatch = max(a, b)
    batches = math.ceil(pieces / perBatch)
    minutes = batches * cycleMin
    verdict = 'one firing' if batches == 1 else 'a morning' if batches <= 3 else 'a full day'
    return {'per_batch': perBatch, 'batches': batches, 'minutes': minutes, 'verdict': verdict}

CASES = [
  {'card':'powderGrams','args':[5,7,2,2]},  {'card':'powderGrams','args':[10,10,2,2]},
  {'card':'powderGrams','args':[10,10,3,2]},{'card':'powderGrams','args':[20,20,2,2]},
  {'card':'powderGrams','args':[20,20,3,2]},{'card':'powderGrams','args':[30,20,2,2]},
  {'card':'powderGrams','args':[30,30,3,2]},{'card':'powderGrams','args':[40,40,2,2]},
  {'card':'powderGrams','args':[50,50,3,2]},{'card':'powderGrams','args':[15,15,1,1]},
  {'card':'powderGrams','args':[25,35,2,2]},{'card':'powderGrams','args':[5,7,6,2]},
  {'card':'powderGrams','args':[0,7,2,2],'error':'positive'},
  {'card':'powderGrams','args':[5,7,0,2],'error':'coats'},
  {'card':'powderGrams','args':[5,7,7,2],'error':'coats'},
  {'card':'powderGrams','args':[5,7,2,3],'error':'sides'},
  {'card':'copperGrams','args':[5,0.9]},  {'card':'copperGrams','args':[3,0.5]},
  {'card':'copperGrams','args':[2,0.5]},  {'card':'copperGrams','args':[10,1.2]},
  {'card':'copperGrams','args':[8,0.9]},  {'card':'copperGrams','args':[6,1.6]},
  {'card':'copperGrams','args':[12,2.0]}, {'card':'copperGrams','args':[4,0.3]},
  {'card':'copperGrams','args':[7,1.0]},  {'card':'copperGrams','args':[15,0.8]},
  {'card':'copperGrams','args':[2.5,0.9]},{'card':'copperGrams','args':[9,2.5]},
  {'card':'copperGrams','args':[0,0.9],'error':'positive'},
  {'card':'copperGrams','args':[5,0],'error':'positive'},
  {'card':'copperGrams','args':[-2,0.9],'error':'positive'},
  {'card':'copperGrams','args':[5,-0.9],'error':'positive'},
  {'card':'kilnBatch','args':[30,30,5,7,20,30]},  {'card':'kilnBatch','args':[30,30,5,7,50,30]},
  {'card':'kilnBatch','args':[30,30,5,7,100,30]}, {'card':'kilnBatch','args':[40,30,8,10,12,25]},
  {'card':'kilnBatch','args':[40,30,8,10,30,25]}, {'card':'kilnBatch','args':[20,20,6,6,10,30]},
  {'card':'kilnBatch','args':[20,20,6,6,9,30]},   {'card':'kilnBatch','args':[20,20,6,6,28,30]},
  {'card':'kilnBatch','args':[25,35,5,7,20,30]},  {'card':'kilnBatch','args':[15,15,5,5,18,40]},
  {'card':'kilnBatch','args':[30,30,40,40,1,30],'error':'bigger than the shelf'},
  {'card':'kilnBatch','args':[30,30,35,10,2,30],'error':'bigger than the shelf'},
  {'card':'kilnBatch','args':[0,30,5,7,20,30],'error':'positive'},
  {'card':'kilnBatch','args':[30,30,5,7,0,30],'error':'at least 1'},
  {'card':'kilnBatch','args':[30,30,5,7,20,0],'error':'positive'},
  {'card':'kilnBatch','args':[30,30,5,7,2.5,30],'error':'whole'},
]

out = []
for c in CASES:
    row = {'card': c['card'], 'args': c['args']}
    if 'error' in c:
        row['error'] = c['error']
    else:
        row['expect'] = globals()[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as f:
    json.dump(out, f, indent=1)
    f.write('\n')
print('wrote', len(out), 'cases')
