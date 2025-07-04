import csv
import io

from flask import Blueprint, send_file

csv_bp = Blueprint("csv", __name__)


@csv_bp.route("/download-csv", methods=["GET"])
def download_csv():
    # メモリ上にCSVデータを作成
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator="\r\n")

    # ヘッダー行を書き込み
    writer.writerow(["test1", "test2", "test3", "test4"])

    # StringIOの内容を取得
    csv_data = output.getvalue()

    # Shift_JISにエンコード
    encoded_data = csv_data.encode("shift_jis")

    return send_file(
        io.BytesIO(encoded_data),
        mimetype="text/csv",
        as_attachment=True,
        download_name="output.csv",
        charset="shift_jis",
    )
