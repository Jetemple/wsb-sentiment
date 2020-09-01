module.exports = app => {
    const comments = require("../controllers/comment.controller.js");
  
    // Create a new comment
    app.post("/comments", comments.create);
  
    // Retrieve all comments
    app.get("/comments", comments.findAll);
  
    // Retrieve all occurances of that ticker 
    app.get("/comments/:ticker", comments.getTicker);
  
    // Retrieve range of comments by ticker and date
    app.get("/comments/:ticker/:frontDate/:backDate", comments.tickerDate); 

    // Retrieve comment by commend ID
    app.get("/id/:postID", comments.postID);
  };