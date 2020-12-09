const Ticker = require("../models/ticker.model.js");

// Create and Save a new Comment
exports.create = (req, res) => {
  // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  // Create a Post
  const ticker = new Ticker({
    source_id: req.body.source_id,
    ticker: req.body.ticker,
  });

  // Save Comment in the database
  Ticker.create(req.params.source, ticker, (err, data) => {
    if (err)
      res.status(500).send({
        message:
          "Some error occurred while creating the ticker."
          // err.message || "Some error occurred while creating the Post."
      });
    else res.send(data);
  });
};

// Retrieve all ticker entries from the database.
exports.findAll = (req, res) => {
  Ticker.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving tickers."
      });
    else res.send(data);
  });
};

// Find a single Comment with a ticker
exports.getTicker = (req, res) => {
    Ticker.findByTicker(req.params.ticker, (err, data) => {
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

// Get count of all tickers in decending order
exports.tickerCount = (req, res) => {
  Ticker.tickerCount((err, data) => {
  if (err) {
    if (err.kind === "not_found") {
      res.status(404).send({
        message: `No posts of ${req.params.ticker}.`
      });
    } else {
      res.status(500).send({
        message: "Error Retrieveing Ticker count" + req.params.ticker
      });
    }
  } else res.send(data);
});
};



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

