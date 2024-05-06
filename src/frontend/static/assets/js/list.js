import userListResultComp from './userListResultComp.js';

document.addEventListener('DOMContentLoaded', () => {
    Vue.createApp({
        data() {
            return {
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
                result_items: [],
            };
        },
        methods: {
            search() {
                const cond_param = {};
                for (const item of this.search_items) {
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
                        console.log(error);
                    });
            },
        },
        components: {
            userListResultComp,
        },
        // デリミタを、ES6 テンプレートの文字列スタイルに変更する。
        delimiters: ['${', '}'],
    }).mount('#list_hoge');
    // こっちはドキュメントに載ってたのにうまく使えない
    // app.config.compilerOptions.delimiters = ['${', '}'];

    // flatpickr のクリアボタンは bootstrap と Bing での回答の合わせ技
    flatpickr('#birth_day_from', {
        dateFormat: 'Y/m/d',
        locale: 'ja',
        onReady: (_, __, instance) => {
            instance.input.parentNode.querySelector('button').addEventListener('click', function () {
                instance.clear();
            });
        },
    });
    flatpickr('#birth_day_to', {
        dateFormat: 'Y/m/d',
        locale: 'ja',
        onReady: (_, __, instance) => {
            instance.input.parentNode.querySelector('button').addEventListener('click', function () {
                instance.clear();
            });
        },
    });
});
