// Mobile menu
const menuBtn = document.querySelector('.menu-btn');
const nav = document.querySelector('.nav-pill');
if (menuBtn && nav) {
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open);
    menuBtn.textContent = open ? 'Close' : 'Menu';
  });
}

// Region tabs on the home page
const regions = {
  asia: { name: 'Asia', places: 'Japan, Nepal, Vietnam, Indonesia, the Philippines' },
  europe: {
    name: 'Europe',
    trip: { title: 'Traunstein, Austria', text: 'A demanding climb above Traunsee, a mountain hut, chamois and a swim in the lake.', url: 'blog/traunstein-austria/' },
  },
  africa: { name: 'Africa', places: 'Morocco, Tanzania, Namibia, South Africa' },
  americas: { name: 'Americas', places: 'Peru, Patagonia, Canada, Mexico, the Rockies' },
  oceania: { name: 'Oceania', places: 'New Zealand, Australia, Fiji' },
};
const tabs = document.querySelectorAll('.tab');
const panelTitle = document.querySelector('#region-title');
const panelText = document.querySelector('#region-text');
const panelPlaces = document.querySelector('#region-places');
const arrow = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>';
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((t) => t.setAttribute('aria-selected', 'false'));
    tab.setAttribute('aria-selected', 'true');
    const r = regions[tab.dataset.region];
    if (r.trip) {
      panelTitle.textContent = r.trip.title;
      panelText.textContent = r.trip.text;
      panelPlaces.innerHTML = `<a class="btn" href="${r.trip.url}">Read the story ${arrow}</a>`;
    } else {
      panelTitle.textContent = `No ${r.name} trips yet`;
      panelText.textContent = 'The first stories from this part of the map are on their way.';
      panelPlaces.textContent = `On the wish list: ${r.places}`;
    }
  });
});

// Footer year
document.querySelectorAll('[data-year]').forEach((el) => (el.textContent = new Date().getFullYear()));

// Lightbox: tap any post or gallery photo to see it full size
const zoomables = document.querySelectorAll('.post-body figure img, .photo-grid img');
if (zoomables.length) {
  const box = document.createElement('div');
  box.className = 'lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.innerHTML = '<button type="button">Close</button><div><img alt=""><p></p></div>';
  document.body.appendChild(box);
  const bigImg = box.querySelector('img');
  const cap = box.querySelector('p');
  const closeBtn = box.querySelector('button');
  let last = null;
  const close = () => { box.classList.remove('open'); bigImg.src = ''; if (last) last.focus(); };
  zoomables.forEach((img) => {
    img.tabIndex = 0;
    const open = () => {
      last = img;
      bigImg.src = img.dataset.full || img.currentSrc || img.src;
      bigImg.alt = img.alt;
      const fc = img.closest('figure')?.querySelector('figcaption');
      cap.textContent = fc ? fc.textContent : '';
      box.classList.add('open');
      closeBtn.focus();
    };
    img.addEventListener('click', open);
    img.addEventListener('keydown', (e) => { if (e.key === 'Enter') open(); });
  });
  closeBtn.addEventListener('click', close);
  box.addEventListener('click', (e) => { if (e.target === box) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && box.classList.contains('open')) close(); });
}
