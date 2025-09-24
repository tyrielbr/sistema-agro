document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.createElement('button');
    toggle.classList.add('toggle-dark');
    toggle.innerText = '🌙';
    toggle.onclick = () => {
      document.body.classList.toggle('dark-mode');
      toggle.innerText = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    };
    document.body.appendChild(toggle);

    // Fade-in animation for main content
    document.querySelector('main').classList.add('fade-in');

    // Chart.js example (adapt for each dashboard)
    if (document.getElementById('exampleChart')) {
      new Chart(document.getElementById('exampleChart'), {
        type: 'bar',
        data: { labels: ['Janeiro', 'Fevereiro'], datasets: [{ label: 'Produtividade', data: [100, 200] }] }
      });
    }
  });