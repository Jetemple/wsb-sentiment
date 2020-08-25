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
    body: req.body.body,
    sentiment: req.body.sentiment,
    score: req.body.comment_id,
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

// Find a single Comment with a customerId
exports.findOne = (req, res) => {
  Comment.findById(req.params.customerId, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Comment with id ${req.params.customerId}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Comment with id " + req.params.customerId
        });
      }
    } else res.send(data);
  });
};

// Update a Comment identified by the customerId in the request
exports.update = (req, res) => {
  // Validate Request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  console.log(req.body);

  Comment.updateById(
    req.params.customerId,
    new Comment(req.body),
    (err, data) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Not found Comment with id ${req.params.customerId}.`
          });
        } else {
          res.status(500).send({
            message: "Error updating Comment with id " + req.params.customerId
          });
        }
      } else res.send(data);
    }
  );
};

// Delete a Comment with the specified customerId in the request
exports.delete = (req, res) => {
  Comment.remove(req.params.customerId, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Comment with id ${req.params.customerId}.`
        });
      } else {
        res.status(500).send({
          message: "Could not delete Comment with id " + req.params.customerId
        });
      }
    } else res.send({ message: `Comment was deleted successfully!` });
  });
};

// Delete all Comments from the database.
exports.deleteAll = (req, res) => {
  Comment.removeAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all comments."
      });
    else res.send({ message: `All Comments were deleted successfully!` });
  });
};