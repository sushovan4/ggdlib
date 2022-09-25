const fs = require('fs'),
    xml2js = require('xml2js');

const dest = './data/Letter/HIGH/';
fs.readdir(dest, (err, files) => {
    files.forEach( file => {
        const parser = new xml2js.Parser();
        fs.readFile(dest + file, function(err, data) {
            parser.parseString(data, function (err, result) {
                fs.writeFileSync('./json/HIGH/' + file.slice(0, -4) + '.json', 
                    JSON.stringify(result) + '');
            });
        });        
    });
})
