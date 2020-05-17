const express = require("express");
const router = express.Router();
const axios = require("axios");

let winner = {
    pr: "n/a",
    name: "n/a",
    price: 0,
    site: "n/a",
    unit: "n/a",
    differnce: 0
}


let currencies = {
    tunisia: "TND"
}


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
    } else if (price < 100){
        res.render("index.ejs", {errorMessage: `Budget too low (under 100${currencies[region]})`})
    } else {
        switch (region) {
            case "tunisia":
                newPrice = price * 1000;
                break;
        }
        getData(comp, newPrice, res, currencies[region]);

        return
    }
})

router.get("/showWin", (req, res) => {
    res.json(winner);
})

router.get("/end", (req, res) => {
    recieved = false;
    console.log(recieved);
})

function getData(comp, newPrice, res, unit) {
    const api = `https://alphapicker.herokuapp.com/api/?comp=${comp}&budget=${newPrice}`;
    axios.get(api)
        .then((response) => {
            recieved = true;
            const data = response.data;
            console.log(data);
            winner.name = data.win.prd;
            winner.pr = data.win.pr;
            winner.price = data.win.price;
            winner.site = data.win.site;
            winner.unit = unit;
            winner.differnce = winner.price - newPrice;
            console.log(recieved)
            res.status(204).send()
        })
}

module.exports = router;