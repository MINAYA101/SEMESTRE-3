document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('mobile-open');
      nav.style.display = nav.classList.contains('mobile-open') ? 'flex' : '';
      nav.style.position = 'absolute';
      nav.style.top = '78px';
      nav.style.left = '0';
      nav.style.right = '0';
      nav.style.padding = '18px 22px';
      nav.style.background = '#fff';
      nav.style.borderBottom = '1px solid #e6e9ed';
      nav.style.flexDirection = 'column';
      nav.style.alignItems = 'flex-start';
    });
  }

  const input = document.querySelector('#tableSearch');
  const table = document.querySelector('#dataTable');
  if (input && table) {
    input.addEventListener('input', () => {
      const term = input.value.toLowerCase().trim();
      table.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(term) ? '' : 'none';
      });
    });
  }
});
