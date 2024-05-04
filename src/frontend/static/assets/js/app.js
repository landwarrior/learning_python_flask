document.addEventListener('DOMContentLoaded', () => {
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const theme = localStorage.getItem('theme') || systemTheme;
    document.documentElement.setAttribute('data-bs-theme', theme);
    if (theme === 'light') {
        document.getElementById('logo_dark').classList.add('d-none');
        document.getElementById('logo_dark').classList.remove('d-inline-block');
        document.getElementById('logo_light').classList.remove('d-none');
        document.getElementById('logo_light').classList.add('d-inline-block');
    } else {
        document.getElementById('logo_light').classList.remove('d-inline-block');
        document.getElementById('logo_light').classList.add('d-none');
        document.getElementById('logo_dark').classList.remove('d-none');
        document.getElementById('logo_dark').classList.add('d-inline-block');
    }

    document.getElementById('theme-switch').addEventListener('click', (e) => {
        e.preventDefault();
        let theme = e.target.dataset.theme;
        if (theme === 'auto') {
            theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        updateTheme(theme);
        document.getElementById('current-theme').classList = e.target.querySelector('i').classList;
        if (theme === 'light') {
            document.getElementById('logo_dark').classList.add('d-none');
            document.getElementById('logo_dark').classList.remove('d-inline-block');
            document.getElementById('logo_light').classList.remove('d-none');
            document.getElementById('logo_light').classList.add('d-inline-block');
        } else {
            document.getElementById('logo_light').classList.remove('d-inline-block');
            document.getElementById('logo_light').classList.add('d-none');
            document.getElementById('logo_dark').classList.remove('d-none');
            document.getElementById('logo_dark').classList.add('d-inline-block');
        }
    });
});

// システムのカラースキームが変更されたときにテーマを更新する関数
function updateTheme(selectedTheme) {
    localStorage.setItem('theme', selectedTheme);
    document.documentElement.setAttribute('data-bs-theme', selectedTheme);
}
