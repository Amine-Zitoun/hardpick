const express = require("express");
const router = express.Router();
const axios = require("axios");

let currencies = {
    tunisia: "TND"
}

router.post("/", (req, res) => {
    if (typeof req.session.winner  == "undefined") {
        req.session.winner = {
            pr: "n/a",
            name: "n/a",
            price: 0,
            site: "n/a",
            unit: "n/a",
            differnce: 0
        };
    }
    const comp = req.body.comp;
    const price = req.body.price;
    const region = req.body.region;
    let newPrice; //added cuz of api uses millimes
    console.log(req.body);
    switch (region) {
        case "tunisia":
            newPrice = price * 1000;
            break;
    }
    console.log(newPrice)
    getData(comp, newPrice, req, res, currencies[region])
        .then(data => res.json(data))
        .catch(err => console.log(err))
    
})

function getData(comp, newPrice, req, res, unit) {
    const api = `https://alphapicker.herokuapp.com/api/?comp=${comp}&budget=${newPrice}`;
    return axios.get(api)
        .then((response) => {
            const data = response.data;
            req.session.winner.name = data.win.prd;
            req.session.winner.pr = data.win.pr;
            req.session.winner.price = data.win.price;
            req.session.winner.site = data.win.site;
            req.session.winner.unit = unit;
            req.session.winner.differnce = req.session.winner.price - newPrice;
            console.log(req.session.winner)
            req.session.save();
            return(req.session.winner);
        }).catch(err => console.error(err))
}

module.exports = router;