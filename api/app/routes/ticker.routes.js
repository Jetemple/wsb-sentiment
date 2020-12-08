module.exports = app => {
    const tickers = require("../controllers/ticker.controller.js");


    //Create a new ticker entry
    app.post("/tickers", tickers.create);

    //Get all tickers
    app.get("/tickers", tickers.findAll);

    //Gets count of all tickers
    app.get("/tickers/count", tickers.tickerCount)
};