"""
Provides an API for accessing quotes.
"""
from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from werkzeug.exceptions import BadRequest
from ..db.datahandler import DataHandler
from ..configs import URI

db = SQLAlchemy()
app = Flask(__name__)
Compress(app)  # add gzip compress middleware

app.config["SQLALCHEMY_DATABASE_URI"] = URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
app.json.compact = True  # type: ignore [attr-defined]


# TODO add response LRU caching
@app.route("/quotes", methods=["GET"])
def get_quotes() -> Response:
    """
    Get 1Inch quotes.

    Parameters
    ----------
    start : int
        The start timestamp to get quotes for.
    end : int
        The end timestamp to get quotes for.
    tokens : str | None, default=None
        Comma-separated string of token addresses to get quotes for.
        All pairwise permutations of the provided tokens will be fetched.
        If not provided, all token pairs are returned.
    cols : str | None, default=None
        Comma-separated string of columns to return.
        If not provided, the following are returned:
        [`src`, `dst`, `in_amount`, `out_amount`, `price`, `price_impact`, `timestamp`].
    process : bool, default=True
        Whether to process the quotes. If processed, the returned quotes
        will be grouped by `hour` and a `price_impact` column will be added.
        Refer to :func:`src.db.datahandler.DataHandler.process_quotes`.
    include-ref-price : bool, default=False
        Whether to include the inferred reference price for the
        price impact calc.

    Returns
    -------
    flask.wrappers.Response
        The quotes.
    """
    start = request.args.get("start", type=int)
    end = request.args.get("end", type=int)
    tokens_raw = request.args.get("tokens", type=str)
    cols_raw = request.args.get("cols", type=str)
    process = request.args.get("process", True, type=bool)
    include_ref_price = request.args.get("include-ref-price", False, type=bool)

    if not start or not end:
        raise BadRequest("start and end must be provided.")

    tokens = tokens_raw.split(",") if tokens_raw else None
    cols = cols_raw.split(",") if cols_raw else None

    with DataHandler() as datahandler:
        try:
            return jsonify(
                datahandler.get_quotes(
                    tokens,
                    start,
                    end,
                    cols=cols,
                    process=process,
                    include_ref_price=include_ref_price,
                )
                .reset_index()
                .to_dict(orient="records")
            )  # TODO better json structure to minimize duplication
        except Exception as e:  # pylint: disable=broad-except
            return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
