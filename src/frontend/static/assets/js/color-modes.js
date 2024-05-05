(() => {
    const getStoredTheme = () => localStorage.getItem('theme');
    const setStoredTheme = (theme) => localStorage.setItem('theme', theme);

    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme();
        if (storedTheme) {
            return storedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    const setTheme = (theme) => {
        if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme);
        }
    };

    setTheme(getPreferredTheme());

    const showActiveTheme = (theme, focus = false) => {
        const themeSwitcher = document.querySelector('#bd-theme');

        if (!themeSwitcher) {
            return;
        }

        const themeSwitcherText = document.querySelector('#bd-theme-text');
        const activeThemeIcon = document.getElementById('current-theme');
        const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`);
        const svgOfActiveBtn = btnToActive.querySelector('i').classList;

        document.querySelectorAll('[data-bs-theme-value]').forEach((element) => {
            element.setAttribute('aria-pressed', 'false');
        });

        btnToActive.setAttribute('aria-pressed', 'true');
        activeThemeIcon.classList = svgOfActiveBtn;
        const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`;
        themeSwitcher.setAttribute('aria-label', themeSwitcherLabel);

        if (focus) {
            themeSwitcher.focus();
        }
    };

    const toggleLogo = (theme) => {
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
    };

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        const storedTheme = getStoredTheme();
        if (storedTheme !== 'light' && storedTheme !== 'dark') {
            setTheme(getPreferredTheme());
        }
    });

    window.addEventListener('DOMContentLoaded', () => {
        showActiveTheme(getPreferredTheme());
        toggleLogo(getPreferredTheme());

        document.querySelectorAll('[data-bs-theme-value]').forEach((toggle) => {
            toggle.addEventListener('click', () => {
                const theme = toggle.getAttribute('data-bs-theme-value');
                setStoredTheme(theme);
                setTheme(theme);
                showActiveTheme(theme, true);
                toggleLogo(theme);
            });
        });
    });
})();
