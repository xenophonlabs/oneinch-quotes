"""
Provides an API for accessing quotes.
"""
from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from ..db.datahandler import DataHandler
from ..configs import URI

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/quotes", methods=["GET"])
def get_quotes() -> Response:
    """
    Get 1Inch quotes.

    Parameters
    ----------
    pair : tuple | None
        The pair to get quotes for. If not provided,
        all pairs are returned.
    start : int | None
        The start timestamp to get quotes for. If not provided,
        all quotes until `end` are returned.
    end : int | None
        The end timestamp to get quotes for. If not provided,
        all quotes from `start` are returned.
    cols : list | None
        The columns to return. If not provided, all columns are returned.
    process : bool
        Whether to process the quotes. If processed, the returned quotes
        will be grouped by `hour` and a `price_impact` column will be added.
        Refer to :func:`src.db.datahandler.DataHandler.process_quotes`.

    Returns
    -------
    flask.wrappers.Response
        The quotes.
    """
    pair = request.args.get("pair", type=tuple)
    start = request.args.get("start", type=int)
    end = request.args.get("end", type=int)
    cols = request.args.get("cols", type=list)
    process = request.args.get("process", True, type=bool)
    with DataHandler() as datahandler:
        try:
            return jsonify(
                datahandler.get_quotes(
                    pair, start, end, cols=cols, process=process
                ).to_dict(orient="records")
            )
        except Exception as e:  # pylint: disable=broad-except
            return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
