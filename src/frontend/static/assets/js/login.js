// ページの読み込みが完了したら実行
document.addEventListener('DOMContentLoaded', () => {
    // ログインフォーム要素を取得
    const loginForm = document.getElementById('login-form');

    // フォーム送信時のイベントリスナーを設定
    loginForm.addEventListener('submit', () => {
        // 送信ボタンを取得
        const button = loginForm.querySelector('button[type="submit"]');

        // ボタンを無効化（二重送信を防止）
        button.disabled = true;

        // ボタンのテキストをスピナー付きのローディング表示に変更
        button.innerHTML = '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> ログイン';
    });
});
