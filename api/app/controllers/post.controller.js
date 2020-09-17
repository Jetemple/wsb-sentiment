const Post = require("../models/post.model.js");

// Create and Save a new Comment
exports.create = (req, res) => {
  // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  // Create a Post
  const post = new Post({
    post_id: req.body.post_id,
    post_date: req.body.post_date,
    num_comments: req.body.num_comments,
    score: req.body.score,
    upvote_ratio: req.body.upvote_ratio,
    guildings: req.body.guildings,
    flair: req.body.flair,
    ticker: req.body.ticker,
    body: req.body.body,
    sentiment: req.body.sentiment,
    // charset : 'utf8mb4'
  });

  // Save Comment in the database
  Post.create(post, (err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Post."
      });
    else res.send(data);
  });
};

// Retrieve all Comments from the database.
exports.findAll = (req, res) => {
  Post.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving comments."
      });
    else res.send(data);
  });
};

// Find a single Comment with a ticker
exports.getTicker = (req, res) => {
    Post.findByTicker(req.params.ticker, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `No posts of ${req.params.ticker}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving comments with the ticker " + req.params.ticker
        });
      }
    } else res.send(data);
  });
};



exports.tickerDate = (req, res) => {
  Comment.tickerDateRange(req.params.ticker ,req.params.frontDate, req.params.backDate, (err, data) => {
    if (err) {
      if (err.kind === "none_in_date") {
        res.status(404).send({
          message: `No occurances of ${req.params.ticker} found in that range.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving comments with the ticker " + req.params.ticker
        });
      }
    } else res.send(data);
  })
}

exports.postID = (req, res) => {
  Comment.getID(req.params.postID, (err,data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `ID: ${req.params.postID} found in data.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving comments with the ticker " + req.params.ticker
        });
      }
    } else res.send(data);
  })
}

