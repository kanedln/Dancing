/* =========================================================
   HOT MAID CLEANING — site behaviour
   Vanilla JS, no dependencies.
   ========================================================= */
(() => {
  'use strict';

  /* ---------------------------------------------------------
     CONFIG — set this to your form endpoint (Formspree,
     Netlify Forms, Basin, your own API…). Leave it empty and
     the form falls back to opening a pre-filled email.
     --------------------------------------------------------- */
  const FORM_ENDPOINT = '';                       // e.g. 'https://formspree.io/f/abcdwxyz'
  const FALLBACK_EMAIL = 'myhotcleaning@gmail.com';

  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- current year ---------------- */
  const yearEl = $('#year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------------- sticky header state ---------------- */
  const header = $('#header');
  const onScroll = () => header.classList.toggle('is-stuck', window.scrollY > 12);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------------- mobile navigation ---------------- */
  const burger = $('#burger');
  const nav    = $('#nav');
  let scrim;

  const setNav = (open) => {
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('nav-open', open);

    if (open) {
      scrim = document.createElement('div');
      scrim.className = 'nav-scrim';
      scrim.addEventListener('click', () => setNav(false));
      document.body.appendChild(scrim);
      requestAnimationFrame(() => scrim.classList.add('is-on'));
    } else if (scrim) {
      scrim.remove();
      scrim = null;
    }
  };

  burger.addEventListener('click', () => setNav(!nav.classList.contains('is-open')));
  $$('#nav a').forEach(a => a.addEventListener('click', () => setNav(false)));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) { setNav(false); burger.focus(); }
  });
  // Reset the drawer if the viewport grows past the mobile breakpoint.
  window.matchMedia('(min-width: 881px)').addEventListener('change', e => { if (e.matches) setNav(false); });

  /* ---------------- scroll reveal ---------------- */
  const revealables = $$('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach(el => el.classList.add('is-in'));
  } else {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        // Small stagger for siblings entering together.
        entry.target.style.transitionDelay = `${Math.min(i * 70, 280)}ms`;
        entry.target.classList.add('is-in');
        obs.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    revealables.forEach(el => io.observe(el));
  }

  /* ---------------- count-up stats ---------------- */
  const counters = $$('[data-count]');
  const runCount = (el) => {
    const target = Number(el.dataset.count) || 0;
    const suffix = el.dataset.suffix || '+';
    if (reduced) { el.textContent = target.toLocaleString() + suffix; return; }

    const dur = 1400;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString() + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  if ('IntersectionObserver' in window) {
    const co = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        runCount(entry.target);
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.6 });
    counters.forEach(el => co.observe(el));
  } else {
    counters.forEach(runCount);
  }

  /* ---------------- active nav link on scroll ---------------- */
  const sections = $$('main section[id]');
  const navLinks = new Map($$('.nav__list a').map(a => [a.getAttribute('href').slice(1), a]));
  if ('IntersectionObserver' in window && sections.length) {
    const so = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const link = navLinks.get(entry.target.id);
        if (!link) return;
        if (entry.isIntersecting) {
          navLinks.forEach(l => l.classList.remove('is-active'));
          link.classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(s => so.observe(s));
  }

  /* ---------------- before / after slider ---------------- */
  const ba = $('#ba');
  if (ba) {
    const range = $('#baRange');
    const paint = () => ba.style.setProperty('--pos', `${range.value}%`);
    range.addEventListener('input', paint);
    paint();

    // Drop real photos in without touching the CSS:
    // set data-replace on the .ba__img elements and they load here.
    $$('.ba__img[data-replace]', ba).forEach(el => {
      const src = el.dataset.replace.trim();
      if (!src) return;                       // keep the branded placeholder
      const probe = new Image();
      probe.onload = () => { el.style.backgroundImage = `url("${src}")`; };
      probe.src = src;
    });
  }

  /* ---------------- quote form ---------------- */
  const form = $('#quoteForm');
  if (form) {
    const status = $('#formStatus');
    const btn = $('#submitBtn');

    const rules = {
      'f-name':    v => v.trim().length >= 2            || 'Please enter your name.',
      'f-phone':   v => /[\d\s()+.-]{7,}/.test(v.trim()) || 'Please enter a phone number we can reach you on.',
      'f-email':   v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || 'Please enter a valid email address.',
      'f-service': v => v !== ''                        || 'Pick the service you need.'
    };

    const validateField = (id) => {
      const input = document.getElementById(id);
      const wrap  = input.closest('.field');
      const msgEl = form.querySelector(`[data-err-for="${id}"]`);
      const result = rules[id](input.value);
      const ok = result === true;

      wrap.classList.toggle('is-invalid', !ok);
      input.setAttribute('aria-invalid', String(!ok));
      if (msgEl) msgEl.textContent = ok ? '' : result;
      return ok;
    };

    Object.keys(rules).forEach(id => {
      const input = document.getElementById(id);
      input.addEventListener('blur', () => validateField(id));
      input.addEventListener('input', () => {
        if (input.closest('.field').classList.contains('is-invalid')) validateField(id);
      });
    });

    const mailtoFallback = (data) => {
      const body = [
        `Name: ${data.name}`,
        `Phone: ${data.phone}`,
        `Email: ${data.email}`,
        `Service: ${data.service}`,
        `Beds/baths: ${data.size || '—'}`,
        '',
        'Notes:',
        data.notes || '—'
      ].join('\n');
      window.location.href =
        `mailto:${FALLBACK_EMAIL}?subject=${encodeURIComponent('Free quote request — ' + data.name)}` +
        `&body=${encodeURIComponent(body)}`;
    };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      status.textContent = '';
      status.className = 'form__status';

      // Honeypot: silently accept and drop bot submissions.
      if (form.company.value) return;

      const invalid = Object.keys(rules).filter(id => !validateField(id));
      if (invalid.length) {
        status.textContent = 'Please fix the highlighted fields.';
        status.classList.add('is-err');
        document.getElementById(invalid[0]).focus();
        return;
      }

      const data = Object.fromEntries(new FormData(form).entries());
      btn.disabled = true;
      btn.textContent = 'Sending…';

      if (!FORM_ENDPOINT) {
        mailtoFallback(data);
        status.textContent = 'Opening your email app so you can send the request…';
        status.classList.add('is-ok');
        btn.disabled = false;
        btn.textContent = 'Send My Free Quote Request';
        return;
      }

      try {
        const res = await fetch(FORM_ENDPOINT, {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: new FormData(form)
        });
        if (!res.ok) throw new Error(`Request failed: ${res.status}`);

        form.reset();
        status.textContent = 'Got it — we’ll text or email your quote within one business hour.';
        status.classList.add('is-ok');
        btn.textContent = 'Request Sent ✓';
      } catch (err) {
        status.innerHTML =
          `Something went wrong. Call <a href="tel:+19203779509">(920) 377-9509</a> or email ` +
          `<a href="mailto:${FALLBACK_EMAIL}">${FALLBACK_EMAIL}</a>.`;
        status.classList.add('is-err');
        btn.disabled = false;
        btn.textContent = 'Send My Free Quote Request';
      }
    });
  }
})();
