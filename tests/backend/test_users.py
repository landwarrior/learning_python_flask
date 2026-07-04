"""GET /users エンドポイントのテスト."""

from datetime import date
from types import SimpleNamespace
from unittest.mock import patch


def _make_user(**kwargs):
    defaults = {
        "user_id": "abe_masami",
        "user_name": "阿部 まさみ",
        "user_name_kana": "あべ まさみ",
        "email": "abe_masami@example.com",
        "gender": "女",
        "age": 58,
        "birth_day": date(1965, 6, 8),
        "blood_type": "AB型",
        "prefecture": "群馬県",
        "curry": "手前ルー・ルー攻め派",
        "total": 1,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


@patch("apis.users.mst_user.get_data")
def test_get_users_returns_200_with_empty_list(mock_get_data, client):
    """ユーザーが存在しない場合、空の一覧を返す."""
    mock_get_data.return_value = iter([])

    response = client.get("/users")

    assert response.status_code == 200
    body = response.get_json()
    assert body["code"] == 200
    assert body["total"] == 0
    assert body["offset"] == 0
    assert body["limit"] == 1000
    assert body["data"] == []


@patch("apis.users.mst_user.get_data")
def test_get_users_returns_user_data(mock_get_data, client):
    """ユーザーデータを正しい形式で返す."""
    mock_get_data.return_value = iter([_make_user()])

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


@patch("apis.users.mst_user.get_data")
def test_get_users_passes_offset_and_limit(mock_get_data, client):
    """offset と limit クエリパラメータをリポジトリに渡す."""
    mock_get_data.return_value = iter([])

    client.get("/users?offset=10&limit=5")

    mock_get_data.assert_called_once()
    _, _, offset, limit, condition = mock_get_data.call_args[0]
    assert offset == 10
    assert limit == 5
    assert condition is None


@patch("apis.users.mst_user.get_data")
def test_get_users_passes_filter_condition(mock_get_data, client):
    """検索条件クエリパラメータをリポジトリに渡す."""
    mock_get_data.return_value = iter([])

    client.get("/users?user_name=阿部&age=58")

    _, _, _, _, condition = mock_get_data.call_args[0]
    assert condition == {"user_name": "阿部", "age": 58}


@patch("apis.users.mst_user.get_data")
def test_get_users_passes_birth_day_range_condition(mock_get_data, client):
    """生年月日の範囲検索条件をリポジトリに渡す."""
    mock_get_data.return_value = iter([])

    client.get("/users?birth_day_from=19650101&birth_day_to=19701231")

    _, _, _, _, condition = mock_get_data.call_args[0]
    assert condition == {
        "birth_day_from": date(1965, 1, 1),
        "birth_day_to": date(1970, 12, 31),
    }


def test_get_users_invalid_birth_day_returns_400(client):
    """不正な生年月日パラメータの場合は 400 を返す."""
    response = client.get("/users?birth_day=invalid")

    assert response.status_code == 400
    body = response.get_json()
    assert body["code"] == 400
    assert "message" in body
