const fs = require('fs');
const util = require('util');
const readFile = util.promisify(fs.readFile);
const writeFile = util.promisify(fs.writeFile);

const CONFIG_FILE = process.env.CONFIG_FILE;  // replace with your actual config file path

async function getConfig() {
    // Read the config file and parse it as JSON
    const data = await readFile(CONFIG_FILE);
    console.log("data",JSON.parse(data))
    return JSON.parse(data);
}

async function saveConfig(config) {
    // Stringify the config object and write it to the config file
    const data = JSON.stringify(config, null, 2);
    console.log("write",data)
    await writeFile(CONFIG_FILE, data);
}

module.exports = {
    getConfig,
    saveConfig,
};