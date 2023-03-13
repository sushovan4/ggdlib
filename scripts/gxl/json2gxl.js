const fs = require('fs'), xml2js = require('xml2js');
const dest = 'HIGH/';

fs.readdir(dest, (err, files) => {
    files.forEach( file => {
        console.log(file);
        const builder = new xml2js.Builder();
        fs.readFile(dest + file, function(err, data) {
            const gxl = builder.buildObject(JSON.parse(data));
            fs.writeFileSync('json/' + file, 
                JSON.stringify(gxl) + '');
        });   
    });
});