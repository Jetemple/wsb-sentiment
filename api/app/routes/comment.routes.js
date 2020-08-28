module.exports = app => {
    const comments = require("../controllers/comment.controller.js");
  
    // Create a new Customer
    app.post("/comments", comments.create);
  
    // Retrieve all comments
    app.get("/comments", comments.findAll);
  
    // Retrieve all occurances of that ticker 
    app.get("/comments/:ticker", comments.getTicker);
  
    // Update a Customer with customerId
    app.put("/comments/:customerId", comments.update);
  
    // Delete a Customer with customerId
    app.delete("/comments/:customerId", comments.delete);
  
    // Create a new Customer
    app.delete("/comments", comments.deleteAll);
    
    // get range of comments by ticker and date
    app.get("/comments/:ticker/:frontDate/:backDate", comments.tickerDate); 
    // get range of comments by ticker and date
    app.get("/id/:postID", comments.postID);
  };