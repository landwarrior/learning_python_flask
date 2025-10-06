/* exported showAlert */
/**
 * アラート表示する
 * @param {HTMLElement} parentNode 親要素
 * @param {string} type アラートのタイプ。 primary, secondary, success, danger, warning, info, light, dark から選択。
 * @param {string} message 表示するメッセージ
 * @param {number} hiddenTime 表示を消すまでの時間（ミリ秒）
 */
function showAlert(parentNode, type, message, hiddenTime) {
    const wrapper = document.createElement('div');
    const id = `alert-${Date.now()}`;
    wrapper.setAttribute('id', id);
    wrapper.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
    wrapper.setAttribute('role', 'alert');
    let icon = '';
    if (type === 'danger' || type === 'warning') {
        icon = '<i class="bi bi-exclamation-triangle"></i> ';
    } else if (type === 'info') {
        icon = '<i class="bi bi-info-circle"></i> ';
    } else if (type === 'success') {
        icon = '<i class="bi bi-check-circle"></i> ';
    }
    wrapper.innerHTML = `<div>${icon} ${message}</div><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;
    parentNode.append(wrapper);

    const autoClose = (targetId) => {
        const alert = new bootstrap.Alert(`#${targetId}`);
        alert.close();
    };
    // append した後に DOM として認識できるので、ここで改めて取得する
    setTimeout(function () {
        autoClose(id);
    }, hiddenTime);
}
