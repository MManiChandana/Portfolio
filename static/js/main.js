(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const intro = document.querySelector('#siteIntro');
  const frames = [...document.querySelectorAll('.intro-frame')];
  const identity = document.querySelector('#introIdentity');
  const count = document.querySelector('#introCount');
  const closeIntro = () => intro?.classList.add('done');

  if (intro && !reduced) {
    let index = 0;
    const advance = () => {
      if (index < frames.length - 1) {
        frames[index].classList.remove('active');
        index += 1;
        frames[index].classList.add('active');
        if (count) count.textContent = `Signal ${String(index + 1).padStart(2, '0')} / ${frames.length}`;
        window.setTimeout(advance, 1550);
      } else {
        window.setTimeout(() => identity?.classList.add('show'), 500);
      }
    };
    window.setTimeout(advance, 1350);
  } else { closeIntro(); }
  document.querySelector('#introEnter')?.addEventListener('click', closeIntro);
  document.querySelector('#introSkip')?.addEventListener('click', closeIntro);

  const cursor = document.querySelector('.cursor-dot');
  if (cursor && !reduced && window.matchMedia('(pointer:fine)').matches) {
    window.addEventListener('pointermove', e => { cursor.style.left = `${e.clientX}px`; cursor.style.top = `${e.clientY}px`; });
    document.querySelectorAll('a,button,.project-card').forEach(el => {
      el.addEventListener('pointerenter', () => cursor.classList.add('active'));
      el.addEventListener('pointerleave', () => cursor.classList.remove('active'));
    });
  }

  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  }), { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  const detail = document.querySelector('#skillDetail');
  document.querySelectorAll('.skill-chip').forEach(chip => chip.addEventListener('click', () => {
    document.querySelectorAll('.skill-chip').forEach(item => item.classList.remove('selected'));
    chip.classList.add('selected');
    if (detail) detail.textContent = `${chip.dataset.title}: ${chip.dataset.description}`;
  }));

  const exploreToggle = document.querySelector('.explore-toggle');
  exploreToggle?.addEventListener('click', event => {
    event.preventDefault();
    const active = document.body.classList.toggle('lab-mode');
    exploreToggle.setAttribute('aria-pressed', String(active));
    exploreToggle.innerHTML = active ? 'Recruiter mode <span>→</span>' : 'Explore 3D lab <span>◎</span>';
  });

  const dialog = document.querySelector('#projectDialog');
  const openProject = card => {
    if (!dialog) return;
    const set = (selector, value) => { const el = document.querySelector(selector); if (el) el.textContent = value || ''; };
    set('#dialogTitle', card.dataset.title); set('#dialogTech', card.dataset.tech); set('#dialogTechnology', card.dataset.tech); set('#dialogDescription', card.dataset.description);
    const image = document.querySelector('#dialogImage'); image.src = card.dataset.image || ''; image.alt = `${card.dataset.title} preview`;
    const links = document.querySelector('#dialogLinks'); links.replaceChildren();
    [['Live demo', card.dataset.live], ['GitHub', card.dataset.repo]].forEach(([label, url]) => {
      if (url && url !== '#') { const a = document.createElement('a'); a.href = url; a.target = '_blank'; a.rel = 'noreferrer'; a.textContent = `${label} ↗`; links.append(a); }
    });
    dialog.showModal();
  };
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('click', () => openProject(card));
    card.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openProject(card); } });
  });
  document.querySelector('.dialog-close')?.addEventListener('click', () => dialog?.close());
  dialog?.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });

  const canvas = document.querySelector('#neuralCanvas');
  if (!canvas || reduced) return;
  const ctx = canvas.getContext('2d'); let dots = []; let width = 0; let height = 0; const fine = window.matchMedia('(pointer:fine)').matches;
  const resize = () => { width = canvas.width = window.innerWidth * devicePixelRatio; height = canvas.height = window.innerHeight * devicePixelRatio; canvas.style.width = `${window.innerWidth}px`; canvas.style.height = `${window.innerHeight}px`; ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0); const total = window.innerWidth < 700 ? 20 : 42; dots = Array.from({ length: total }, () => ({x: Math.random()*window.innerWidth, y: Math.random()*window.innerHeight, vx:(Math.random()-.5)*.18, vy:(Math.random()-.5)*.18})); };
  resize(); window.addEventListener('resize', resize); let mouse = {x:-999,y:-999}; if (fine) window.addEventListener('pointermove', e => mouse={x:e.clientX,y:e.clientY});
  const draw = () => { ctx.clearRect(0,0,window.innerWidth,window.innerHeight); dots.forEach(dot => { dot.x += dot.vx; dot.y += dot.vy; if(dot.x<0||dot.x>window.innerWidth) dot.vx*=-1; if(dot.y<0||dot.y>window.innerHeight) dot.vy*=-1; }); for(let a=0;a<dots.length;a++){ const d=dots[a]; ctx.beginPath(); ctx.arc(d.x,d.y,1.35,0,Math.PI*2); ctx.fillStyle='rgba(132,227,208,.58)'; ctx.fill(); for(let b=a+1;b<dots.length;b++){const q=dots[b],dx=d.x-q.x,dy=d.y-q.y,dist=Math.hypot(dx,dy);if(dist<125){ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(q.x,q.y);ctx.strokeStyle=`rgba(139,126,255,${.16*(1-dist/125)})`;ctx.stroke();}} const md=Math.hypot(d.x-mouse.x,d.y-mouse.y);if(md<150){ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(mouse.x,mouse.y);ctx.strokeStyle=`rgba(132,227,208,${.22*(1-md/150)})`;ctx.stroke();}} requestAnimationFrame(draw); };
  draw();
})();
