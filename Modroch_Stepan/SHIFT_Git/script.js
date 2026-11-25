================================================================================

// FILTROVÁNÍ — jednoduchý JavaScript, aby filtry opravdu fungovaly.
// querySelectorAll najde všechny produkty a potom je podle výběru schová nebo ukáže.
const produkty = [...document.querySelectorAll('.produkt')];
const filtry = ['auto', 'vyrobce', 'typ', 'cena', 'razeni'];
const prvek = id => document.getElementById(id);

function filtruj() {
  const auto = prvek('auto').value;
  const vyrobce = prvek('vyrobce').value;
  const typ = prvek('typ').value;
  const cena = Number(prvek('cena').value) || Infinity;
  const razeni = prvek('razeni').value;
  const hledat = (prvek('hledat').value || '').toLowerCase().trim();
  let pocet = 0;

  produkty.forEach(produkt => {
    const odpovida = (!auto || produkt.dataset.auto === auto) &&
      (!vyrobce || produkt.dataset.vyrobce === vyrobce) &&
      (!typ || produkt.dataset.typ === typ) &&
      Number(produkt.dataset.cena) <= cena &&
      (!hledat || produkt.textContent.toLowerCase().includes(hledat));
    produkt.hidden = !odpovida;
    if (odpovida) pocet++;
  });

  // Seřadíme viditelné karty podle ceny, aniž bychom je museli vytvářet znovu.
  const serazene = [...produkty];
  if (razeni === 'nejlevnejsi') serazene.sort((a,b) => Number(a.dataset.cena) - Number(b.dataset.cena));
  if (razeni === 'nejdrazsi') serazene.sort((a,b) => Number(b.dataset.cena) - Number(a.dataset.cena));
  serazene.forEach(produkt => prvek('produkty').appendChild(produkt));

  prvek('pocet').textContent = `${pocet} ${pocet === 1 ? 'produkt' : pocet >= 2 && pocet <= 4 ? 'produkty' : 'produktů'}`;
  prvek('zadne').hidden = pocet !== 0;
}

// Změna selectu spustí filtrování.
filtry.forEach(id => prvek(id).addEventListener('change', filtruj));
// Reset vrátí všechny filtry do výchozího stavu.
prvek('reset').addEventListener('click', () => { filtry.forEach(id => prvek(id).selectedIndex = 0); prvek('hledat').value = ''; filtruj(); });
filtruj();

// Vyhledávání pracuje s názvem i parametry produktů.
prvek('hledat').addEventListener('input', filtruj);
