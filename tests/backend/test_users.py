"""GET /users エンドポイントのテスト."""

from datetime import date

from conftest import insert_mst_user, insert_mst_users


def test_get_users_returns_200_with_empty_list(client):
    """ユーザーが存在しない場合、空の一覧を返す."""
    response = client.get("/users")

    assert response.status_code == 200
    body = response.get_json()
    assert body["code"] == 200
    assert body["total"] == 0
    assert body["offset"] == 0
    assert body["limit"] == 1000
    assert body["data"] == []


def test_get_users_returns_user_data(client, db):
    """ユーザーデータを正しい形式で返す."""
    insert_mst_user(db)
    response = client.get("/users")

    assert response.status_code == 200
    body = response.get_json()
    assert body["total"] == 1
    assert len(body["data"]) == 1
    assert body["data"][0] == {
        "user_id": "abe_masami",
        "user_name": "阿部 まさみ",
        "user_name_kana": "あべ まさみ",
        "email": "abe_masami@example.com",
        "gender": "女",
        "age": 58,
        "birth_day": "19650608",
        "blood_type": "AB型",
        "prefecture": "群馬県",
        "curry": "手前ルー・ルー攻め派",
    }


def test_get_users_passes_offset_and_limit(client, db):
    """offset と limit クエリパラメータでページングする."""
    insert_mst_users(
        db,
        [{"user_id": f"test_user_{i:02d}", "user_name": f"テスト {i:02d}"} for i in range(15)],
    )

    response = client.get("/users?offset=10&limit=5")

    assert response.status_code == 200
    body = response.get_json()
    assert body["total"] == 15
    assert body["offset"] == 10
    assert body["limit"] == 5
    assert len(body["data"]) == 5
    assert body["data"][0]["user_id"] == "test_user_10"
    assert body["data"][-1]["user_id"] == "test_user_14"


def test_get_users_passes_filter_condition(client, db):
    """検索条件クエリパラメータで絞り込む."""
    insert_mst_user(db)
    insert_mst_user(
        db,
        user_id="kumai_keita",
        user_name="熊井 慶太",
        user_name_kana="くまい けいた",
        email="kumai_keita@example.com",
        gender="男",
        age=43,
        birth_day=date(1980, 7, 6),
        blood_type="A型",
        prefecture="群馬県",
    )

    response = client.get("/users?user_name=阿部&age=58")

    assert response.status_code == 200
    body = response.get_json()
    assert body["total"] == 1
    assert len(body["data"]) == 1
    assert body["data"][0]["user_id"] == "abe_masami"


def test_get_users_passes_birth_day_range_condition(client, db):
    """生年月日の範囲検索条件で絞り込む."""
    insert_mst_user(db)
    insert_mst_user(
        db,
        user_id="kumai_keita",
        user_name="熊井 慶太",
        user_name_kana="くまい けいた",
        email="kumai_keita@example.com",
        gender="男",
        age=43,
        birth_day=date(1980, 7, 6),
        blood_type="A型",
        prefecture="群馬県",
    )

    response = client.get("/users?birth_day_from=19650101&birth_day_to=19701231")

    assert response.status_code == 200
    body = response.get_json()
    assert body["total"] == 1
    assert len(body["data"]) == 1
    assert body["data"][0]["user_id"] == "abe_masami"


def test_get_users_invalid_birth_day_returns_400(client):
    """不正な生年月日パラメータの場合は 400 を返す."""
    response = client.get("/users?birth_day=invalid")

    assert response.status_code == 400
    body = response.get_json()
    assert body["code"] == 400
    assert "message" in body
