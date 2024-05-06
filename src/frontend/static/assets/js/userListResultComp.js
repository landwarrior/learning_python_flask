export default {
    props: {
        // 呼び出し元から受け取るパラメータ。 template での利用方法は、 data で定義したパラメータと同じように利用する
        result_items: Array,
    },
    template: /*html*/ `
    <tr v-for="item in result_items">
      <td>{{ item.user_id }}</td>
      <td>{{ item.user_name }}</td>
      <td class="d-none d-lg-table-cell">{{ item.user_name_kana }}</td>
      <td class="d-none d-md-table-cell text-truncate">{{ item.email }}</td>
      <td class="d-none d-xl-table-cell">{{ item.gender }}</td>
      <td class="d-none d-md-table-cell">{{ item.age }}</td>
      <td class="d-none d-lg-table-cell">{{ item.blood_type }}</td>
      <td>{{ item.prefecture }}</td>
      <td class="d-none d-xl-table-cell text-truncate">{{ item.curry }}</td>
    </tr>
    `,
};
