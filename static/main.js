// ── bread buddy · main.js ─────────────────────────────────────────────────
//
// Storage format: localStorage key = "bb_recipe_<name>", value = JSON string
// of the recipe dict (matching Recipe.to_dict() output).
//
// Hydration slider display (called from index.html inline script)
// ─────────────────────────────────────────────────────────────────────────

const STORAGE_PREFIX = 'bb_recipe_';

// ── Contextual info tooltips ───────────────────────────────────────────────

const TIPS = {
  'bakers-pct': {
    title: "Baker's percentage",
    body: "Flour is always 100%. Every other ingredient is expressed as a percentage of that flour weight. So 70% hydration with 500g flour means 350g water. The beauty of it: double the flour, double everything else. Scale any recipe in seconds without doing the maths. Professional bakers have used this system for centuries, which suggests it works.",
  },
  'hydration': {
    title: 'Hydration',
    body: "Water as a percentage of flour weight. More water means a more open, hole-y crumb. It also means a wetter, stickier dough that tests your patience and your bench skills in equal measure. Most home bakers start at 68-72% and nudge upward as their confidence grows. There is absolutely no shame in 70%. Some of the best bread in the world is 70%.",
  },
  'starter-pct': {
    title: 'Starter percentage',
    body: "How much active starter you use, relative to flour. Use less (5-8%) and you get a slower rise, more complex sour flavour, and a forgiving timing window. Use more (15-20%) and the loaf rises faster but tastes milder. The bake timeline adjusts automatically either way, so there is no wrong answer here, only different bread.",
  },
  'friction-factor': {
    title: 'Friction factor',
    body: "Mechanical mixing generates heat. Kneading by hand adds almost none, so enter 0. A stand mixer on medium adds roughly 15-25 degrees of warmth to your dough over a typical mix. This number tells the DDT formula how much extra heat your method contributes, so it can ask for correspondingly cooler water to compensate.",
  },
  'autolyse': {
    title: 'Autolyse',
    body: "Mix flour and water first, then rest them before adding starter and salt. During that quiet window, amylase builds sugar reserves and protease softens the gluten network. The result is a noticeably silkier, more extensible dough that holds together under shaping without fighting you. Twenty to sixty minutes is typical. Skip it if you are pressed for time and nobody will know.",
  },
  'cold-proof': {
    title: 'Cold proof (retard)',
    body: "Park your shaped dough in the fridge overnight at 4-8°C. The cold slows yeast to almost nothing but keeps the bacteria gently working, favouring acetic acid (sharp, tangy) over lactic (mild, creamy). You get more flavour complexity, a better ear on the score, and a firm dough that holds its shape beautifully. Bake straight from cold. Do not let it warm up first. That is a very common and entirely avoidable mistake.",
  },
  'feeding-ratio': {
    title: 'Feeding ratio',
    body: "A 1:5:5 ratio means for every 1g of old starter, you add 5g flour and 5g water. Higher ratios (1:10:10) dilute more and give a milder starter that peaks later, useful when you need scheduling flexibility. Lower ratios (1:2:2) peak faster and produce a more assertively sour starter. Neither is better. It depends entirely on when you want to bake and how much tang you enjoy.",
  },
  'ddt': {
    title: 'Desired Dough Temperature (DDT)',
    body: "Yeast and bacteria perform best at 24-26°C. Even 2-3°C off that target will noticeably speed up or slow down your bulk fermentation. The DDT formula accounts for every input temperature (room, flour, levain, water) plus the heat your mixing method adds, and tells you precisely how warm your water should be to land at your target. It sounds fiddly. It genuinely is not, once you have done it once.",
  },
  'hydration-effective': {
    title: 'Set vs. actual hydration',
    body: "Your starter contains water. A 100% hydration starter at 10% baker's percentage adds roughly 5% extra water to the dough on top of what the slider shows. 'Set' is the hydration you dialled in; 'actual' is the true water-to-flour ratio once the starter's water content is counted in. Both numbers are useful: 'set' is what you reproduce next time, 'actual' tells you how the dough will really behave.",
  },
};

function showTip(triggerEl, key) {
  // Toggle: if this tip is already open, close it
  const existing = document.getElementById('info-popover-active');
  if (existing) {
    existing.remove();
    if (existing.dataset.key === key) return;
  }

  const tip = TIPS[key];
  if (!tip) return;

  const pop = document.createElement('div');
  pop.id = 'info-popover-active';
  pop.className = 'info-popover';
  pop.dataset.key = key;
  pop.innerHTML = `<h4>${tip.title}</h4><p>${tip.body}</p>`;
  document.body.appendChild(pop);

  // Position below the trigger, clamped to viewport
  // position:fixed uses viewport coords — getBoundingClientRect() is already viewport-relative,
  // so do NOT add window.scrollX/Y here.
  const rect = triggerEl.getBoundingClientRect();
  const popW = 300;
  let left = rect.left;
  if (left + popW > window.innerWidth - 16) left = window.innerWidth - popW - 16;
  left = Math.max(16, left);
  pop.style.top  = (rect.bottom + 8) + 'px';
  pop.style.left = left + 'px';

  // Close on any outside click
  setTimeout(() => {
    document.addEventListener('click', function outsideClose(e) {
      if (!pop.contains(e.target) && e.target !== triggerEl) {
        pop.remove();
        document.removeEventListener('click', outsideClose);
      }
    });
  }, 0);
}

const HYDRATION_LABELS = [
  { max: 65, label: 'Stiff',             desc: 'Dense and chewy. Very easy to shape. Great for bagels, not so great for Instagram.' },
  { max: 72, label: 'Classic',           desc: 'The sweet spot. Forgiving, flavourful, excellent for anyone who wants to actually enjoy baking.' },
  { max: 78, label: 'Open crumb',        desc: 'Lovely irregular holes. Needs more stretch and folds and reasonably confident hands.' },
  { max: 85, label: 'Ambitious',         desc: 'Very wet and sticky. Strong flour, strong gluten, and a high tolerance for mess required.' },
  { max: 90, label: 'Brave',             desc: 'Genuine respect. This will test every skill you have. Make sure your gluten is bulletproof.' },
  { max: 999,label: 'Wetsuit required',  desc: 'Put your wetsuit on. At this level you are not shaping dough, you are negotiating with it. Respect.' },
];

function updateHydrationDisplay(value) {
  const pct = parseInt(value, 10);
  const valEl  = document.getElementById('hydration-value');
  const lblEl  = document.getElementById('hydration-label');
  const gramsEl = document.getElementById('hydration-grams');
  if (valEl) valEl.textContent = `${pct}%`;
  if (gramsEl) {
    const flourW = parseFloat(document.getElementById('flour-weight')?.value) || 500;
    gramsEl.textContent = `= ${Math.round(flourW * pct / 100)}g water`;
  }
  if (!lblEl) return;
  const match = HYDRATION_LABELS.find(h => pct <= h.max);
  lblEl.textContent = match ? `${match.label}: ${match.desc}` : '';
}

// ── Recipe templates ────────────────────────────────────────────────────────

const RECIPE_TEMPLATES = {
  country: {
    name: 'Classic Country Loaf',
    flour: 500, hydration: 72, starter: 10, salt: 2,
    breadType: 'freestanding',
  },
  highHydration: {
    name: 'High-Hydration Batard',
    flour: 500, hydration: 80, starter: 10, salt: 2,
    breadType: 'freestanding',
  },
  rye: {
    name: 'Rye Sandwich Loaf',
    flour: 500, hydration: 75, starter: 15, salt: 2,
    breadType: 'loaf_pan',
  },
  flatbread: {
    name: 'Quick Flatbread',
    flour: 400, hydration: 80, starter: 20, salt: 1.8,
    breadType: 'flatbread',
  },
};

function loadTemplate(key) {
  const tpl = RECIPE_TEMPLATES[key];
  if (!tpl) return;

  // Fill flour weight
  const flourEl = document.getElementById('flour-weight');
  if (flourEl) { flourEl.value = tpl.flour; updateGramFields(); }

  // Fill hydration
  const hydEl = document.getElementById('hydration');
  if (hydEl) { hydEl.value = tpl.hydration; updateHydrationDisplay(tpl.hydration); }

  // Fill starter (visible field + hidden)
  const starterVisible = document.getElementById('starter-pct-visible');
  const starterHidden  = document.getElementById('starter-pct');
  if (starterVisible) starterVisible.value = tpl.starter;
  if (starterHidden)  starterHidden.value  = tpl.starter;

  // Fill salt (visible field + hidden)
  const saltVisible = document.getElementById('salt-pct-visible');
  const saltHidden  = document.getElementById('salt-pct');
  if (saltVisible) saltVisible.value = tpl.salt;
  if (saltHidden)  saltHidden.value  = tpl.salt;

  // Pre-fill recipe name
  const nameInput = document.getElementById('recipe-name-input');
  if (nameInput) nameInput.value = tpl.name;

  // Switch bread type
  applyBreadType(tpl.breadType, tpl.hydration, tpl.starter);

  // Set the radio button for bread type
  const radio = document.querySelector(`input[name="bread_type_radio"][value="${tpl.breadType}"]`);
  if (radio) radio.checked = true;

  // Update hidden bread type field and trigger HTMX
  const breadTypeInput = document.getElementById('bread-type-input');
  if (breadTypeInput) breadTypeInput.value = tpl.breadType;

  const form = document.getElementById('recipe-form');
  if (form && window.htmx) htmx.trigger(form, 'change');
}

// ── Bread type / mode helper ───────────────────────────────────────────────

// In starter-only mode hide the recipe form + downstream sections, but keep
// the bread-type-bar (at top of section-recipe card) always visible.
const STARTER_ONLY_SECTIONS = ['recipe-form-wrap', 'section-params', 'section-timeline'];
const STARTER_ONLY_STEPS    = ['section-params', 'section-timeline'];

function applyBreadType(type, hydration, starterPct) {
  const hydEl    = document.getElementById('hydration');
  const starterEl = document.getElementById('starter-pct');
  const hiddenEl  = document.getElementById('bread-type-input');

  if (hiddenEl) hiddenEl.value = type;

  const isStarterOnly = type === 'starter_only';
  const isFlatbread   = type === 'flatbread';

  // Starter-only mode: hide bread sections, dim progress steps
  STARTER_ONLY_SECTIONS.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = isStarterOnly ? 'none' : '';
  });
  document.querySelectorAll('.progress-step').forEach(s => {
    const id = s.dataset.section;
    s.classList.toggle('dimmed', isStarterOnly && STARTER_ONLY_STEPS.includes(id));
  });

  if (!isStarterOnly) {
    if (hydEl) { hydEl.value = hydration; updateHydrationDisplay(hydration); }
    if (starterEl) starterEl.value = starterPct;
  }

  // Flatbread: hide proofing + autolyse fields, show explanatory note
  const proofingField          = document.getElementById('proofing-field');
  const proofingAutolyseFields = document.getElementById('proofing-autolyse-fields');
  const flatbreadNote          = document.getElementById('flatbread-note');
  if (proofingField)          proofingField.style.display          = isFlatbread ? 'none' : '';
  if (proofingAutolyseFields) proofingAutolyseFields.style.display = isFlatbread ? 'none' : '';
  if (flatbreadNote)          flatbreadNote.style.display          = isFlatbread ? 'block' : 'none';

  // Update the inline bread-type descriptor note
  const noteEl = document.getElementById('bread-type-note');
  if (noteEl) {
    const notes = {
      flatbread:    'Same-day bake · skillet or griddle · 80% hydration',
      loaf_pan:     'Pan-baked · easier shaping · 75% hydration',
      freestanding: 'Dutch oven · free-form · 70% hydration',
      starter_only: 'Feeding calculator only. No bread recipe.',
    };
    noteEl.textContent = notes[type] || '';
  }

  // Fire HTMX on the recipe form so sidebar updates immediately
  const form = document.getElementById('recipe-form');
  if (!isStarterOnly && form && window.htmx) htmx.trigger(form, 'change');
}

// ── Progress stepper ───────────────────────────────────────────────────────

function initProgressNav() {
  const steps    = document.querySelectorAll('.progress-step');
  const sections = [...steps].map(s => document.getElementById(s.dataset.section));

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        steps.forEach(s => s.classList.remove('active'));
        const active = document.querySelector(`.progress-step[data-section="${e.target.id}"]`);
        if (active && !active.classList.contains('dimmed')) active.classList.add('active');
      }
    });
  }, { rootMargin: '-15% 0px -70% 0px' });

  sections.forEach(s => s && obs.observe(s));
}

// ── Flour blend ────────────────────────────────────────────────────────────

const FLOUR_TYPES = ['Bread flour', 'Whole wheat', 'Rye', 'Spelt', 'Einkorn', 'Other'];

const FLOUR_HINTS = {
  'Whole wheat': 'Thirstier than white flour. Adds a nutty depth and speeds up fermentation noticeably.',
  'Rye':         'Speeds fermentation significantly. Earthy, dense, and its enzymes are extremely active. Watch your bulk carefully.',
  'Spelt':       'Lovely flavour, but fragile gluten. Handle gently, keep autolyse short, and do not overwork it.',
  'Einkorn':     'Ancient grain with genuinely weak gluten. Expect a denser crumb, faster fermentation, and a nutty sweetness worth the extra care.',
  'Bread flour': '',
  'Other':       '',
};

function updateFlourTypeHint(selectEl, hintEl) {
  const hint = FLOUR_HINTS[selectEl.value] || '';
  hintEl.textContent = hint;
  hintEl.style.display = hint ? '' : 'none';
}

function addFlourRow(name = '', weight = '') {
  const container = document.getElementById('flour-rows');
  if (!container) return;
  const idx = container.querySelectorAll('.flour-row').length;

  const wrapper = document.createElement('div');
  wrapper.className = 'flour-row-wrap';

  const row = document.createElement('div');
  row.className = 'flour-row';

  const sel = document.createElement('select');
  sel.name = `flour_${idx}_name`;
  FLOUR_TYPES.forEach(f => {
    const opt = document.createElement('option');
    opt.value = f;
    opt.textContent = f;
    if (f === name) opt.selected = true;
    sel.appendChild(opt);
  });

  const inp = document.createElement('input');
  inp.type = 'number';
  inp.name = `flour_${idx}_weight`;
  inp.value = weight;
  inp.min = '0';
  inp.step = '10';
  inp.placeholder = 'g';
  inp.className = 'flour-weight-input';
  inp.addEventListener('input', syncFlourTotal);

  const rmBtn = document.createElement('button');
  rmBtn.type = 'button';
  rmBtn.className = 'flour-row-remove';
  rmBtn.textContent = '×';
  rmBtn.title = 'Remove';
  rmBtn.addEventListener('click', () => { wrapper.remove(); syncFlourTotal(); });

  const hintEl = document.createElement('small');
  hintEl.className = 'flour-type-hint';
  hintEl.style.display = 'none';

  sel.addEventListener('change', () => {
    updateFlourTypeHint(sel, hintEl);
    syncFlourTotal();
  });
  updateFlourTypeHint(sel, hintEl);

  row.appendChild(sel);
  row.appendChild(inp);
  row.appendChild(rmBtn);
  wrapper.appendChild(row);
  wrapper.appendChild(hintEl);
  container.appendChild(wrapper);
}

function syncFlourTotal() {
  const inputs  = document.querySelectorAll('.flour-weight-input');
  const total   = [...inputs].reduce((sum, i) => sum + (parseFloat(i.value) || 0), 0);
  const mainInp = document.getElementById('flour-weight');
  const label   = document.getElementById('flour-blend-total');

  if (inputs.length > 0 && total > 0) {
    if (mainInp) mainInp.value = Math.round(total);
    if (label)   label.textContent = `Total: ${Math.round(total)}g`;
  } else {
    if (label) label.textContent = '';
  }
  // Re-trigger HTMX so sidebar updates
  const form = document.getElementById('recipe-form');
  if (form && window.htmx) htmx.trigger(form, 'change');
  updateGramFields();
  const hyd = document.getElementById('hydration');
  if (hyd) updateHydrationDisplay(hyd.value);
}

// ── Other ingredients ──────────────────────────────────────────────────────

// weightGrams: stored weight in grams (for restoring saved state)
function addOtherRow(name = '', weightGrams = '') {
  const container = document.getElementById('other-rows');
  if (!container) return;
  const idx = container.querySelectorAll('.other-ing-row').length;

  const row = document.createElement('div');
  row.className = 'other-ing-row';

  const nameInp = document.createElement('input');
  nameInp.type = 'text';
  nameInp.name = `other_${idx}_name`;
  nameInp.value = name;
  nameInp.placeholder = 'e.g. Honey';
  nameInp.className = 'other-name-input';
  nameInp.addEventListener('input', () => {
    const form = nameInp.closest('form');
    if (form && window.htmx) htmx.trigger(form, 'change');
  });

  // Visible display input (no name — not submitted)
  const visibleInp = document.createElement('input');
  visibleInp.type = 'number';
  visibleInp.value = weightGrams;
  visibleInp.min = '0';
  visibleInp.step = '1';
  visibleInp.placeholder = 'g';
  visibleInp.className = 'other-weight-input';

  // Hidden input (always grams — submitted)
  const hiddenInp = document.createElement('input');
  hiddenInp.type = 'hidden';
  hiddenInp.name = `other_${idx}_weight`;
  hiddenInp.value = weightGrams;

  const toggleBtn = document.createElement('button');
  toggleBtn.type = 'button';
  toggleBtn.className = 'unit unit-toggle other-unit-toggle';
  toggleBtn.textContent = 'g';
  toggleBtn.title = 'Tap to switch between g and %';

  visibleInp.addEventListener('input', () => syncOtherFromVisible(visibleInp, hiddenInp, toggleBtn));
  toggleBtn.addEventListener('click', () => toggleOtherPctGrams(toggleBtn, visibleInp, hiddenInp));

  const rmBtn = document.createElement('button');
  rmBtn.type = 'button';
  rmBtn.className = 'flour-row-remove';
  rmBtn.textContent = '×';
  rmBtn.title = 'Remove';
  rmBtn.addEventListener('click', () => {
    row.remove();
    const form = document.getElementById('recipe-form');
    if (form && window.htmx) htmx.trigger(form, 'change');
  });

  row.appendChild(nameInp);
  row.appendChild(visibleInp);
  row.appendChild(toggleBtn);
  row.appendChild(hiddenInp);
  row.appendChild(rmBtn);
  container.appendChild(row);
}

/** Sync hidden (grams) from what the user typed in the visible input. */
function syncOtherFromVisible(visible, hidden, btn) {
  const flourW = parseFloat(document.getElementById('flour-weight')?.value) || 500;
  const isPct  = btn.textContent.trim() === '%';
  const val    = parseFloat(visible.value) || 0;
  hidden.value = isPct ? Math.round(val * flourW / 100 * 10) / 10 : val;
  const form = visible.closest('form');
  if (form && window.htmx) htmx.trigger(form, 'change');
}

/** Toggle the visible unit between g and % for an other-ingredient row. */
function toggleOtherPctGrams(btn, visible, hidden) {
  const flourW     = parseFloat(document.getElementById('flour-weight')?.value) || 500;
  const currentlyG = btn.textContent.trim() === 'g';
  const grams      = parseFloat(hidden.value) || 0;

  if (currentlyG) {
    // Switch to %
    visible.value = flourW > 0 ? Math.round(grams / flourW * 100 * 10) / 10 : 0;
    visible.step  = '0.1';
    btn.textContent = '%';
    btn.title = 'Switch to grams';
  } else {
    // Switch to grams
    visible.value = Math.round(grams * 10) / 10;
    visible.step  = '1';
    btn.textContent = 'g';
    btn.title = 'Switch to %';
  }
}

// ── Scroll sidebar hydration click back to the slider ─────────────────────

function scrollToHydration() {
  const el = document.getElementById('hydration');
  if (!el) return;
  el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  el.focus();
}

// ── Starter presets ────────────────────────────────────────────────────────

function applyStarterPreset(flourRatio, waterRatio, starterRatio) {
  const f = document.querySelector('[name="ratio_flour"]');
  const w = document.querySelector('[name="ratio_water"]');
  const s = document.querySelector('[name="ratio_starter"]');
  if (f) f.value = flourRatio;
  if (w) w.value = waterRatio;
  if (s) s.value = starterRatio;
  // Trigger HTMX recalculation
  const form = f && f.closest('form');
  if (form && window.htmx) htmx.trigger(form, 'change');
}

// ── g / % toggle for starter and salt ─────────────────────────────────────

function togglePctGrams(btn, visibleInputId, hiddenInputId) {
  const visible = document.getElementById(visibleInputId);
  const hidden  = document.getElementById(hiddenInputId);
  const flourW  = parseFloat(document.getElementById('flour-weight').value) || 500;
  const currentlyPct = btn.textContent.trim() === '%';

  if (currentlyPct) {
    // Switch to grams
    const pct = parseFloat(visible.value) || 0;
    visible.value = Math.round(pct * flourW / 100 * 10) / 10;
    visible.step = '1';
    visible.min  = '0';
    btn.textContent = 'g';
    btn.title = 'Switch to %';
  } else {
    // Switch to percent
    const grams = parseFloat(visible.value) || 0;
    visible.value = flourW > 0 ? Math.round(grams / flourW * 100 * 10) / 10 : 0;
    visible.step = '0.1';
    visible.min  = '0';
    btn.textContent = '%';
    btn.title = 'Switch to grams';
  }
  // Sync hidden % field and trigger HTMX
  syncPctFromVisible(visible, hidden, btn);
}

function syncPctFromVisible(visible, hidden, btn) {
  const flourW = parseFloat(document.getElementById('flour-weight').value) || 500;
  const isGrams = btn.textContent.trim() === 'g';
  const val = parseFloat(visible.value) || 0;
  hidden.value = isGrams ? (flourW > 0 ? Math.round(val / flourW * 100 * 10) / 10 : 0) : val;
  const form = visible.closest('form');
  if (form && window.htmx) htmx.trigger(form, 'change');
}

// When flour weight changes, update any fields currently showing grams
function updateGramFields() {
  document.querySelectorAll('.unit-toggle').forEach(btn => {
    if (btn.textContent.trim() !== 'g') return;
    const visibleId = btn.dataset.visibleInput;
    const hiddenId  = btn.dataset.hiddenInput;
    if (!visibleId || !hiddenId) return;
    const visible = document.getElementById(visibleId);
    const hidden  = document.getElementById(hiddenId);
    const flourW  = parseFloat(document.getElementById('flour-weight').value) || 500;
    const pct = parseFloat(hidden.value) || 0;
    visible.value = Math.round(pct * flourW / 100 * 10) / 10;
  });
  // Refresh hydration gram display when flour weight changes
  const hyd = document.getElementById('hydration');
  if (hyd) updateHydrationDisplay(hyd.value);
}

// ── Temperature unit toggle (°C / °F) ─────────────────────────────────────

let tempUnit = 'C';

const TEMP_FIELDS = [
  { id: 'target-dough-temp', defaultC: 25, minC: 15, maxC: 35 },
  { id: 'ambient-temp',      defaultC: 20, minC: 5,  maxC: 40 },
  { id: 'flour-temp',        defaultC: 20, minC: 5,  maxC: 35 },
  { id: 'levain-temp',       defaultC: 22, minC: 5,  maxC: 35 },
  { id: 'friction-factor',   defaultC: null }, // not a temperature, skip conversion
  { id: 'reference-temp',    defaultC: 21, minC: 10, maxC: 35 },
  { id: 'ambient-temp-ferm', defaultC: 20, minC: 5,  maxC: 40 },
];

function toF(c) { return Math.round((c * 9/5 + 32) * 2) / 2; }
function toC(f) { return Math.round((f - 32) * 5/9 * 2) / 2; }

function setTempUnit(unit) {
  if (unit === tempUnit) return;
  const toNew = unit === 'F' ? toF : toC;
  TEMP_FIELDS.forEach(({ id, minC, maxC }) => {
    if (minC == null) return; // friction-factor — skip
    const el = document.getElementById(id);
    if (!el) return;
    el.value = toNew(parseFloat(el.value) || 0);
    // minC/maxC are always in Celsius — only convert them when targeting °F
    el.min   = unit === 'F' ? toF(minC) : minC;
    el.max   = unit === 'F' ? toF(maxC) : maxC;
    el.step  = unit === 'F' ? '1' : '0.5';
  });
  // Update unit labels
  document.querySelectorAll('.temp-unit-label').forEach(el => {
    el.textContent = unit === 'F' ? '°F' : '°C';
  });
  // Update hidden fields (main form + fermentation form)
  const hiddenUnit = document.getElementById('temp-unit-hidden');
  if (hiddenUnit) hiddenUnit.value = unit;
  const fermUnit = document.getElementById('temp-unit-ferm');
  if (fermUnit) fermUnit.value = unit;
  // Update toggle pill appearance
  document.querySelectorAll('.temp-toggle-pill').forEach(pill => {
    pill.classList.toggle('active', pill.dataset.unit === unit);
  });
  tempUnit = unit;
  localStorage.setItem('bb_temp_unit', unit);
  // Re-trigger HTMX
  const form = document.getElementById('water-temp-form');
  if (form && window.htmx) htmx.trigger(form, 'change');
}

// ── Starter section: fill target amount from recipe sidebar ────────────────

function useRecipeStarterWeight() {
  const el = document.getElementById('recipe-starter-weight');
  if (!el) {
    // Sidebar hasn't been populated yet — nudge user
    alert('Fill in your recipe first (section ②) to calculate starter weight.');
    return;
  }
  const weight = el.dataset.weight;
  if (!weight || weight === '0') return;
  const input = document.getElementById('target-amount');
  if (input) {
    input.value = weight;
    // Trigger HTMX recalculation on the starter form
    const form = input.closest('form');
    if (form && window.htmx) htmx.trigger(form, 'change');
  }
}

// ── State persistence (localStorage, no server round-trip) ────────────────

/**
 * Read current form values into a plain state object.
 * Called after every sidebar HTMX swap and on explicit save.
 */
function readFormState() {
  const flourEl = document.getElementById('flour-weight');
  if (!flourEl) return null;   // not on the calculator page

  const state = {
    flour_weight: parseFloat(flourEl.value) || 500,
    hydration:    parseInt(document.getElementById('hydration')?.value, 10) || 70,
    starter_pct:  parseFloat(document.getElementById('starter-pct')?.value) || 10,
    salt_pct:     parseFloat(document.getElementById('salt-pct')?.value) || 2,
    bread_type:   document.getElementById('bread-type-input')?.value || 'freestanding',
    loaf_count:   parseInt(document.querySelector('[name="loaf_count"]:checked')?.value, 10) || 1,
    recipe_name:  document.getElementById('recipe-name-input')?.value.trim() || 'My Sourdough',
    notes:        document.getElementById('recipe-notes-input')?.value.trim() || '',
    starter_unit: document.querySelector('[data-visible-input="starter-pct-visible"]')?.textContent.trim() || '%',
    salt_unit:    document.querySelector('[data-visible-input="salt-pct-visible"]')?.textContent.trim() || '%',
  };

  // Capture any open flour blend rows
  const rows = document.querySelectorAll('.flour-row');
  if (rows.length > 0) {
    const blend = [];
    rows.forEach(row => {
      const sel = row.querySelector('select');
      const inp = row.querySelector('input[type="number"]');
      if (sel && inp && parseFloat(inp.value) > 0) {
        blend.push({ name: sel.value, weight: parseFloat(inp.value) });
      }
    });
    if (blend.length > 0) state.flour_blend = blend;
  }

  // Capture any open other ingredient rows (hidden field always stores grams)
  const otherRows = document.querySelectorAll('.other-ing-row');
  if (otherRows.length > 0) {
    const others = [];
    otherRows.forEach(row => {
      const nameEl   = row.querySelector('input[type="text"]');
      const weightEl = row.querySelector('input[type="hidden"]');
      if (nameEl && weightEl && nameEl.value.trim() && parseFloat(weightEl.value) > 0) {
        others.push({ name: nameEl.value.trim(), weight: parseFloat(weightEl.value) });
      }
    });
    if (others.length > 0) state.other_ingredients = others;
  }

  return state;
}

/** Persist current form state to localStorage. */
function saveLastState() {
  const state = readFormState();
  if (state) localStorage.setItem('bb_last_state', JSON.stringify(state));
}

/**
 * Normalise a stored value to the new form-state format.
 * Handles legacy Recipe-model dicts (from before Phase 1).
 */
function normaliseStoredState(data) {
  if (!data) return null;
  if (data.flour_weight !== undefined) return data;   // already new format

  // Legacy: Recipe model dict with 'ingredients' array
  const ings = data.ingredients || [];
  const flourIngs = ings.filter(i => i.category === 'flour');
  const flourW    = flourIngs.reduce((s, i) => s + i.weight, 0);
  const waterW    = ings.filter(i => i.category === 'water').reduce((s, i) => s + i.weight, 0);
  const starterW  = ings.filter(i => i.category === 'starter').reduce((s, i) => s + i.weight, 0);
  const saltW     = ings.filter(i => i.category === 'salt').reduce((s, i) => s + i.weight, 0);

  const hydration   = flourW > 0 ? Math.round(waterW  / flourW * 100) : 70;
  const starter_pct = flourW > 0 ? Math.round(starterW / flourW * 100 * 10) / 10 : 10;
  const salt_pct    = flourW > 0 ? Math.round(saltW    / flourW * 100 * 10) / 10 : 2;
  const flour_blend = flourIngs.length > 1 ? flourIngs.map(i => ({ name: i.name, weight: i.weight })) : undefined;

  return {
    flour_weight: Math.round(flourW) || 500,
    hydration,
    starter_pct,
    salt_pct,
    bread_type:  'freestanding',
    loaf_count:  1,
    flour_blend,
    recipe_name: data.name || 'My Sourdough',
    notes:       data.notes || '',
  };
}

/** Restore form fields from a stored state object and trigger HTMX recalc. */
function restoreFormState(raw) {
  const state = normaliseStoredState(raw);
  if (!state) return;

  // Unlock sections immediately — avoids flash of locked UI on returning users
  unlockSections();

  // Bread type first — it adjusts visibility of other sections
  const breadTypeInput = document.getElementById('bread-type-input');
  if (breadTypeInput && state.bread_type) {
    breadTypeInput.value = state.bread_type;
    const radio = document.querySelector(`[name="bread_type_radio"][value="${state.bread_type}"]`);
    if (radio) radio.checked = true;
    applyBreadType(state.bread_type, state.hydration, state.starter_pct);
  }

  // Flour (skip if blend will handle it)
  if (!state.flour_blend) {
    const flourEl = document.getElementById('flour-weight');
    if (flourEl) flourEl.value = state.flour_weight;
  }

  // Hydration
  const hydEl = document.getElementById('hydration');
  if (hydEl) { hydEl.value = state.hydration; updateHydrationDisplay(state.hydration); }

  // Starter %
  const starterVisible = document.getElementById('starter-pct-visible');
  const starterHidden  = document.getElementById('starter-pct');
  if (starterVisible) starterVisible.value = state.starter_pct;
  if (starterHidden)  starterHidden.value  = state.starter_pct;

  // Salt %
  const saltVisible = document.getElementById('salt-pct-visible');
  const saltHidden  = document.getElementById('salt-pct');
  if (saltVisible) saltVisible.value = state.salt_pct;
  if (saltHidden)  saltHidden.value  = state.salt_pct;

  // Loaf count
  if (state.loaf_count) {
    const loafRadio = document.querySelector(`[name="loaf_count"][value="${state.loaf_count}"]`);
    if (loafRadio) loafRadio.checked = true;
  }

  // Recipe name + notes
  const nameInput  = document.getElementById('recipe-name-input');
  const notesInput = document.getElementById('recipe-notes-input');
  if (nameInput  && state.recipe_name) nameInput.value  = state.recipe_name;
  if (notesInput && state.notes)       notesInput.value = state.notes;

  // Flour blend
  if (state.flour_blend && state.flour_blend.length > 0) {
    const blendPanel = document.getElementById('flour-blend-panel');
    if (blendPanel) blendPanel.open = true;
    state.flour_blend.forEach(f => addFlourRow(f.name, f.weight));
    syncFlourTotal();
    // Fall through to also restore other ingredients before triggering HTMX
  }

  // Other ingredients
  if (state.other_ingredients && state.other_ingredients.length > 0) {
    const otherPanel = document.getElementById('other-ing-panel');
    if (otherPanel) otherPanel.open = true;
    state.other_ingredients.forEach(o => addOtherRow(o.name, o.weight));
  }

  if (state.flour_blend && state.flour_blend.length > 0) {
    return; // syncFlourTotal already triggers HTMX
  }

  // Trigger HTMX to recalculate sidebar with restored values
  const form = document.getElementById('recipe-form');
  if (form && window.htmx) htmx.trigger(form, 'change');
}

// ── Save recipe ────────────────────────────────────────────────────────────

/** Called from the quick "Save recipe" button inside the sidebar partial. */
function quickSaveRecipe() {
  const nameInput = document.getElementById('recipe-name-input');
  const currentName = nameInput ? nameInput.value.trim() : '';
  if (currentName && currentName !== 'My Sourdough') {
    saveRecipe();
  } else {
    // Scroll to and focus the name input in the sidebar footer
    if (nameInput) {
      nameInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
      nameInput.focus();
      nameInput.select();
      showToast('Give your recipe a name, then click Save.');
    }
  }
}

function saveRecipe() {
  const nameInput = document.getElementById('recipe-name-input');
  const name = nameInput ? nameInput.value.trim() : '';
  if (!name) {
    if (nameInput) nameInput.focus();
    showToast('Enter a recipe name first.');
    return;
  }

  const state = readFormState();
  if (!state) { showToast('Fill in your recipe first.'); return; }

  state.recipe_name = name;
  localStorage.setItem(STORAGE_PREFIX + name, JSON.stringify(state));
  localStorage.setItem('bb_last_state', JSON.stringify(state));
  populateRecipePanel();
  showToast(`"${name}" saved.`);
}

// ── Load recipe ────────────────────────────────────────────────────────────

function loadRecipe(name) {
  if (!name) return;
  const raw = localStorage.getItem(STORAGE_PREFIX + name);
  if (!raw) return;

  try {
    const data = JSON.parse(raw);
    restoreFormState(data);
    showToast(`"${name}" loaded.`);
  } catch (err) {
    showToast('Load failed: ' + err.message);
  }
}

// ── Delete a saved recipe ──────────────────────────────────────────────────

function deleteRecipe(name, event) {
  event.stopPropagation();
  if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
  localStorage.removeItem(STORAGE_PREFIX + name);
  populateRecipePanel();
}

// ── Recipe panel (custom dropdown) ────────────────────────────────────────

function toggleRecipePanel() {
  const panel = document.getElementById('recipe-panel');
  const toggle = document.getElementById('recipe-panel-toggle');
  if (!panel) return;
  const isOpen = !panel.hidden;
  panel.hidden = isOpen;
  toggle.setAttribute('aria-expanded', String(!isOpen));
}

function populateRecipePanel() {
  // Legacy: also called populateLoadDropdown — keep alias
  const list = document.getElementById('recipe-panel-list');
  if (!list) return;

  const keys = Object.keys(localStorage)
    .filter(k => k.startsWith(STORAGE_PREFIX))
    .sort();

  list.innerHTML = '';

  if (keys.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'recipe-panel-empty';
    empty.innerHTML = 'No saved recipes yet.<br><small>Name your recipe in the sidebar and click <strong>Save this recipe</strong>.</small>';
    list.appendChild(empty);
    return;
  }

  keys.forEach(key => {
    const name = key.slice(STORAGE_PREFIX.length);
    let meta = '';
    try {
      const data = JSON.parse(localStorage.getItem(key));
      if (data && data.flour_weight !== undefined) {
        // New form-state format
        meta = `${data.flour_weight}g · ${data.hydration || '?'}% hydration`;
      } else if (data && data.ingredients) {
        // Legacy Recipe model format
        const flourW = data.ingredients
          .filter(i => i.category === 'flour')
          .reduce((s, i) => s + i.weight, 0);
        const waterW = data.ingredients
          .filter(i => i.category === 'water' || i.category === 'starter')
          .reduce((s, i) => s + i.weight, 0);
        const totalW = data.ingredients.reduce((s, i) => s + i.weight, 0);
        if (flourW > 0) {
          const hyd = Math.round((waterW / flourW) * 100);
          meta = `${Math.round(totalW)}g · ${hyd}% hydration`;
        }
      }
    } catch (_) {}

    const row = document.createElement('div');
    row.className = 'recipe-panel-row';
    row.onclick = () => { loadRecipe(name); toggleRecipePanel(); };

    const nameEl = document.createElement('span');
    nameEl.className = 'recipe-panel-name';
    nameEl.textContent = name;

    const metaEl = document.createElement('span');
    metaEl.className = 'recipe-panel-meta';
    metaEl.textContent = meta;

    // Show truncated notes if present
    let notesEl = null;
    try {
      const storedData = JSON.parse(localStorage.getItem(key));
      if (storedData && storedData.notes) {
        notesEl = document.createElement('span');
        notesEl.className = 'recipe-panel-notes';
        notesEl.textContent = storedData.notes.length > 60
          ? storedData.notes.slice(0, 60) + '…'
          : storedData.notes;
      }
    } catch (_) {}

    const del = document.createElement('button');
    del.className = 'recipe-panel-delete';
    del.title = 'Delete';
    del.textContent = '✕';
    del.onclick = (e) => deleteRecipe(name, e);

    const infoCol = document.createElement('div');
    infoCol.className = 'recipe-panel-info';
    infoCol.appendChild(nameEl);
    infoCol.appendChild(metaEl);
    if (notesEl) infoCol.appendChild(notesEl);

    row.appendChild(infoCol);
    row.appendChild(del);
    list.appendChild(row);
  });
}

// Alias for legacy DOMContentLoaded call
function populateLoadDropdown() { populateRecipePanel(); }

// Close recipe panel when clicking outside
document.addEventListener('click', e => {
  const wrap = document.getElementById('recipe-panel-wrap');
  const panel = document.getElementById('recipe-panel');
  if (wrap && panel && !wrap.contains(e.target) && !panel.hidden) {
    panel.hidden = true;
    const toggle = document.getElementById('recipe-panel-toggle');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }
});

// ── Bake log ───────────────────────────────────────────────────────────────

const BAKE_LOG_PREFIX = 'bb_bake_';

function saveBakeLog() {
  // Quick-log UI: read from pill/button selection
  const outcomeBtn = document.querySelector('.bake-quick-btn--selected');
  const crumbBtn   = document.querySelector('.crumb-pill--selected');
  const outcome = outcomeBtn?.dataset.outcome || 'ok';
  const crumb   = crumbBtn?.dataset.crumb || 'standard';
  const notes   = document.getElementById('bl-notes')?.value.trim() || '';

  // Snapshot recipe from last saved state
  const lastState = (() => {
    try { return JSON.parse(localStorage.getItem('bb_last_state') || '{}'); } catch { return {}; }
  })();

  const entry = {
    date:    new Date().toISOString(),
    outcome,
    crumb,
    notes,
    recipe: {
      flour:     lastState.flour_weight || document.getElementById('flour-weight')?.value || '',
      hydration: lastState.hydration    || document.getElementById('hydration')?.value    || '',
      starter:   lastState.starter_pct  || document.getElementById('starter-pct')?.value  || '',
      salt:      lastState.salt_pct     || document.getElementById('salt-pct')?.value     || '',
      type:      lastState.bread_type   || document.getElementById('bread-type-input')?.value || '',
    },
  };

  const key = BAKE_LOG_PREFIX + entry.date;
  localStorage.setItem(key, JSON.stringify(entry));
  showToast('Bake saved. View it in the Bake Log.');

  const notesEl = document.getElementById('bl-notes');
  if (notesEl) notesEl.value = '';
}

function renderBakeLog() {
  const list = document.getElementById('bake-log-list');
  const empty = document.getElementById('bake-log-empty');
  if (!list) return;

  const entries = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (!key.startsWith(BAKE_LOG_PREFIX)) continue;
    try {
      entries.push({ key, data: JSON.parse(localStorage.getItem(key)) });
    } catch (e) { /* skip malformed */ }
  }

  if (entries.length === 0) {
    if (empty) empty.style.display = '';
    return;
  }

  if (empty) empty.style.display = 'none';

  entries.sort((a, b) => b.data.date.localeCompare(a.data.date));

  entries.forEach(({ key, data }) => {
    const card = document.createElement('div');
    card.className = 'bake-card';

    const date = new Date(data.date);
    const dateStr = date.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
    const r = data.recipe || {};

    const outcomeCls = { great: 'outcome--great', good: 'outcome--good', ok: 'outcome--ok', disappointing: 'outcome--bad' }[data.outcome] || '';

    const outcomeEmoji = { great: '🌟', good: '👍', ok: '😐', disappointing: '👎' }[data.outcome] || '';
    card.innerHTML = `
      <div class="bake-card-header">
        <div class="bake-card-date">${dateStr}</div>
        <span class="bake-outcome ${outcomeCls}">${outcomeEmoji} ${data.outcome}</span>
        <button class="bake-delete" title="Delete" onclick="deleteBakeLog('${key}')">✕</button>
      </div>
      ${r.flour ? `<div class="bake-card-meta">${r.flour}g flour · ${r.hydration}% hydration · ${r.starter}% starter · ${r.type || ''}</div>` : ''}
      ${data.crumb ? `<div class="bake-card-tags"><span class="bake-tag">Crumb: ${data.crumb}</span></div>` : ''}
      ${data.notes ? `<p class="bake-card-notes">${data.notes}</p>` : ''}
    `;
    list.appendChild(card);
  });
}

function deleteBakeLog(key) {
  localStorage.removeItem(key);
  // Re-render the list
  const list = document.getElementById('bake-log-list');
  if (list) {
    list.innerHTML = '';
    const empty = document.createElement('p');
    empty.className = 'bake-log-empty';
    empty.id = 'bake-log-empty';
    empty.style.display = 'none';
    empty.textContent = 'No bakes recorded yet. Generate a bake plan, then use the "Record this bake" panel at the bottom to log your results.';
    list.appendChild(empty);
    renderBakeLog();
  }
}

// ── Recipe sharing ─────────────────────────────────────────────────────────

function shareRecipe() {
  const flour   = document.getElementById('flour-weight')?.value || '';
  const hydration = document.getElementById('hydration')?.value || '';
  const starter = document.getElementById('starter-pct')?.value || '';
  const salt    = document.getElementById('salt-pct')?.value || '';
  const type    = document.getElementById('bread-type-input')?.value || '';

  const params = new URLSearchParams();
  if (flour)     params.set('flour', flour);
  if (hydration) params.set('hydration', hydration);
  if (starter)   params.set('starter', starter);
  if (salt)      params.set('salt', salt);
  if (type)      params.set('type', type);

  const url = location.origin + '/?' + params.toString();
  navigator.clipboard.writeText(url).then(() => {
    showToast('Link copied to clipboard.');
  }).catch(() => {
    // Fallback for browsers without clipboard API
    prompt('Copy this link to share your recipe:', url);
  });
}

// ── Timeline step checkboxes ───────────────────────────────────────────────

function initTimelineChecks() {
  const checks = document.querySelectorAll('.step-check');
  if (!checks.length) return;
  checks.forEach(cb => {
    const idx = cb.dataset.stepIdx;
    const stored = localStorage.getItem('bb_step_' + idx);
    if (stored === '1') {
      cb.checked = true;
      cb.closest('.timeline-step').classList.add('done');
    }
    cb.addEventListener('change', () => {
      const step = cb.closest('.timeline-step');
      if (cb.checked) {
        step.classList.add('done');
        localStorage.setItem('bb_step_' + idx, '1');
      } else {
        step.classList.remove('done');
        localStorage.removeItem('bb_step_' + idx);
      }
    });
  });
}

// Re-init checkboxes and reminders after HTMX swaps the timeline into the DOM.
// Also persist form state whenever the recipe sidebar updates.
document.body.addEventListener('htmx:afterSwap', e => {
  const id = e.detail.target?.id;
  if (id === 'timeline-result') {
    // Clear step states from previous bake before initialising new ones
    Object.keys(localStorage).filter(k => k.startsWith('bb_step_')).forEach(k => localStorage.removeItem(k));
    initTimelineChecks();
    initReminders();
    // Persist timeline so it survives page refresh
    const tlEl = document.getElementById('timeline-result');
    if (tlEl) localStorage.setItem('bb_last_timeline', tlEl.innerHTML);
  }
  if (id === 'recipe-sidebar')  { saveLastState(); updateFabHydration(); unlockSections(); }
});

// ── Bake step reminders (Phase 3) ─────────────────────────────────────────

const REMINDERS_KEY = 'bb_reminders';
let _reminderTimeouts = [];

function toggleReminders() {
  const perm = Notification.permission;
  if (perm === 'denied') {
    showToast('Notifications are blocked in your browser settings.');
    return;
  }
  if (perm === 'default') {
    Notification.requestPermission().then(p => {
      if (p === 'granted') scheduleReminders();
      else showToast('Reminders need notification permission.');
    });
  } else {
    // Already granted — toggle on/off
    const existing = localStorage.getItem(REMINDERS_KEY);
    if (existing) {
      clearAllReminders();
    } else {
      scheduleReminders();
    }
  }
}

function scheduleReminders() {
  clearAllReminders();
  const steps = document.querySelectorAll('.timeline-step[data-step-time]');
  if (!steps.length) return;

  const scheduled = [];
  const now = Date.now();

  steps.forEach(el => {
    const date  = el.dataset.stepDate;
    const time  = el.dataset.stepTime;
    const label = el.dataset.stepLabel;
    const cue   = el.dataset.stepCue;
    if (!date || !time || !label) return;

    const stepMs = new Date(`${date}T${time}:00`).getTime();
    const delay  = stepMs - now;
    if (delay <= 0) return;   // step is in the past

    // Notify 2 minutes before each step
    const notifyAt = delay - 2 * 60 * 1000;
    const actualDelay = notifyAt > 0 ? notifyAt : delay;

    const tid = setTimeout(() => {
      fireStepNotification(label, cue);
    }, actualDelay);

    _reminderTimeouts.push(tid);
    scheduled.push({ time: stepMs, label, cue });
  });

  if (!scheduled.length) {
    showToast('All steps are in the past — nothing to remind you about.');
    return;
  }

  localStorage.setItem(REMINDERS_KEY, JSON.stringify(scheduled));
  updateReminderStatus(scheduled.length);
  showToast(`${scheduled.length} step reminder${scheduled.length !== 1 ? 's' : ''} set.`);
}

function clearAllReminders() {
  _reminderTimeouts.forEach(clearTimeout);
  _reminderTimeouts = [];
  localStorage.removeItem(REMINDERS_KEY);
  updateReminderStatus(0);
}

function updateReminderStatus(count) {
  const el = document.getElementById('reminders-status');
  const btn = document.getElementById('reminders-btn');
  if (!el) return;
  if (count > 0) {
    el.textContent = `${count} step reminder${count !== 1 ? 's' : ''} active. You'll be notified 2 min before each step.`;
    el.hidden = false;
    if (btn) btn.textContent = 'Clear reminders';
  } else {
    el.hidden = true;
    if (btn) btn.textContent = 'Set step reminders';
  }
}

function fireStepNotification(label, cue) {
  if (Notification.permission !== 'granted') return;
  // Use service worker notification if available (works in background on PWA)
  if (navigator.serviceWorker?.controller) {
    navigator.serviceWorker.ready.then(reg => {
      reg.showNotification('bread buddy — time to act', {
        body: cue ? `${label}: ${cue}` : label,
        icon: '/static/icons/icon-192.png',
        badge: '/static/icons/icon-192.png',
        vibrate: [200, 100, 200],
        tag: 'bb-step',
        renotify: true,
      });
    });
  } else {
    new Notification('bread buddy — time to act', {
      body: cue ? `${label}: ${cue}` : label,
      icon: '/static/icons/icon-192.png',
    });
  }
}

/** Re-schedule any future reminders from localStorage (called on page load). */
function initReminders() {
  // Update UI state based on what's stored
  const raw = localStorage.getItem(REMINDERS_KEY);
  if (!raw) return;
  try {
    const scheduled = JSON.parse(raw);
    const now = Date.now();
    const future = scheduled.filter(s => s.time > now);
    if (!future.length) { localStorage.removeItem(REMINDERS_KEY); return; }

    // Re-schedule each future step
    _reminderTimeouts.forEach(clearTimeout);
    _reminderTimeouts = [];
    future.forEach(s => {
      const delay = s.time - now - 2 * 60 * 1000;
      const actualDelay = delay > 0 ? delay : (s.time - now);
      if (actualDelay > 0) {
        const tid = setTimeout(() => fireStepNotification(s.label, s.cue), actualDelay);
        _reminderTimeouts.push(tid);
      }
    });

    // Update stored list to only future items
    localStorage.setItem(REMINDERS_KEY, JSON.stringify(future));
    updateReminderStatus(future.length);
  } catch (_) {
    localStorage.removeItem(REMINDERS_KEY);
  }
}

// ── Quick bake log helpers ─────────────────────────────────────────────────

function selectOutcome(btn) {
  document.querySelectorAll('.bake-quick-btn').forEach(b => b.classList.remove('bake-quick-btn--selected'));
  btn.classList.add('bake-quick-btn--selected');
}

function selectCrumb(btn) {
  document.querySelectorAll('.crumb-pill').forEach(b => b.classList.remove('crumb-pill--selected'));
  btn.classList.add('crumb-pill--selected');
}

// ── Progressive disclosure ────────────────────────────────────────────────

/**
 * After a successful recipe calculation, unlock downstream sections.
 * Starter section unlocks first, then Conditions and Bake Plan together.
 * This is CSS class toggling only — no hard gating.
 */
function unlockSections() {
  const starter  = document.getElementById('section-starter');
  const params   = document.getElementById('section-params');
  const timeline = document.getElementById('section-timeline');
  if (starter)  starter.classList.remove('section-locked');
  if (params)   params.classList.remove('section-locked');
  if (timeline) timeline.classList.remove('section-locked');
}

// ── Mobile sidebar bottom sheet ──────────────────────────────────────────

function toggleSidebarSheet() {
  const panel    = document.getElementById('sidebar-panel');
  const backdrop = document.getElementById('sidebar-backdrop');
  if (!panel) return;
  const isOpen = panel.classList.contains('is-open');
  if (isOpen) {
    closeSidebarSheet();
  } else {
    panel.classList.add('is-open');
    if (backdrop) backdrop.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }
}

function closeSidebarSheet() {
  const panel    = document.getElementById('sidebar-panel');
  const backdrop = document.getElementById('sidebar-backdrop');
  if (panel) panel.classList.remove('is-open');
  if (backdrop) backdrop.style.display = '';
  document.body.style.overflow = '';
}

/** Update the FAB hydration teaser when sidebar recalculates. */
function updateFabHydration() {
  const hydEl  = document.getElementById('hydration');
  const fabHyd = document.getElementById('fab-hydration');
  if (fabHyd && hydEl) fabHyd.textContent = `${hydEl.value}% hydration`;
}

// ── Charts ────────────────────────────────────────────────────────────────
// Recipe composition bar is pure CSS/Jinja2 — no JS chart library needed.

// ── Toast notification ─────────────────────────────────────────────────────

function showToast(msg) {
  let toast = document.getElementById('bb-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'bb-toast';
    toast.style.cssText = [
      'position:fixed', 'bottom:1.5rem', 'right:1.5rem',
      'background:var(--brown-dark)', 'color:#fff',
      'padding:0.6rem 1.1rem', 'border-radius:6px',
      'font-size:0.875rem', 'opacity:0',
      'transition:opacity 0.2s', 'z-index:9999',
      'pointer-events:none',
    ].join(';');
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => { toast.style.opacity = '0'; }, 2500);
}
