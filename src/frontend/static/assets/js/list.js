document.addEventListener('DOMContentLoaded', () => {
    Vue.createApp({
        data() {
            return {
                search_items: [
                    { id: 'user_id', value: '', label: '社員ID' },
                    { id: 'user_name', value: '', label: '社員名' },
                    { id: 'user_name_kana', value: '', label: '社員名カナ' },
                    { id: 'email', value: '', label: 'email' },
                    { id: 'birth_day_from', value: '', label: '生年月日FROM' },
                    { id: 'birth_day_to', value: '', label: '生年月日TO' },
                    { id: 'prefecture', value: '', label: '都道府県' },
                    { id: 'curry', value: '', label: 'カレーの食べ方' },
                ],
            };
        },
        methods: {
            search() {
                axios
                    .post('/users/api/list')
                    .then((response) => {
                        console.log(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            },
        },
        // デリミタを、ES6 テンプレートの文字列スタイルに変更する。
        delimiters: ['${', '}'],
    }).mount('#search_body');
    // こっちはドキュメントに載ってたのにうまく使えない
    // app.config.compilerOptions.delimiters = ['${', '}'];

    flatpickr('#birth_day_from', { dateFormat: 'Y/m/d', locale: 'ja' });
    flatpickr('#birth_day_to', { dateFormat: 'Y/m/d', locale: 'ja' });
});
