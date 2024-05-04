document.addEventListener('DOMContentLoaded', () => {
    const selectedTheme = localStorage.getItem('theme') || 'auto';
    let theme = selectedTheme;
    if (selectedTheme === 'auto') {
        theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-bs-theme', theme);
    if (theme === 'light') {
        document.getElementById('logo_dark').classList.toggle('d-inline-block');
        document.getElementById('logo_dark').classList.toggle('d-none');
    } else {
        document.getElementById('logo_light').classList.toggle('d-inline-block');
        document.getElementById('logo_light').classList.toggle('d-none');
    }
    toggleLogo(theme);
    toggleIcon(selectedTheme);

    document.getElementById('theme-switch').addEventListener('click', (e) => {
        e.preventDefault();
        let theme = e.target.dataset.theme;
        localStorage.setItem('theme', theme);
        if (theme === 'auto') {
            theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        document.documentElement.setAttribute('data-bs-theme', theme);
        document.getElementById('current-theme').classList = e.target.querySelector('i').classList;
        toggleLogo(theme);
    });
});

/**
 * テーマによってロゴを切り替える
 * @param {string} theme テーマ
 */
function toggleLogo(theme) {
    if (theme === 'light') {
        document.getElementById('logo_dark').classList.add('d-none');
        document.getElementById('logo_dark').classList.remove('d-inline-block');
        document.getElementById('logo_light').classList.remove('d-none');
        document.getElementById('logo_light').classList.add('d-inline-block');
    } else {
        document.getElementById('logo_light').classList.add('d-none');
        document.getElementById('logo_light').classList.remove('d-inline-block');
        document.getElementById('logo_dark').classList.remove('d-none');
        document.getElementById('logo_dark').classList.add('d-inline-block');
    }
}

/**
 * テーマによってアイコンを切り替える
 * @param {string} theme テーマ
 */
function toggleIcon(theme) {
    if (theme === 'auto') {
        document.getElementById('current-theme').classList = ['bi bi-circle-half'];
    } else if (theme === 'light') {
        document.getElementById('current-theme').classList = ['bi bi-brightness-high-fill'];
    } else {
        document.getElementById('current-theme').classList = ['bi bi-moon-stars-fill'];
    }
}
