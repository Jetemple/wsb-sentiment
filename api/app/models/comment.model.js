const sql = require("./db.js");

// constructor
const Comment = function(comment) {
  this.comment_id = comment.comment_id;
  this.comment_date = comment.comment_date;
  this.ticker = comment.ticker;
  this.parent_post = comment.parent_post;
  this.parent_comment = comment.parent_comment;
  this.body = comment.body;
  this.sentiment = comment.sentiment;
  this.score = comment.score;
  this.author = comment.author
};


Comment.create = (newComment, result) => {
  sql.query("INSERT INTO comments SET ?", newComment, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    console.log("created comment: ", { id: res.insertId, ...newComment });
    result(null, { id: res.insertId, ...newComment });
  });
};

Comment.findByTicker = (ticker, result) => {
  sql.query(`SELECT c.* FROM comments c INNER JOIN tickers t ON t.comment_id = c.comment_id WHERE t.symbol = "${ticker}"`, (err, res) => {
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


Comment.allPostComments = (post_id, result) => {
  sql.query(`SELECT c.* FROM comments c INNER JOIN posts p ON c.parent_post = p.post_id WHERE p.post_id = "${post_id}"`, (err, res) => {
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



Comment.tickerDateRange = (ticker, frontDate, backDate, result) => {
  sql.query(`SELECT c.* FROM comments c INNER JOIN tickers t ON t.comment_id = c.comment_id WHERE t.symbol = "${ticker}" AND t.comment_date BETWEEN ${frontDate} AND ${backDate}`, (err, res) => {
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
    result({ kind: "none_in_date" }, null);
  });
};

Comment.getID = (id, result) => {
  sql.query(`SELECT * FROM comments WHERE comment_id = "${id}"`, (err, res) => {
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

}

Comment.getAll = result => {
  sql.query("SELECT * FROM comments", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log("comments: ", res);
    result(null, res);
  });
};


module.exports = Comment;
