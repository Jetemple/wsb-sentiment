module.exports = app => {
    const comments = require("../controllers/comment.controller.js");
  
    // Create a new Customer
    app.post("/comments", comments.create);
  
    // Retrieve all comments
    app.get("/comments", comments.findAll);
  
    // Retrieve a single Customer with customerId
    app.get("/comments/:customerId", comments.findOne);
  
    // Update a Customer with customerId
    app.put("/comments/:customerId", comments.update);
  
    // Delete a Customer with customerId
    app.delete("/comments/:customerId", comments.delete);
  
    // Create a new Customer
    app.delete("/comments", comments.deleteAll);
  };