var usfm = require('usfm-js');
var fs = require('fs');

try {
    const sample = fs.readFileSync('data/el-x-koine_ugnt/41-MAT.usfm', 'utf8')
    var toJSON = usfm.toJSON(sample);
    //  console.log(sample)
} catch (err) {
    console.error(err)
}

//Convert from USFM to JSON
// console.log(toJSON)
console.log(toJSON['chapters']['1']['18'])