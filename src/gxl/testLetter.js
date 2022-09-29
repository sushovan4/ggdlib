import * as fs from 'fs';
import { ggd } from '../ggd.js';
import { adjMat } from './gxlObj.js';

function testLetter(distortion = 'LOW', C_V = 0.5, C_E = 1) {
    const out = [];
    const PROTOTYPE = [];
    const proto_path = 'data/PROTOTYPE/';
    const source_path = 'data/Letter/json/' + distortion + '/';
    
    fs.readdirSync(proto_path).forEach( file => {
        const data = fs.readFileSync(proto_path + file);
        PROTOTYPE.push(JSON.parse(data));
    });
    
    fs.readdirSync(source_path).forEach( file => {
        if(file.split('.')[1] !== 'json')
             return;
        const data = fs.readFileSync(source_path + file);
        const G = JSON.parse(data);
        let dist = Infinity;
        let nearestTo;
        PROTOTYPE.forEach( H => {
            //console.log(H.gxl.graph[0].$.id);
            const dist1 =  ggd(adjMat(G), adjMat(H), C_V, C_E);
            if( dist1 < dist) {
                nearestTo = H.gxl.graph[0].$.id;
                dist = dist1;
            }
        });
        out.push({ file, nearestTo, distortion, C_V, C_E });
        console.log(file, nearestTo);
    });
    fs.writeFileSync('out.json', JSON.stringify(out));
}
testLetter();
export { testLetter };