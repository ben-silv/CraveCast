/* ══ CraveCast — Apple layer: motion ═══════════════════════════════════
   Runs after the app's own script (build-apple.py appends it), and only
   wraps what is already there: showTab, renderRisk, renderGarden and the
   dialogs. No app logic lives here.

   Everything touchable moves on springs described the way Apple describes
   them — a damping ratio and a response — so motion always starts from the
   value on screen, carries velocity, and can be grabbed mid-flight. */
(() => {
"use strict";

const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
const phone = matchMedia("(max-width: 700px)");
const q = s => document.querySelector(s);

/* ── a spring: damping ratio + response (seconds), mass 1 ─────────── */
class Spring{
  constructor({value = 0, damping = 1, response = .4, precision = .01, onUpdate, onRest} = {}){
    Object.assign(this, {value, target: value, velocity: 0, damping, response,
                         precision, onUpdate, onRest});
    this.raf = 0;
  }
  get running(){ return this.raf !== 0; }
  to(target, {velocity, damping, response} = {}){
    this.target = target;
    if(velocity !== undefined) this.velocity = velocity;
    if(damping !== undefined) this.damping = damping;
    if(response !== undefined) this.response = response;
    if(reduceMotion.matches){ this.jump(target); this.onRest?.(target); return this; }
    if(!this.raf){ this.last = performance.now(); this.raf = requestAnimationFrame(t => this.tick(t)); }
    return this;
  }
  jump(v){ this.stop(); this.value = this.target = v; this.velocity = 0; this.onUpdate?.(v); }
  stop(){ if(this.raf) cancelAnimationFrame(this.raf); this.raf = 0; }
  tick(now){
    let dt = Math.min(.064, (now - this.last) / 1000);
    this.last = now;
    const k = (2 * Math.PI / this.response) ** 2;          // stiffness
    const c = 4 * Math.PI * this.damping / this.response;  // damping coefficient
    while(dt > 0){                                         // fixed 240 Hz substeps
      const h = Math.min(1 / 240, dt);
      this.velocity += (-k * (this.value - this.target) - c * this.velocity) * h;
      this.value += this.velocity * h;
      dt -= h;
    }
    if(Math.abs(this.value - this.target) < this.precision &&
       Math.abs(this.velocity) < this.precision * 10){
      this.value = this.target; this.velocity = 0; this.raf = 0;
      this.onUpdate?.(this.value); this.onRest?.(this.value);
      return;
    }
    this.onUpdate?.(this.value);
    this.raf = requestAnimationFrame(t => this.tick(t));
  }
}

/* velocity from the last ~100ms of samples; a pointer that stopped before
   letting go has no velocity, however fast it moved earlier */
function tracker(){
  const pts = [];
  return {
    add(x, t){ pts.push([x, t]); while(pts.length > 2 && t - pts[0][1] > 100) pts.shift(); },
    v(now){
      if(pts.length < 2) return 0;
      const [x0, t0] = pts[0], [x1, t1] = pts[pts.length - 1];
      if(now - t1 > 80 || t1 <= t0) return 0;
      return (x1 - x0) / (t1 - t0) * 1000;
    },
  };
}
// where a flick would come to rest (Apple's decay projection)
const project = (v, d = .998) => (v / 1000) * d / (1 - d);
// resistance past an edge: the further out, the less it follows
const rubber = (o, dim, c = .55) => (o * dim * c) / (dim + c * Math.abs(o));
const haptic = ms => { try{ navigator.vibrate?.(ms); }catch(e){} };

/* ── 1. press feedback: on pointer-down, released on a spring ──────── */
const PRESSABLE = "button, [role=button], summary, .cc-day";
const pressSprings = new WeakMap();
let pressed = null;
function pressSpring(el){
  let s = pressSprings.get(el);
  if(!s){
    s = new Spring({value: 1, response: .3, precision: .0005,
                    onUpdate: v => { el.style.scale = v === 1 ? "" : v; }});
    pressSprings.set(el, s);
  }
  return s;
}
document.addEventListener("pointerdown", e => {
  if(e.button !== 0) return;
  const el = e.target.closest(PRESSABLE);
  if(!el || el.disabled || el.closest(".cc-stage3d")) return;
  // shrink by a few pixels, not a fixed percentage: a full-width row
  // scaled to 97% would lurch
  const k = Math.max(.96, 1 - 7 / Math.max(1, el.offsetWidth));
  const s = pressSpring(el);
  s.stop(); s.value = s.target = k; s.velocity = 0;
  el.style.scale = k;
  pressed = el;
}, {passive: true});
const unpress = () => { if(pressed){ pressSpring(pressed).to(1); pressed = null; } };
document.addEventListener("pointerup", unpress, {passive: true});
document.addEventListener("pointercancel", unpress, {passive: true});
document.addEventListener("pointermove", e => {
  if(!pressed) return;
  // dragging off the target cancels the press
  const r = pressed.getBoundingClientRect(), pad = 10;
  if(e.clientX < r.left - pad || e.clientX > r.right + pad ||
     e.clientY < r.top - pad || e.clientY > r.bottom + pad) unpress();
}, {passive: true});

/* ── 2. the top bar becomes a material only once something is under it */
const bar = q(".cc-top");
const edge = () => bar.classList.toggle("scrolled", scrollY > 2);
addEventListener("scroll", edge, {passive: true});
edge();

/* ── 3. segmented control thumb + phone tab bar ────────────────────── */
const nav = q("#tabBar");
const ind = document.createElement("span");
ind.className = "ind"; ind.setAttribute("aria-hidden", "true");
nav.prepend(ind);
const paintInd = () => {
  ind.style.transform = `translateX(${indX.value}px)`;
  ind.style.width = indW.value + "px";
};
const indX = new Spring({response: .34, precision: .1, onUpdate: paintInd});
const indW = new Spring({response: .34, precision: .1, onUpdate: paintInd});
function placeInd(animate){
  const b = nav.querySelector('[role=tab][aria-selected="true"]');
  const wasHidden = ind.style.opacity === "0";
  ind.style.opacity = b ? 1 : 0;
  if(!b) return;
  // coming back from a view with no tab (the result), it appears in place
  if(animate && !wasHidden){ indX.to(b.offsetLeft); indW.to(b.offsetWidth); }
  else { indX.jump(b.offsetLeft); indW.jump(b.offsetWidth); }
}
// a fixed bar can't live inside the blurred header (backdrop-filter makes
// the header its containing block), so on phones the nav moves to <body>
const navSlot = document.createComment("tab bar slot");
nav.after(navSlot);
function placeNav(){
  if(phone.matches){ document.body.append(nav); nav.classList.add("tabbar"); }
  else { navSlot.before(nav); nav.classList.remove("tabbar"); }
  placeInd(false);
}
phone.addEventListener("change", placeNav);
placeNav();
new ResizeObserver(() => placeInd(false)).observe(nav);

/* ── 4. views enter from the side of the tab you moved toward ──────── */
const ORDER = ["home", "log", "result", "garden", "history"];
const baseShowTab = showTab;
showTab = function(name){
  const from = ORDER.indexOf(TAB), to = ORDER.indexOf(name);
  const dir = from < 0 || to < 0 || from === to ? 0 : Math.sign(to - from);
  const root = document.documentElement.style;
  root.setProperty("--dx", dir * 28 + "px");
  root.setProperty("--dy", dir ? "0px" : "8px");
  baseShowTab(name);
  placeInd(true);
};

/* ── 5. the risk ring counts from what it showed last ──────────────── */
const tone = v => v >= 67 ? "#FB7185" : v >= 34 ? "#F59E0B" : "#10B981";
const ring = new Spring({value: 0, response: .7, precision: .05, onUpdate: v => {
  q("#riskArc").style.background = `conic-gradient(${tone(v)} ${v}%, var(--ring-track) 0)`;
  q("#riskNum").innerHTML = Math.round(v) + "<span>%</span>";
}});
const baseRenderRisk = renderRisk;
renderRisk = function(){
  baseRenderRisk.apply(this, arguments);
  ring.to(riskNow());
};
renderRisk();

/* ── 6. the garden plot: grab it and spin it ───────────────────────── */
const stage = q(".cc-stage3d"), plane = q("#gPlane");
function paintRot(r){
  const a = (((r % 90) + 90) % 90) * Math.PI / 180;
  const fit = 1 / (Math.cos(a) + Math.sin(a));
  plane.style.transform = `rotateX(58deg) rotateZ(${r}deg) scale(${fit})`;
  const upright = `translate(-50%,-50%) rotateZ(${-r}deg) rotateX(-58deg) translateY(-11px)`;
  for(const e of plane.querySelectorAll(".cc-tile .e")) e.style.transform = upright;
}
const rot = new Spring({value: S.garden.rot || 0, response: .4, precision: .05,
  onUpdate: paintRot,
  onRest: v => { S.garden.rot = Math.round(v); save(); haptic(6); }});
let grab = null, swallowClick = false;

const baseRenderGarden = renderGarden;
renderGarden = function(){
  baseRenderGarden.apply(this, arguments);
  // a redraw mid-spin must not snap the plot back to the saved angle
  if(rot.running || grab?.live) paintRot(rot.value);
  else rot.value = rot.target = S.garden.rot;
};

// the buttons retarget the same spring, so tapping three times quickly
// carries on smoothly instead of queueing three separate turns
for(const [sel, step] of [["#gRotL", -45], ["#gRotR", 45]]){
  q(sel).addEventListener("click", e => {
    e.stopImmediatePropagation();
    const base = rot.running ? rot.target : rot.value;
    rot.to(base + step, {damping: 1, response: .4});
  }, true);
}

const DEG_PER_PX = .45;
stage.addEventListener("pointerdown", e => {
  if(e.button !== 0) return;
  grab = {id: e.pointerId, x0: e.clientX, y0: e.clientY, live: false, vt: tracker()};
});
stage.addEventListener("pointermove", e => {
  if(!grab || e.pointerId !== grab.id) return;
  if(!grab.live){
    const dx = e.clientX - grab.x0, dy = e.clientY - grab.y0;
    if(Math.abs(dy) > 10 && Math.abs(dy) > Math.abs(dx)){ grab = null; return; } // a scroll
    if(Math.abs(dx) < 10) return;                                                // hysteresis
    rot.stop();                       // catch it wherever it is, mid-spin or not
    grab.live = true; grab.x0 = e.clientX; grab.r0 = rot.value;
    stage.setPointerCapture(e.pointerId);
    stage.classList.add("grabbing");
    unpress();
  }
  const r = grab.r0 + (e.clientX - grab.x0) * DEG_PER_PX;
  rot.value = rot.target = r; rot.velocity = 0;
  paintRot(r);
  grab.vt.add(r, e.timeStamp);
});
function letGo(e){
  if(!grab || e.pointerId !== grab.id) return;
  const g = grab; grab = null;
  if(!g.live) return;
  stage.classList.remove("grabbing");
  swallowClick = true; setTimeout(() => { swallowClick = false; }, 0);
  const v = e.type === "pointercancel" ? 0 : g.vt.v(e.timeStamp);   // deg/s
  const target = Math.round((rot.value + project(v, .99)) / 45) * 45;
  // a flick earns a little overshoot; a slow placement settles flat
  rot.to(target, {velocity: v, damping: Math.abs(v) > 90 ? .8 : 1, response: .4});
}
stage.addEventListener("pointerup", letGo);
stage.addEventListener("pointercancel", letGo);
// releasing a drag over a tile must not also plant in it
document.addEventListener("click", e => {
  if(swallowClick){ e.stopPropagation(); e.preventDefault(); swallowClick = false; }
}, true);

/* ── 7. dialogs: cards that materialise on desktop, sheets on phones ─ */
const scrim = document.createElement("div");
scrim.className = "ap-scrim";
document.body.append(scrim);
const main = q(".cc-main");
const levels = new Map();
function setDim(dlg, v){
  levels.set(dlg, v);
  const m = Math.max(0, ...levels.values());
  scrim.style.opacity = m;
  scrim.style.visibility = m > 0.001 ? "visible" : "hidden";
  if(m > 0.001){
    // push the page back around what is on screen, not the top of <main>
    main.style.transformOrigin = `50% ${scrollY + innerHeight / 2 - main.offsetTop}px`;
    main.style.transform = `scale(${1 - .025 * m})`;
  } else main.style.transform = "";
}

const nativeShow = HTMLDialogElement.prototype.showModal;
const nativeClose = HTMLDialogElement.prototype.close;

for(const dlg of document.querySelectorAll("dialog")){
  const hd = dlg.querySelector(".dlg-hd");
  const grabber = document.createElement("span");
  grabber.className = "sheet-grab"; grabber.setAttribute("aria-hidden", "true");
  hd?.prepend(grabber);

  let closing = false, returnValue;
  const clamp = v => Math.min(1, Math.max(0, v));
  const clear = () => { dlg.style.transform = dlg.style.opacity = dlg.style.filter = ""; };

  // one progress value, 0 = away, 1 = presented; above 1 is a rubber-band
  const p = new Spring({value: 0, precision: .001,
    onUpdate(v){
      if(phone.matches){
        dlg.style.transform = v === 1 ? "" : `translateY(${(1 - v) * dlg.offsetHeight}px)`;
        dlg.style.opacity = dlg.style.filter = "";
      } else {
        const c = clamp(v);
        // a material arriving: blur and scale resolve together with opacity
        dlg.style.transform = c === 1 ? "" : `scale(${.95 + .05 * c})`;
        dlg.style.opacity = c === 1 ? "" : c;
        dlg.style.filter = c > .995 ? "" : `blur(${(1 - c) * 10}px)`;
      }
      setDim(dlg, clamp(v));
    },
    onRest(v){
      if(v === 0 && closing){ closing = false; nativeClose.call(dlg, returnValue); clear(); setDim(dlg, 0); }
    }});

  dlg.showModal = function(){
    closing = false;
    if(!dlg.open){ nativeShow.call(dlg); p.jump(0); }
    if(reduceMotion.matches){
      p.jump(1); clear();
      dlg.animate([{opacity: 0}, {opacity: 1}], {duration: 200, easing: "ease-out"});
      return;
    }
    p.to(1, {damping: 1, response: phone.matches ? .38 : .3});
  };
  dlg.close = function(rv){
    if(!dlg.open) return;
    returnValue = rv; closing = true;
    if(reduceMotion.matches){
      dlg.animate([{opacity: 1}, {opacity: 0}], {duration: 160, easing: "ease-in"})
         .finished.then(() => { if(closing) p.to(0); });
      return;
    }
    // leaves along the path it came in on
    p.to(0, {damping: 1, response: .28});
  };
  dlg.addEventListener("cancel", e => { e.preventDefault(); dlg.close(); });
  // safety net: if the browser closes it on its own, don't leave the page dimmed
  dlg.addEventListener("close", () => { if(p.value !== 0 || closing){ closing = false; p.jump(0); clear(); setDim(dlg, 0); } });

  /* drag the sheet by its header (phones) */
  if(!hd) continue;
  let drag = null;
  hd.addEventListener("pointerdown", e => {
    if(!phone.matches || e.button !== 0 || e.target.closest("button,input,select,textarea,a")) return;
    p.stop();                                   // grab it even while it is moving
    drag = {id: e.pointerId, y0: e.clientY, h: dlg.offsetHeight,
            start: (1 - p.value) * dlg.offsetHeight, vt: tracker()};
    hd.setPointerCapture(e.pointerId);
  });
  hd.addEventListener("pointermove", e => {
    if(!drag || e.pointerId !== drag.id) return;
    let y = drag.start + (e.clientY - drag.y0);
    drag.raw = y;
    if(y < 0) y = -rubber(-y, drag.h);          // pulling up past the top resists
    p.value = p.target = 1 - y / drag.h; p.velocity = 0;
    p.onUpdate(p.value);
    drag.vt.add(e.clientY, e.timeStamp);
  });
  const release = e => {
    if(!drag || e.pointerId !== drag.id) return;
    const d = drag; drag = null;
    const vy = e.type === "pointercancel" ? 0 : d.vt.v(e.timeStamp);    // px/s, + is down
    const y = d.raw ?? d.start;
    // decide from where the flick is going, not where the finger stopped
    const dismiss = y + project(vy) > d.h * .5;
    closing = dismiss;
    if(dismiss){ returnValue = undefined; haptic(8); }
    p.to(dismiss ? 0 : 1, {velocity: -vy / d.h, damping: dismiss ? 1 : .8, response: .3});
  };
  hd.addEventListener("pointerup", release);
  hd.addEventListener("pointercancel", release);
}

/* ── 8. haptics only where something is committed ──────────────────── */
q("#logSubmit")?.addEventListener("click", () => haptic(10));
q("#plantBtn")?.addEventListener("click", () => haptic(10));
})();
