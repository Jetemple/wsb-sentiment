module.exports = {
    HOST: process.env.HOST || "$HOSTNAME",
    USER: process.env.USER || "$USER",
    PASSWORD: process.env.PASSWORD || "$PASSWORD",
    PORT: process.env.PORT || "$PORT",
    DB: process.env.DB || "$DATABASE"
  };