import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    files: ['static/js/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'script',
      globals: {
        // ブラウザ環境のグローバル変数
        window: 'readonly',
        document: 'readonly',
        console: 'readonly',
        fetch: 'readonly',
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        setInterval: 'readonly',
        clearInterval: 'readonly',
        alert: 'readonly',
        confirm: 'readonly',
        prompt: 'readonly',
        localStorage: 'readonly',
        sessionStorage: 'readonly',
        location: 'readonly',
        history: 'readonly',
        navigator: 'readonly',
        screen: 'readonly',
        // DOM要素
        Element: 'readonly',
        HTMLElement: 'readonly',
        HTMLInputElement: 'readonly',
        HTMLButtonElement: 'readonly',
        HTMLFormElement: 'readonly',
        Event: 'readonly',
        EventTarget: 'readonly',
        // JSON
        JSON: 'readonly',
        // その他
        parseInt: 'readonly',
        parseFloat: 'readonly',
        isNaN: 'readonly',
        isFinite: 'readonly',
        encodeURIComponent: 'readonly',
        decodeURIComponent: 'readonly',
        encodeURI: 'readonly',
        decodeURI: 'readonly',
      },
    },
    rules: {
      // 基本的なルール設定
      'no-unused-vars': 'warn',
      'no-console': 'off',
      // Prettierと競合するルールは無効化
      semi: 'off',
      quotes: 'off',
      indent: 'off',
      'no-trailing-spaces': 'off',
      'eol-last': 'off',
      'comma-dangle': 'off',
      'max-len': 'off',
      // ブラウザ環境特有のルール
      'no-undef': 'error',
      'no-global-assign': 'error',
      'no-implicit-globals': 'error',
    },
  },
  {
    ignores: ['node_modules/**', 'dist/**', 'build/**', '*.min.js'],
  },
];
