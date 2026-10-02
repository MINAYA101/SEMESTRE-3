document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', () => {
      const boton = form.querySelector('button[type="submit"], input[type="submit"]');
      if (boton && !boton.dataset.confirmacion) boton.disabled = false;
    });
  });
});
