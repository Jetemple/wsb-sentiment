module.exports = app => {
    const tickers = require("../controllers/ticker.controller.js");


    //Create a new ticker_post entry
    app.post("/tickers/:source", tickers.create);

    // Create a new ticker_comment entry
    // app.post("/tickers/post", tickers.createPost);

    //Get all tickers
    app.get("/tickers", tickers.findAll);

    //Get specific tickers
    app.get("/tickers/:ticker", tickers.getTicker)

    //Gets count of all tickers
    app.get("/tickers/count", tickers.tickerCount)
};