module.exports = app => {
    const posts = require("../controllers/post.controller.js");
      
    // Create a new comment
    app.post("/posts", posts.create);
  
    // Retrieve all comments
    app.get("/posts", posts.findAll);
  
    // Retrieve all occurances of that ticker 
    app.get("/posts/:ticker", posts.getTicker);
  
    // Retrieve range of comments by ticker and date
    app.get("/posts/:ticker/:frontDate/:backDate", posts.tickerDate); 

    // Retrieve comment by commend ID
    app.get("/id/:postID", posts.postID);
  };