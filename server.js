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


SpeciesInfo = {
Clownfish : {
    Name: "Clownfish",
    ScientificName: "Amphiprion ocellaris",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Pomacentridae",
        Genus: "Amphiprion",
        Species: "A. ocellaris",
    },
    Description: "Clown fishes have striking orange & white coloration. ",
    Location: "Found on coral reefs in the tropical Pacific & Indian oceans from northwestern Australia, Southeast Asia, & Indonesia to Taiwan & Japan’s Ryukyu Islands.",
},

BlueTang : {
    Name: "Blue Tang",
    ScientificName: "Paracanthurus hepatus",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Acanthuriformes",
        Genus: "Acanthuridae",
        Species: "P. hepatus",
    },
    Description: "Blue Tang has a royal blue body, yellow tail, & black palette design.  ",
    Location: "Found in the Indo-Pacific, in the reefs of the Philippines, Indonesia, Japan, the Great Barrier Reef of Australia, New Caledonia, Samoa, East Africa, & Sri Lanka",
},

TrumpetFish: {
    Name: "Trumpet Fish",
    ScientificName: "Aulostomus",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Aulostomidae Rafinesque",
        Genus: "Aulostomus Lacépède",
        Species: "Aulostomus chinesis",
    },
    Description: "Trumpetfishes have elongated bodies & stiff tubelike snouts ending in small jaws.",
    Location: "Found on coral reefs & reef flats in the tropical & subtropical waters of the Atlantic, Indian, & western Pacific oceans.",
},


MorayEel: {
    Name: "Moray Eel",
    ScientificName: "Muraenidae ",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Muraenidae",
        Genus: "Gymnothorax",
        Species: "G. javanicus",
    },
    Description: "These slender, predatory bony fishes come in a wide variety of colors & patterns. The skin of morays is thick & lacks scales.",
    Location: "Occur in all tropical & subtropical seas, where they live in shallow water among reefs & rocks & hide in crevices.",
},

MantaRay : {
    Name: "Manta Ray",
    ScientificName: "Manta birostris",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Chondrichthyes",
        Family: "Mobulidae",
        Genus: "Manta Bancroft",
        Species: "Manta birostris",
    },
    Description: "Flattened & wider than they are long, manta rays have fleshy enlarged pectoral fins that look like wings and have short whiplike tails ",
    Location: "Found in tropical, subtropical, temperate bodies of water, in oceanic waters, & in productive coastal areas.",
},

GiantTrevally : {
    Name: "Giant Trevally",
    ScientificName: "Caranx ignobilis",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Carangidae",
        Genus: "Caranx",
        Species: "C. ignobilis",
    },
    Description: "It is normally a silvery colour with occasional dark spots, but males may be black once they mature.",
    Location: "Founds in warm, coastal waters in the Indo-Pacific, including Africa's eastern coast, Japan, northern Australia, & the Pacific Islands.",
},

EmperorAngelfish : {
    Name: "Emperor Angelfish",
    ScientificName: "Pomacanthus imperator",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Pomacanthidae",
        Genus: "Pomacanthus",
        Species: "P. imperator",
    },
    Description: "It has a dark stripe across its eye area, which resembles a mask. Its body is vibrantly coloured, with alternating stripes in blue & yellow. ",
    Location: "Emperor angelfish can be found in coral reefs in the Pacific & Indian oceans, & have been reported off the coast of Hawaii.",
},

GreenChromis : {
    Name: "Green Chromis",
    ScientificName: "Chromis viridis ",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Pomacentridae",
        Genus: "Chromis",
        Species: "C. viridis",
    },
    Description: "Species of damselfish, tend to be iridescent apple-green & light blue, & reach a maximal length of 10 cm.",
    Location: "Found in tropical waters of the Pacific Ocean, east of the Philippines, New Guinea & eastern Australia, where they live in coral reef areas.",
},

HumpheadWrasse : {
    Name: "Humphead Wrasse",
    ScientificName: "Cheilinus undulatus",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Labridae",
        Genus: "Cheilinus",
        Species: "C. undulatus",
    },
    Description: "They have thick, full lips & a forehead hump. Males have bright electric blue, green, or purplish-blue colour. Juveniles & females have red-orange colour & white on their bellies.  ",
    Location: "The humphead wrasses can be found on the east coast of Africa around the mouth of the Red Sea, & in some areas of the Indian & Pacific Oceans.",
},

LionFish : {
    Name: "Lion Fish",
    ScientificName: "Pterois",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Scorpaenidae",
        Genus: "Pterois Oken",
        Species: "Pterois brevipectoralis",
    },
    Description: "They have distinctive brown or maroon, & white stripes with fleshy tentacles above their eyes & below the mouth.",
    Location: "Lionfish are native to the warm, tropical waters of the South Pacific & Indian Oceans (i.e., the Indo-Pacific region), including the Red Sea.",
},

OrientalFlyingGurnard : {
    Name: "Oriental Flying Gurnard",
    ScientificName: "Dactyloptena orientalis",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Dactylopteridae",
        Genus: "Dactyloptena",
        Species: "D. orientalis",
    },
    Description: "It has a broad head with a blunt snout & the eyes are set a long way apart. It has a heavily armoured robust body.",
    Location: "Found in tropical waters of the Indo-Pacific region including the Red Sea. Its range extends from the coasts of East Africa to Polynesia & the western, northern & eastern coasts of Australia.",
},

OrientalSweetlips : {
    Name: "Oriental Sweetlips",
    ScientificName: "Plectorhinchus vittatus",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Haemulidae",
        Genus: "Plectorhinchus",
        Species: "P. vittatus",
    },
    Description: "They are vibrantly coloured, reef-dwelling fish with rounded bodies, striking horizontal blue, yellow, & white stripes.",
    Location: "Found in the tropical waters of the Indo-Pacific region ranging from East Africa to the Western Coast of Australia.",
}
,
RibbonEel : {
    Name: "Ribbon Eel",
    ScientificName: "Rhinomuraena quaesita",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Muraenidae",
        Genus: "Rhinomuraena Garman",
        Species: "R. quaesita",
    },
    Description: "The ribbon eel bears a resemblance to a mythical Chinese dragon with a long, thin body & high dorsal fins. The ribbon eel can easily be recognised by its exp&ed anterior nostrils.",
    Location: "The ribbon eel is found in lagoons & reefs in the Indo-Pacific Ocean, ranging from East Africa to southern Japan, Australia & French Polynesia.",
},

BlueShark : {
    Name: "Blue Shark",
    ScientificName: "Prionace glauca",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Chondrichthyes",
        Family: "Carcharhinidae",
        Genus: "Prionace Cantor",
        Species: "P. glauca",
    },
    Description: "It has a distinct colouration, a deep indigo blue from above & a vibrant blue on its sides, changing to white underneath. ",
    Location: "Found in Atlantic, Pacific & Indian Oceans in both inshore & offshore waters; from 50º N latitude to 50ºS latitude. In the western Atlantic it can be found from Newfoundland & the Gulf of St. Lawrence to Argentina.",
},

TriggerFish : {
    Name: "Trigger Fish",
    ScientificName: "Balistidae",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Balistidae A. Risso, 1810",
        Genus: "Abalistes",
        Species: "Abalistes stellatus",
    },
    Description: "They have an oval-shaped, highly compressed body, often marked by lines & spots. The head is large, ending in a small but strong-jawed mouth. ",
    Location: "Found in tropical & subtropical oceans throughout the world, with the greatest species richness in the Indo-Pacific.",
},

ParrotFish : {
    Name: "Parrot Fish",
    ScientificName: "Scaridae",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Balistidae A. Risso",
        Genus: "",
        Species: "",
    },
    Description: "They have an oval-shaped, highly compressed body, often marked by lines & spots. The head is large, ending in a small but strong-jawed mouth. ",
    Location: "Found in tropical & subtropical oceans throughout the world, with the greatest species richness in the Indo-Pacific. ",
},

PufferFish : {
    Name: "Puffer Fish",
    ScientificName: "Tetraodontidae",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Tetraodontidae Bonaparte",
        Genus: "Arothron",
        Species: "A. mappa",
    },
    Description: "Pufferfish can inflate into a ball shape to evade predators. Some pufferfish species also have spines on their skin to ward off predators.",
    Location: "They primarily live in marine habitats from coasts & reefs to open pelagic waters & deep ocean, but some pufferfishes live in freshwater rivers in Southeast Asia, South America, & Africa.",
},

MahiMahi : {
    Name: "Mahi Mahi",
    ScientificName: "Coryphaena hippurus",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Coryphaenidae",
        Genus: "Coryphaena",
        Species: "C. hippurus",
    },
    Description: "They have an elongated compressed body & a forked tail with metallic blue-green above & silver with a golden sheen on the sides and iridescent blue to black spots on the sides.",
    Location: "Found in the Atlantic, Gulf of Mexico, & Caribbean, the Pacific Ocean (mainly Hawaii).",
},

PinnateSpadefish : {
    Name: "Pinnate Spadefish",
    ScientificName: "Platax pinnatus",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Ephippidae",
        Genus: "Platax",
        Species: "P. pinnatus",
    },
    Description: "They have a round, strongly compressed body which has a depth of twice the length of the head. Larger adults, have a protruding snout.",
    Location: "Found in the Indo-West Pacific & Indian Ocean. The confirmed range is in the western Pacific from the Ryukyu Islands south to Australia.",
},

MandarinFish : {
    Name: "Mandarin Fish",
    ScientificName: "Synchiropus splendidus",
    ScientificClassification: {
        Domain: "Eukaryota",
        Kingdom: "Animalia",
        Phylum: "Chordata",
        Class: "Actinopterygii",
        Family: "Callionymidae",
        Genus: "Synchiropus",
        Species: "S. splendidus",
    },
    Description: "Small, broad-headed & elongated, scaleless fish. A brilliantly-colored fish, with striking patterns of green & orange.",
    Location: "Occurs in the Western Pacific from the Philippine Islands to the Great Barrier Reef.",
}
}


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
    path = 'C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Website/Flask app/' + req.files.file.name;
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
                        "C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Website/public/Videos/" +
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
                        "C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Website/public/Videos/" +
                        resultsName;
                    fs.rename(resultsPath, rp, function (err) {
                        if (err) throw err;
                        console.log("File Renamed!");
                        console.log(resultsPath);
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
                        "C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Website/public/Videos/" +
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
                    totalMaxCount = response.data.totalMaxCount;
                    totalMinCount = response.data.totalMinCount;
                    avgCount = response.data.avgCount;
                    console.log(resultsPath);
                    console.log(resultsName);
                    const info = []
                    
                        
                    for(let key in totalMaxCount)
                    {
                        var temp = Object.values(SpeciesInfo)
                        for(let i=0;i<temp.length;i++)
                        {
                            if(temp[i].Name==key)
                            {
                                console.log(temp[i].ScientificClassification.Species)
                                info.push(temp[i])
                            }
                        }
                    }
                    
                    console.log(info)

                    rp =
                        "C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Website/public/Videos/" +
                        resultsName;
                    fs.rename(resultsPath, rp, function (err) {
                        if (err) throw err;
                        console.log("File Renamed!");
                        console.log(resultsPath);
                        res.render("analysis", { resultsPath: resultsName, totalMaxCount: totalMaxCount,  totalMinCount: totalMinCount, avgCount:avgCount, info: info});
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