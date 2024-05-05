(() => {
    const collapseToggle = document.querySelectorAll('.collapse-toggle');

    // カードの展開と折りたたみのアイコンを変更する
    document.addEventListener('DOMContentLoaded', () => {
        collapseToggle.forEach((toggle) => {
            toggle.parentNode.parentNode.querySelector('.collapse').addEventListener('shown.bs.collapse', () => {
                toggle.querySelector('i').classList.toggle('bi-dash');
                toggle.querySelector('i').classList.toggle('bi-plus');
            });
            toggle.parentNode.parentNode.querySelector('.collapse').addEventListener('hidden.bs.collapse', () => {
                toggle.querySelector('i').classList.toggle('bi-dash');
                toggle.querySelector('i').classList.toggle('bi-plus');
            });
        });
    });
    // こっちは card-header の border を消すためのもの
    document.addEventListener('DOMContentLoaded', () => {
        collapseToggle.forEach((toggle) => {
            toggle.parentNode.parentNode.querySelector('.collapse').addEventListener('show.bs.collapse', () => {
                toggle.parentNode.classList.toggle('no-border');
            });
            toggle.parentNode.parentNode.querySelector('.collapse').addEventListener('hidden.bs.collapse', () => {
                toggle.parentNode.classList.toggle('no-border');
            });
        });
    });
})();
