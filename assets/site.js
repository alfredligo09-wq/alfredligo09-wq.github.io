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
  europe: { name: 'Europe', places: 'Switzerland, Italy, Norway, Portugal, Scotland' },
  africa: { name: 'Africa', places: 'Morocco, Tanzania, Namibia, South Africa' },
  americas: { name: 'Americas', places: 'Peru, Patagonia, Canada, Mexico, the Rockies' },
  oceania: { name: 'Oceania', places: 'New Zealand, Australia, Fiji' },
};
const tabs = document.querySelectorAll('.tab');
const panelTitle = document.querySelector('#region-title');
const panelPlaces = document.querySelector('#region-places');
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((t) => t.setAttribute('aria-selected', 'false'));
    tab.setAttribute('aria-selected', 'true');
    const r = regions[tab.dataset.region];
    panelTitle.textContent = `No ${r.name} trips yet`;
    panelPlaces.textContent = `On the wish list: ${r.places}`;
  });
});

// Footer year
document.querySelectorAll('[data-year]').forEach((el) => (el.textContent = new Date().getFullYear()));
