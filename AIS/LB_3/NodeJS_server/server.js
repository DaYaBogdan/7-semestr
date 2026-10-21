const express = require("express");
const app = express();

app.get("/", (req, res) => {
    res.type("text/plain").send("Hello world from NodeJS");
});

app.listen(8002, "127.0.0.1", () => {
    console.log("Server running at http://127.0.0.1:8002/");
});