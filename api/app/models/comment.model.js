const sql = require("./db.js");

// constructor
const Comment = function(comment) {
  this.comment_id = comment.comment_id;
  this.comment_date = comment.comment_date;
  this.ticker = comment.ticker;
  this.parent_post = comment.parent_post;
  this.body = comment.body;
  this.sentiment = comment.sentiment;
  this.score = comment.score;
};


Comment.create = (newCustomer, result) => {
  sql.query("INSERT INTO comments SET ?", newCustomer, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    console.log("created comment: ", { id: res.insertId, ...newCustomer });
    result(null, { id: res.insertId, ...newCustomer });
  });
};

Comment.findByTicker = (customerId, result) => {
  sql.query(`SELECT * FROM comments WHERE ticker = "${customerId}"`, (err, res) => {
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
  sql.query(`SELECT * FROM comments WHERE ticker = "${ticker}" AND comment_date BETWEEN ${frontDate} AND ${backDate}`, (err, res) => {
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

Comment.updateById = (id, comment, result) => {
  sql.query(
    "UPDATE comments SET email = ?, name = ?, active = ? WHERE id = ?",
    [comment.email, comment.name, comment.active, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found Comment with the id
        result({ kind: "not_found" }, null);
        return;
      }

      console.log("updated comment: ", { id: id, ...comment });
      result(null, { id: id, ...comment });
    }
  );
};

Comment.remove = (id, result) => {
  sql.query("DELETE FROM comments WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found Comment with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted comment with id: ", id);
    result(null, res);
  });
};

Comment.removeAll = result => {
  sql.query("DELETE FROM comments", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} comments`);
    result(null, res);
  });
};

module.exports = Comment;
