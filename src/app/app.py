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
app.json.compact = True # type: ignore [attr-defined]


# TODO add response LRU caching
@app.route("/quotes", methods=["GET"])
def get_quotes() -> Response:
    """
    Get 1Inch quotes.

    Parameters
    ----------
    start : int
        The start timestamp to get quotes for. If not provided,
        all quotes until `end` are returned.
    end : int
        The end timestamp to get quotes for. If not provided,
        all quotes from `start` are returned.
    pair : tuple | None, default=None
        The pair to get quotes for. If not provided,
        all pairs are returned.
    cols : list | None, default=None
        The columns to return. If not provided, all columns are returned.
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
    pair = request.args.get("pair", type=tuple)
    cols = request.args.get("cols", type=list)
    process = request.args.get("process", True, type=bool)
    include_ref_price = request.args.get("include-ref-price", False, type=bool)
    
    if not start or not end:
        raise BadRequest("start and end must be provided.")

    with DataHandler() as datahandler:
        try:
            return jsonify(
                datahandler.get_quotes(
                    pair,
                    start,
                    end,
                    cols=cols,
                    process=process,
                    include_ref_price=include_ref_price,
                ).to_dict(orient="records")
            )
        except Exception as e:  # pylint: disable=broad-except
            return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
