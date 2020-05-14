const express = require("express");
const router = express.Router();
const axios = require("axios");


let recieved = false;

router.get("/", (req, res) => {
    res.json(recieved);
})

router.post("/", (req, res) => {
    console.log(req.body)
    const comp = req.body.comp;
    const price = req.body.price;
    const region = req.body.region;
    let newPrice; //added cuz of api uses millimes
    if (!(price) && !(region)) {
        res.render("index.ejs", {errorMessage: "Please enter your country and budget"})
    } else if (region == undefined) {
        res.render("index.ejs", {errorMessage: "Please select your country"})
    } else if (!price) {
        res.render("index.ejs", {errorMessage: "Please enter your budget"})
    } else {
        switch (region) {
            case "tunisia":
                newPrice = price * 1000;
                break;
        }
        getData(comp, newPrice);
    }
})


function getData(comp, newPrice) {
    const api = `https://alphapicker.herokuapp.com/api/?comp=${comp}&budget=${newPrice}`;
    axios.get(api)
        .then((response) => {
            recieved = true;
            const data = response.data;
            console.log(data);
            console.log(recieved)
        })
}

module.exports = router;