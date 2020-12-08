const sql = require("./db.js");

// constructor

const Ticker = function(ticker) {
  this.symbol = ticker.symbol;
  this.comment_id = ticker.comment_id;
};


Ticker.create = (newPost, result) => {
  sql.query("INSERT IGNORE INTO tickers SET ?", newPost, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    console.log("created comment: ", { id: res.insertId, ...newPost });
    result(null, { id: res.insertId, ...newPost });
  });
};

Ticker.findByTicker = (ticker, result) => {
  sql.query(`SELECT * FROM tickers WHERE ticker = "${ticker}"`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      console.log("found comment: ", res);
      result(null, res);
      return;
    }

    // not found Comment with the id
    result({ kind: "not_found" }, null);
  });
};

Ticker.tickerCount = (result) => {
  sql.query(`SELECT symbol, COUNT(symbol) AS count FROM tickers t GROUP BY symbol ORDER BY count DESC`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      console.log("found comment: ", res);
      result(null, res);
      return;
    }

    // not found Comment with the id
    result({ kind: "not_found" }, null);
  });
};


Ticker.getAll = result => {
  sql.query("SELECT * FROM tickers", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log("post: ", res);
    result(null, res);
  });
};


module.exports = Ticker;
