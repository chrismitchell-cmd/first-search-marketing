(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Sticky header shadow
  const header = document.querySelector('.site-header');
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  const nav = document.querySelector('.nav');
  const toggle = document.querySelector('.nav__toggle');
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    toggle.querySelector('use').setAttribute('href', open ? '#i-close' : '#i-menu');
  });
  nav.querySelectorAll('.nav__menu a').forEach(a => a.addEventListener('click', () => {
    if (nav.classList.contains('is-open')) toggle.click();
  }));

  // Services dropdown (tap to open on mobile; hover/focus handles desktop)
  document.querySelectorAll('.has-dropdown > .nav__link').forEach(btn => {
    btn.addEventListener('click', () => {
      const li = btn.parentElement;
      const open = li.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open);
    });
  });

  // Reveal on scroll
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => io.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('is-visible'));
  }

  // "What We Do… ___" typewriter
  const typer = document.querySelector('.typer');
  if (typer && !reduceMotion) {
    const words = typer.dataset.words.split('|');
    let w = 0, i = words[0].length, deleting = true;
    const tick = () => {
      const word = words[w];
      typer.textContent = word.slice(0, i);
      if (deleting) {
        if (i > 0) { i--; setTimeout(tick, 55); }
        else { deleting = false; w = (w + 1) % words.length; setTimeout(tick, 250); }
      } else {
        const next = words[w];
        if (i < next.length) { i++; typer.textContent = next.slice(0, i); setTimeout(tick, 95); }
        else { deleting = true; setTimeout(tick, 1800); }
      }
    };
    setTimeout(tick, 1800);
  }

  // Count-up stats
  const counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const cio = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target, target = +el.dataset.count, start = performance.now(), dur = 1400;
        const step = now => {
          const p = Math.min((now - start) / dur, 1);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        };
        el.textContent = '0';
        requestAnimationFrame(step);
        cio.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(el => cio.observe(el));
  }

  // Three Ways — expanding panels
  const ways = document.querySelectorAll('.way');
  const activate = panel => ways.forEach(p => {
    const on = p === panel;
    p.classList.toggle('is-active', on);
    p.setAttribute('aria-selected', on);
  });
  ways.forEach(p => {
    p.addEventListener('click', () => activate(p));
    p.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(p); }
    });
    if (window.matchMedia('(hover: hover) and (min-width: 861px)').matches) {
      p.addEventListener('mouseenter', () => activate(p));
    }
  });

  // Testimonials carousel
  const track = document.querySelector('.carousel__track');
  document.querySelectorAll('.carousel__btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const card = track.querySelector('.review');
      const gap = parseFloat(getComputedStyle(track).columnGap) || 24;
      const step = card.getBoundingClientRect().width + gap;
      const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      if (+btn.dataset.dir > 0 && atEnd) track.scrollTo({ left: 0 });
      else track.scrollBy({ left: step * +btn.dataset.dir });
    });
  });

  // Newsletter — client-side validation only; hook up to the real endpoint
  const form = document.querySelector('.js-newsletter');
  if (form) {
    form.addEventListener('submit', e => {
      const email = form.querySelector('[type=email]');
      const msg = form.querySelector('.form-msg');
      if (!email.checkValidity() || !email.value) {
        e.preventDefault();
        msg.textContent = 'Please enter a valid email address.';
        email.focus();
        return;
      }
      if (form.getAttribute('action') === '#') {
        e.preventDefault();
        msg.textContent = "Thanks! You're on the list for weekly marketing tips.";
        form.reset();
      }
    });
  }

  document.querySelectorAll('.js-year').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
