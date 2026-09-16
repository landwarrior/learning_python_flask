"""mylogger のマスク処理テスト."""

import logging

from mylogger import MASK, MaskingFilter, mask_message, mask_sensitive


def test_mask_sensitive_masks_password_keys():
    """機密キーの値をマスクし、それ以外は残す."""
    payload = {
        "login_id": "user01",
        "ignition_key": "plain-secret",
        "old_password": "old",
        "new_password": "new",
    }

    masked = mask_sensitive(payload)

    assert masked == {
        "login_id": "user01",
        "ignition_key": MASK,
        "old_password": MASK,
        "new_password": MASK,
    }


def test_mask_sensitive_does_not_mutate_original():
    """元の dict は変更しない."""
    payload = {"ignition_key": "plain-secret", "login_id": "user01"}

    mask_sensitive(payload)

    assert payload["ignition_key"] == "plain-secret"


def test_mask_sensitive_masks_nested_and_list_values():
    """ネストした dict と list も再帰的にマスクする."""
    payload = {
        "users": [
            {"user_id": "user01", "password": "secret"},
            {"user_id": "user02", "token": "abc"},
        ],
        "meta": {"csrf_token": "csrf-value"},
    }

    masked = mask_sensitive(payload)

    assert masked == {
        "users": [
            {"user_id": "user01", "password": MASK},
            {"user_id": "user02", "token": MASK},
        ],
        "meta": {"csrf_token": MASK},
    }


def test_mask_sensitive_masks_header_keys_case_insensitively():
    """ヘッダ名は大文字小文字を区別せずマスクする."""
    headers = {
        "Host": "example.local",
        "Cookie": "session=abc; csrf_token=def",
        "Authorization": "Bearer xyz",
        "Set-Cookie": "session=abc",
    }

    masked = mask_sensitive(headers)

    assert masked == {
        "Host": "example.local",
        "Cookie": MASK,
        "Authorization": MASK,
        "Set-Cookie": MASK,
    }


def test_mask_message_masks_python_dict_repr():
    """f-string で埋め込んだ dict 文字列からも機密値を消す."""
    message = "DATA: {'login_id': 'user01', 'ignition_key': 'plain-secret'}"

    masked = mask_message(message)

    assert "plain-secret" not in masked
    assert "user01" in masked
    assert f"'ignition_key': '{MASK}'" in masked


def test_mask_message_masks_json_and_header_strings():
    """JSON とヘッダ形式の文字列からも機密値を消す."""
    message = (
        '[DATA] {"password": "plain-secret"} '
        "[HEADER] Host: example.local, Cookie: session=abc, Authorization: Bearer xyz"
    )

    masked = mask_message(message)

    assert "plain-secret" not in masked
    assert "session=abc" not in masked
    assert "Bearer xyz" not in masked
    assert "example.local" in masked
    assert f'"password": "{MASK}"' in masked
    assert f"Cookie: {MASK}" in masked
    assert f"Authorization: {MASK}" in masked


def test_masking_filter_masks_completed_log_record():
    """Filter は完成済みメッセージをマスクし、出力は抑制しない."""
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="DATA: {'ignition_key': 'plain-secret', 'login_id': 'user01'}",
        args=(),
        exc_info=None,
    )

    keep = MaskingFilter().filter(record)

    assert keep is True
    assert "plain-secret" not in record.getMessage()
    assert "user01" in record.getMessage()
    assert MASK in record.getMessage()
