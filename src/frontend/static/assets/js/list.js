document.addEventListener('DOMContentLoaded', () => {
    Vue.createApp({
        data() {
            return {
                // 検索条件
                search_items: [
                    { id: 'user_id', value: '', label: '社員ID', type: 'text' },
                    { id: 'user_name', value: '', label: '社員名', type: 'text' },
                    { id: 'user_name_kana', value: '', label: '社員名カナ', type: 'text' },
                    { id: 'email', value: '', label: 'email', type: 'text' },
                    { id: 'birth_day_from', value: '', label: '生年月日FROM', type: 'date' },
                    { id: 'birth_day_to', value: '', label: '生年月日TO', type: 'date' },
                    { id: 'prefecture', value: '', label: '都道府県', type: 'text' },
                    { id: 'curry', value: '', label: 'カレーの食べ方', type: 'text' },
                ],
                // 検索条件の現在値
                search_current_items: [],
                // 検索結果
                result_items: [],
                // 検索中かどうか
                searching: false,
                // 選択中の社員
                focus_item: {},
                // ページング
                page: 1,
                per_page: 10,
                total: 0,
            };
        },
        methods: {
            search() {
                this.search_current_items = this.search_items;
                this.searching = true;
                this.execute_search();
            },
            search_current() {
                this.execute_search();
            },
            execute_search() {
                const cond_param = {};
                for (const item of this.search_current_items) {
                    if (item.value !== '' && item.type === 'date') {
                        cond_param[item.id] = item.value.replace(/\//g, '');
                    } else if (item.value !== '') {
                        cond_param[item.id] = item.value;
                    }
                }
                axios
                    .post('/users/api/list', cond_param)
                    .then((response) => {
                        this.result_items = response.data.data;
                    })
                    .catch(function (error) {
                        if (error.response.status === 500) {
                            console.log(error.response.data);
                            console.log(error.response.status);
                            console.log(error.response.headers);
                            const alertArea = document.getElementById('alert-area');
                            showAlert(alertArea, 'danger', 'サーバーエラーが発生しました。', 5000);
                        } else if (error.response.status === 400) {
                            console.log(error.response.data);
                            console.log(error.response.status);
                            console.log(error.response.headers);
                            const alertArea = document.getElementById('alert-area');
                            showAlert(alertArea, 'danger', '検索条件に誤りがあります。', 5000);
                        } else if (error.response.status === 401) {
                            console.log(error.response.data);
                            console.log(error.response.status);
                            console.log(error.response.headers);
                            const alertArea = document.getElementById('alert-area');
                            showAlert(alertArea, 'danger', 'セッションの有効期限が切れています。再ログインするか、ページを再読み込みしてください。', 5000);
                        } else {
                            console.log(error.response.data);
                            console.log(error.response.status);
                            console.log(error.response.headers);
                            const alertArea = document.getElementById('alert-area');
                            showAlert(alertArea, 'danger', 'データ取得に失敗しました。', 5000);
                        }
                    })
                    .finally(() => {
                        this.searching = false;
                    });
            },
            showModal(user_id) {
                for (const item of this.result_items) {
                    if (item.user_id === user_id) {
                        this.focus_item = item;
                        break;
                    }
                }
                const modalEl = document.getElementById('modal');
                const modal = new bootstrap.Modal(modalEl, {});
                modal.show();
            },
            clearInputValue(clearButton) {
                let parentDiv = '';
                if (clearButton.tagName.toLowerCase() === 'button') {
                    parentDiv = clearButton.parentNode;
                } else {
                    // i 要素がイベント元になっているので、2階層上がる
                    parentDiv = clearButton.parentNode.parentNode;
                }
                const inputElement = parentDiv.querySelector('.form-control');
                if (!parentDiv.classList.contains('flatpickr') && inputElement) {
                    // input要素が属するデータオブジェクト内の対応するプロパティを空にする
                    const inputId = inputElement.id;
                    for (const item of this.search_items) {
                        if (item.id === inputId) {
                            item.value = ''; // Vueのデータを更新
                            break;
                        }
                    }
                }
            },
            showTaost() {
                const toastElList = document.querySelectorAll('.toast');
                const toastList = [...toastElList].map((toastEl) => new bootstrap.Toast(toastEl, {}));
                for (const toast of toastList) {
                    toast.show();
                }
            },
            showAlert(msg) {
                const alertArea = document.getElementById('alert-area');
                showAlert(alertArea, 'danger', msg, 5000);
            },
            showAlert2() {
                const alertArea = document.getElementById('alert-area');
                showAlert(alertArea, 'primary', 'primary の動作確認', 5000);
            },
            showAlert3() {
                const alertArea = document.getElementById('alert-area');
                showAlert(alertArea, 'secondary', 'secondary の動作確認', 5000);
            },
            showAlert4() {
                const alertArea = document.getElementById('alert-area');
                showAlert(alertArea, 'info', 'info の動作確認', 5000);
            },
            showAlert5() {
                const alertArea = document.getElementById('alert-area');
                showAlert(alertArea, 'success', 'success の動作確認', 5000);
            },
            showAlert6() {
                const alertArea = document.getElementById('alert-area');
                showAlert(alertArea, 'warning', 'warning の動作確認', 5000);
            },
        },
        // デリミタを、ES6 テンプレートの文字列スタイルに変更する。
        delimiters: ['${', '}'],
    }).mount('#user_list');
    // こっちはドキュメントに載ってたのにうまく使えない（app は Vue.createApp の戻り値を受け取る変数）
    // app.config.compilerOptions.delimiters = ['${', '}'];

    // flatpickr のクリアボタンは bootstrap と Bing での回答の合わせ技
    flatpickr('#birth_day_from', {
        dateFormat: 'Y/m/d',
        locale: 'ja',
        onReady: (_, __, instance) => {
            // フローティングラベルにしたので親要素を2階層上がる必要がある
            instance.input.parentNode.parentNode.querySelector('button').addEventListener('click', function () {
                instance.clear();
            });
        },
    });
    flatpickr('#birth_day_to', {
        dateFormat: 'Y/m/d',
        locale: 'ja',
        onReady: (_, __, instance) => {
            // フローティングラベルにしたので親要素を2階層上がる必要がある
            instance.input.parentNode.parentNode.querySelector('button').addEventListener('click', function () {
                instance.clear();
            });
        },
    });
});
