document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', () => {
        const button = loginForm.querySelector('button[type="submit"]');
        button.disabled = true;
        button.innerHTML = '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> ログイン';
    });
});
