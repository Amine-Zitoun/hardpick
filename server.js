if (process.env.NODE_ENV !== "production") {
    require("dotenv").config();
}

const express = require("express");
const expressLayouts = require("express-ejs-layouts");
const bodyParser = require("body-parser");
const cors = require("cors");
const session = require("express-session");
const mongoose = require("mongoose");
const MongoStore = require("connect-mongo")(session);

const app = express();

const dbString = process.env.URI;
const dbOptions = {
    useNewUrlParser: true,
    useUnifiedTopology: true
}
const connection = mongoose.createConnection(dbString, dbOptions);

const sessionStore= new MongoStore({
    mongooseConnection: connection,
    collection: "sessions"
});
app.set("view engine", "ejs")
app.set("views", __dirname + "/views")
app.set("layout", "layouts/layout")
app.use(expressLayouts)
app.use(express.static("public"))
app.use(cors())
app.use(bodyParser.urlencoded({extended: true}))
app.use(bodyParser.json());
app.use(session({
    secret: process.env.SECRET,
    resave: false,
    saveUninitialized: true,
    store: sessionStore,
    cookie: {
        maxAge: 1000 * 60 * 60 * 24 * 14
    }
}))

const indexRouter = require("./routes/index");
const searchRouter = require("./routes/search");
app.use("/", indexRouter)
app.use("/search", searchRouter)


app.listen(process.env.PORT || 3000)