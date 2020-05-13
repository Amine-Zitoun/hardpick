const express = require("express");
const router = express.Router();

router.post("/", (req, res) => {
    console.log(req.body)
    const price = req.body.price;
    const region = req.body.region;
    if (!(price) && !(region)) {
        res.render("index.ejs", {errorMessage: "Please enter your country and budget"})
    } else if (region == undefined) {
        res.render("index.ejs", {errorMessage: "Please select your country"})
    } else if (!price) {
        res.render("index.ejs", {errorMessage: "Please enter your budget"})
    } else {
        
    }
})

module.exports = router;