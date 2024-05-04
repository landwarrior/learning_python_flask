document.addEventListener('DOMContentLoaded', () => {
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const theme = localStorage.getItem('theme') || systemTheme;
    document.documentElement.setAttribute('data-bs-theme', theme);

    document.getElementById('theme-switch').addEventListener('click', (e) => {
        e.preventDefault();
        const theme = e.target.dataset.theme;
        if (theme === 'auto') {
            updateTheme(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        } else {
            updateTheme(theme);
        }
        const cls = e.target.querySelector('i').classList;
        document.getElementById('current-theme').classList = cls;
    });
});

// システムのカラースキームが変更されたときにテーマを更新する関数
function updateTheme(selectedTheme) {
    localStorage.setItem('theme', selectedTheme);
    document.documentElement.setAttribute('data-bs-theme', selectedTheme);
}
