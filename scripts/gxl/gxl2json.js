import * as fs from 'fs';
import * as xml2js from 'xml2js';
//import { embedObj } from './embedGxl';

const dest = 'data/Letter/LOW/';
const target = 'json/LOW/';

fs.readdir(dest, (err, files) => {
    files.forEach( file => {
        if(file.split('.')[1] === 'gxl') {
            const parser = new xml2js.Parser();
            fs.readFile(dest + file, function(err, data) {
                parser.parseString(data, function (err, result) {
                    console.log('1: ' + file);
                    fs.writeFileSync(target + file.slice(0, -4) + '.json', 
                        JSON.stringify(result) + '');
                });
            });        
        } else {
            fs.readFile(dest + file, function(err, data) {
                console.log('2: ' + file);
                fs.writeFileSync(target + file, data);
            });        
        }
    });
});
