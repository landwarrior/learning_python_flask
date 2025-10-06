import js from '@eslint/js';
import globals from 'globals';

// 共通のルール定義
const commonRules = {
    // === 基本的なエラー・警告設定 ===
    // 未使用の変数・関数・パラメータをエラーとして表示する
    'no-unused-vars': 'error',
    // console.log、console.warn 等の使用を警告として表示する（本番環境では不適切なため）
    'no-console': 'warn',
    // 宣言されていない変数や関数が使用されたらエラーとして表示する
    'no-undef': 'error',
    // グローバル変数（ window, document 等）への再代入をエラーとして表示する
    'no-global-assign': 'error',

    // === コードスタイル・フォーマット ===
    // セミコロンが使用されていない場合にエラーとして表示する（Prettier による自動フォーマットで問題なくなるはず）
    semi: 'error',
    // クォートの種類（シングル/ダブル）をチェックする設定だが、 Prettier による自動フォーマットがあるので off にする
    quotes: 'off',
    // インデント（スペース/タブ、数）をチェックする設定だが、 Prettier による自動フォーマットがあるので off にする
    indent: 'off',
    // 行末の不要な空白をチェックする設定だが、 Prettier による自動フォーマットがあるので off にする
    'no-trailing-spaces': 'off',
    // ファイル末尾の改行の有無をチェックする設定だが、 VSCode 標準の自動フォーマットがあるので off にする
    'eol-last': 'off',
    // オブジェクト等の末尾のカンマを必須あるいは禁止にする設定だが、 Prettier による自動フォーマットがあるので off にする
    'comma-dangle': 'off',
    // 行の最大文字数をチェックする設定だが、 Prettier による自動フォーマットがあるので off にする
    'max-len': 'off',

    // === アロー関数・関数関連 ===
    // アロー関数の本体のスタイルを統一する（デフォルトでは可能な限り波括弧を省略する）
    'arrow-body-style': 'error',
    // アロー関数の引数の括弧の使用を統一する（デフォルトでは常に括弧を使用）
    'arrow-parens': 'error',
    // アロー関数の矢印（=>）の前後のスペースを統一する（デフォルトでは前後両方にスペースを配置）
    'arrow-spacing': 'error',
    // argumentsオブジェクトの代わりにrestパラメータの使用を推奨し、 arguments が使用されていればエラーとして表示する
    'prefer-rest-params': 'error',
    // apply()の代わりにスプレッド構文 (...) の使用を推奨し、 apply() が使用されていればエラーとして表示する
    'prefer-spread': 'error',

    // === ジェネレーター・イテレーター ===
    // ジェネレーター関数 function* の * の配置スタイルを統一する（デフォルトでは * の前後両方にスペースを配置）
    'generator-star-spacing': 'error',
    // yield* の * の配置スタイルを統一する（デフォルトでは * の前後両方にスペースを配置）
    'yield-star-spacing': 'error',

    // === インポート・エクスポート ===
    // 同じモジュールからの重複する import 文があればエラーとして表示する
    'no-duplicate-imports': 'error',
    // 同じ名前への不要な名前変更（例: import { foo as foo } ）を禁止し、不要な名前変更があればエラーとして表示する
    'no-useless-rename': 'error',

    // === オブジェクト・クラス ===
    // 不要な計算プロパティキー（例: { ['a']: 1 } を { a: 1 } にすべき）を禁止し、不要な計算プロパティがあればエラーとして表示する
    'no-useless-computed-key': 'error',
    // 不要なコンストラクタ（空のコンストラクタ等）を禁止し、不要なコンストラクタがあればエラーとして表示する
    'no-useless-constructor': 'error',

    // === 変数宣言・スコープ ===
    // 再代入されない変数は const を使用することを強制し、 let/var が使用されていればエラーとして表示する
    'prefer-const': 'error',

    // === テンプレートリテラル・演算子 ===
    // スプレッド/restパラメータの ... の後ろのスペースを統一する（デフォルトではスペースを入れない）
    'rest-spread-spacing': 'error',
    // テンプレートリテラルの ${} 内側のスペースを統一する（デフォルトではスペースを入れない）
    'template-curly-spacing': 'error',
};

// 共通のグローバル変数定義
const commonGlobals = {
    ...globals.browser,
    ...globals.es2022,
    bootstrap: 'readonly',
    Vue: 'readonly',
    axios: 'readonly',
    flatpickr: 'readonly',
};

export default [
    js.configs.recommended,
    // alertShow.js: グローバル関数を定義するファイル
    {
        files: ['src/frontend/static/assets/js/alertShow.js'],
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: 'script',
            globals: commonGlobals,
        },
        rules: {
            ...commonRules,
            // このファイルはグローバル関数を定義するため、 no-implicit-globals をオフにする
            'no-implicit-globals': 'off',
        },
    },
    // その他の JS ファイル: グローバル関数を使用するファイル
    {
        files: ['src/**/*.js'],
        ignores: ['src/frontend/static/assets/js/alertShow.js'],
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: 'script',
            globals: {
                ...commonGlobals,
                showAlert: 'readonly',
            },
        },
        rules: {
            ...commonRules,
            // 暗黙的にグローバル変数を作成した際にエラーとして表示する
            'no-implicit-globals': 'error',
        },
    },
    {
        ignores: ['node_modules/**', 'dist/**', 'build/**', '*.min.js'],
    },
];
