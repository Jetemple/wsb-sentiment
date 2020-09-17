const sql = require("./db.js");

// constructor

const Post = function(post) {
  this.post_id = post.post_id;
  this.post_date = post.post_date;
  this.num_comments = post.num_comments;
  this.score = post.score;
  this.upvote_ratio = post.upvote_ratio;
  this.guildings = post.guildings;
  this.flair = post.flair;
  this.ticker = post.ticker;
  this.title = post.title;
  this.body = post.body;
  this.sentiment = post.sentiment;
  
};


Post.create = (newPost, result) => {
  sql.query("INSERT INTO posts SET ?", newPost, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    console.log("created comment: ", { id: res.insertId, ...newPost });
    result(null, { id: res.insertId, ...newPost });
  });
};

Post.findByTicker = (ticker, result) => {
  sql.query(`SELECT * FROM posts WHERE ticker = "${ticker}"`, (err, res) => {
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


Post.getID = (id, result) => {
  sql.query(`SELECT * FROM posts WHERE post_id = "${id}"`, (err, res) => {
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




Post.getAll = result => {
  sql.query("SELECT * FROM posts", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log("post: ", res);
    result(null, res);
  });
};


module.exports = Post;
