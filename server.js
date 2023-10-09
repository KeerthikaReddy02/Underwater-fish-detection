const express = require('express');
const https = require('https');
const bodyParser = require('body-parser');
const axios = require('axios');
const fileUpload= require("express-fileupload");
const fs = require('fs');
const fs1 = require('fs-extra');
const { Console } = require('console');

const app = express();
app.set('view engine', 'ejs');
app.use(express.static(__dirname + "/public/"));
app.use(express.urlencoded({ extended: true }));
app.use(fileUpload());


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

// app.post('/uploadedVideo', function(req, res) {
//     vid = req.files.file;
//     path = 'C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Website/Flask app/' + req.files.file.name;
//     // console.log(path)
//     vid.mv(path, err => {
//         if (err) {
//             return res.status(500).send(err);
//         }
        
//         console.log('File uploaded successfully');
//     });
//     axios.post('http://127.0.0.1:5000/predict', {    
//         path: path,
//     })
//     res.sendFile(__dirname + "/analysis.html");
// });

app.post('/uploadedVideo', function(req, res) {
    // console.log(req.files.file);
    console.log(req.body.enhancement);
    vid = req.files.file;
    if (!req.files)
        return res.status(400).send('No files were uploaded.');
    path = 'C:/UnderwaterDatasetFinal/mainWebsite/Underwater-fish-detection/Flask app' + req.files.file.name;
    // console.log(path)
    vid.mv(path, err => {
        if (err) {
            return res.status(500).send(err);
        }
        
        console.log('File uploaded successfully');
    });

    if (req.body.enhancement == "denoise") {
        axios
            .post("http://127.0.0.1:5000/denoise", {
                path: path,
            })
            .then(
                (response) => {
                    resultsPath = response.data.path;
                    resultsName = response.data.filename;
                    console.log(resultsPath);
                    console.log(resultsName);
                    rp =
                        "C:/UnderwaterDatasetFinal/mainWebsite/Underwater-fish-detection/public/Videos/" +
                        resultsName;
                    fs.rename(resultsPath, rp, function (err) {
                        if (err) throw err;
                        console.log("File Renamed!");
                        res.render("analysis", { resultsPath: resultsName });
                    });
                },
                (error) => {
                    console.log(error);
                }
            );
    } else if (req.body.enhancement == "histeq") {
        axios
            .post("http://127.0.0.1:5000/histeq", {
                path: path,
            })
            .then(
                (response) => {
                    resultsPath = response.data.path;
                    resultsName = response.data.filename;
                    console.log(resultsPath);
                    console.log(resultsName);
                    rp =
                        "C:/UnderwaterDatasetFinal/mainWebsite/Underwater-fish-detection/public/Videos/" +
                        resultsName;
                    fs.rename(resultsPath, rp, function (err) {
                        if (err) throw err;
                        console.log("File Renamed!");
                        res.render("analysis", {
                            resultsPath: resultsName,
                        });
                    });
                },
                (error) => {
                    console.log(error);
                }
            );
    } else if (req.body.enhancement == "whitebalancing") {
        axios
            .post("http://127.0.0.1:5000/clahe", {
                path: path,
            })
            .then(
                (response) => {
                    resultsPath = response.data.path;
                    resultsName = response.data.filename;
                    console.log(resultsPath);
                    console.log(resultsName);
                    rp =
                        "C:/UnderwaterDatasetFinal/mainWebsite/Underwater-fish-detection/public/Videos/" +
                        resultsName;
                    fs.rename(resultsPath, rp, function (err) {
                        if (err) throw err;
                        console.log("File Renamed!");
                        res.render("analysis", { resultsPath: resultsName });
                    });
                },
                (error) => {
                    console.log(error);
                }
            );
    } else if (req.body.enhancement == "none") {
        axios
            .post("http://127.0.0.1:5000/predict", {
                path: path,
            })
            .then(
                (response) => {
                    resultsPath = response.data.path;
                    resultsName = response.data.filename;
                    console.log(resultsPath);
                    console.log(resultsName);
                    rp =
                        "C:/UnderwaterDatasetFinal/mainWebsite/Underwater-fish-detection/public/Videos/" +
                        resultsName;
                    fs.rename(resultsPath, rp, function (err) {
                        if (err) throw err;
                        console.log("File Renamed!");
                        res.render("analysis", { resultsPath: resultsName });
                    });
                },
                (error) => {
                    console.log(error);
                }
            );
    }


    // axios.post('http://127.0.0.1:5000/histeq', {    
    //     path: path,
    // }).then((response) => { 
    //     resultsPath = response.data.path;
    //     resultsName = response.data.filename;
    //     console.log(resultsPath);
    //     console.log(resultsName);
    //     rp = 'C:/UnderwaterDatasetFinal/mainWebsite/Underwater-fish-detection/public/Videos/'+resultsName ;
    //     fs.rename(resultsPath, rp, function (err) 
    //     { 
    //         if (err) throw err; console.log('File Renamed!'); 
    //         res.render("analysis", { resultsPath: resultsName });
    //     });
    // }, (error) => {
    //     console.log(error);
    // });
});

app.listen(process.env.PORT || 3000,function(){
    console.log("Server is running on port 3000"); 
});