module.exports = app => {
    const posts = require("../controllers/post.controller.js");
    const comments = require("../controllers/comment.controller.js");
      
    // Create a new post
    app.post("/posts", posts.create);
  
    // Retrieve all post
    app.get("/posts", posts.findAll);
  
    // Retrieve all posts that use that ticker 
    app.get("/posts/:ticker", posts.getTicker);
  
    // Retrieve range of posts by ticker and date
    app.get("/posts/:ticker/:frontDate/:backDate", posts.tickerDate); 

    // Retrieve post by post ID
    app.get("/posts/id/:postID", posts.postID);

    // Retrieve all comments from PostID 
    app.get("/posts/comments/:postID", comments.allPostComments);
  };