const Comment = require("../models/comment.model.js");

// Create and Save a new Comment
exports.create = (req, res) => {
  // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  // Create a Comment
  const comment = new Comment({
    comment_id: req.body.comment_id,
    comment_date: req.body.comment_date,
    ticker: req.body.ticker,
    parent_post: req.body.parent_post,
    parent_comment: req.body.parent_comment,
    body: req.body.body,
    score: req.body.score,
    sentiment: req.body.sentiment,
    author: req.body.author
    
    // charset : 'utf8mb4'
  });

  // Save Comment in the database
  Comment.create(comment, (err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Comment."
      });
    else res.send(data);
  });
};

// Retrieve all Comments from the database.
exports.findAll = (req, res) => {
  Comment.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving comments."
      });
    else res.send(data);
  });
};

// Find all comments that contain ticker
exports.getTicker = (req, res) => {
  Comment.findByTicker(req.params.ticker, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `No comments of ${req.params.ticker}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving comments with the ticker " + req.params.ticker
        });
      }
    } else res.send(data);
  });
};


// Find all comments that contain ticker
exports.allPostComments = (req, res) => {
  Comment.allPostComments(req.params.postID, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `No comments of ${req.params.ticker}.`
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

