const express = require('express');
const https = require('https');
const bodyParser = require('body-parser');

const app = express();
app.set('view engine', 'ejs');
app.use(express.static(__dirname + "/public/"));
app.use(express.urlencoded({ extended: true }));

app.get('/', function(req, res) {
    res.sendFile(__dirname + "/home.html");
});

app.get('/upload', function(req, res) {
    res.sendFile(__dirname + "/upload.html");
});

app.get('/analysis', function(req, res) {
    res.sendFile(__dirname + "/analysis.html");
});

app.get('/enhancement', function(req, res) {
    res.sendFile(__dirname + "/enhancement.html");
});

app.post('/uploadedVideo', function(req, res) {
    console.log(req.body.videoFile);
    res.redirect('/analysis');
});

app.listen(process.env.PORT || 3000,function(){
    console.log("Server is running on port 3000");
});