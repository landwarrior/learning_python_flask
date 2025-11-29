/**
 * カラーモード（ダークモード/ライトモード）の切り替えを管理するモジュール
 * Bootstrapのテーマ切り替え機能と連携して動作します
 */
(() => {
    /**
     * localStorageから保存されているテーマ設定を取得
     * @returns {string|null} 保存されているテーマ（'light', 'dark', 'auto'）またはnull
     */
    const getStoredTheme = () => localStorage.getItem('theme');

    /**
     * テーマ設定をlocalStorageに保存
     * @param {string} theme - 保存するテーマ（'light', 'dark', 'auto'）
     */
    const setStoredTheme = (theme) => localStorage.setItem('theme', theme);

    /**
     * 優先されるテーマを取得
     * 保存されているテーマがあればそれを返し、なければシステム設定に基づいて判定
     * @returns {string} 優先されるテーマ（'light' または 'dark'）
     */
    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme();
        // 保存されているテーマがあればそれを返す
        if (storedTheme) {
            return storedTheme;
        }
        // システム設定がダークモードなら'dark'、そうでなければ'light'を返す
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    /**
     * テーマをHTML要素に適用
     * @param {string} theme - 適用するテーマ（'light', 'dark', 'auto'）
     */
    const setTheme = (theme) => {
        // 'auto'が指定されていて、システム設定がダークモードの場合は'dark'を適用
        if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
        } else {
            // それ以外の場合は指定されたテーマをそのまま適用
            document.documentElement.setAttribute('data-bs-theme', theme);
        }
    };

    // ページ読み込み時に優先されるテーマを適用
    setTheme(getPreferredTheme());

    /**
     * アクティブなテーマをUIに表示
     * テーマ切り替えボタンの状態を更新し、アクセシビリティ属性も設定
     * @param {string} theme - 表示するテーマ
     * @param {boolean} focus - テーマ切り替えボタンにフォーカスを当てるかどうか（デフォルト: false）
     */
    const showActiveTheme = (theme, focus = false) => {
        const themeSwitcher = document.querySelector('#bd-theme');

        // テーマ切り替えボタンが存在しない場合は処理を終了
        if (!themeSwitcher) {
            return;
        }

        const themeSwitcherText = document.querySelector('#bd-theme-text');
        const activeThemeIcon = document.getElementById('current-theme');
        // 指定されたテーマに対応するボタンを取得
        const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`);
        const svgOfActiveBtn = btnToActive.querySelector('i').classList;

        // すべてのテーマボタンのaria-pressed属性をfalseに設定
        document.querySelectorAll('[data-bs-theme-value]').forEach((element) => {
            element.setAttribute('aria-pressed', 'false');
        });

        // アクティブなボタンのaria-pressed属性をtrueに設定
        btnToActive.setAttribute('aria-pressed', 'true');
        // アクティブなテーマのアイコンを現在のテーマアイコンにコピー
        activeThemeIcon.classList = svgOfActiveBtn;
        // アクセシビリティ用のラベルを更新
        const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`;
        themeSwitcher.setAttribute('aria-label', themeSwitcherLabel);

        // フォーカスが必要な場合はテーマ切り替えボタンにフォーカスを当てる
        if (focus) {
            themeSwitcher.focus();
        }
    };

    /**
     * テーマに応じてロゴを切り替え
     * ライトモードの場合はライト用ロゴを表示し、ダークモードの場合はダーク用ロゴを表示
     * @param {string} theme - 適用するテーマ（'light' または 'dark'）
     */
    const toggleLogo = (theme) => {
        if (theme === 'light') {
            // ライトモード: ダーク用ロゴを非表示、ライト用ロゴを表示
            document.getElementById('logo_dark').classList.add('d-none');
            document.getElementById('logo_dark').classList.remove('d-inline-block');
            document.getElementById('logo_light').classList.remove('d-none');
            document.getElementById('logo_light').classList.add('d-inline-block');
        } else {
            // ダークモード: ライト用ロゴを非表示、ダーク用ロゴを表示
            document.getElementById('logo_light').classList.add('d-none');
            document.getElementById('logo_light').classList.remove('d-inline-block');
            document.getElementById('logo_dark').classList.remove('d-none');
            document.getElementById('logo_dark').classList.add('d-inline-block');
        }
    };

    // システムのカラースキーム設定が変更されたときのイベントリスナー
    // 'auto'モードが選択されている場合のみ、システム設定の変更に追従
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        const storedTheme = getStoredTheme();
        // 'auto'モードの場合（'light'でも'dark'でもない場合）のみ、システム設定に追従
        if (storedTheme !== 'light' && storedTheme !== 'dark') {
            setTheme(getPreferredTheme());
            toggleLogo(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        }
    });

    // DOMの読み込み完了後に初期化処理を実行
    window.addEventListener('DOMContentLoaded', () => {
        // アクティブなテーマをUIに表示
        showActiveTheme(getPreferredTheme());
        // ロゴを現在のテーマに合わせて切り替え
        toggleLogo(getPreferredTheme());

        // すべてのテーマ切り替えボタンにクリックイベントリスナーを追加
        document.querySelectorAll('[data-bs-theme-value]').forEach((toggle) => {
            toggle.addEventListener('click', () => {
                const theme = toggle.getAttribute('data-bs-theme-value');
                // 選択されたテーマを保存
                setStoredTheme(theme);
                // テーマを適用
                setTheme(theme);
                // UIを更新（フォーカスも設定）
                showActiveTheme(theme, true);
                // ロゴを切り替え
                toggleLogo(theme);
            });
        });
    });
})();
