const sql = require("./db.js");

// constructor

const Ticker = function(ticker) {
  this.ticker = ticker.ticker;
  this.source_id = ticker.source_id;
};


Ticker.create = (source ,newPost, result) => {
  if(source == "post" || source == "comment"){
    console.log("THE CONDITION WORKED")
    // sql.query(`INSERT INTO tickers SET ?`, newPost, (err, res) => {
    sql.query(`INSERT INTO tickers_${source}s SET ?`, newPost, (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(err, null);
        return;
      }
  
      console.log("created comment: ", { id: res.insertId, ...newPost });
      result(null, { id: res.insertId, ...newPost });
    });

  }
  else{
    return
  }
};

Ticker.findByTicker = (ticker, result) => {
  // sql.query(`SELECT * FROM tickers WHERE ticker = "${ticker}"`, (err, res) => {
  sql.query(`SELECT * FROM tickers_comments tc where ticker = "${ticker}" UNION SELECT * FROM tickers_posts tp where tp.ticker = "${ticker}"`, (err, res) => {
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
