const { readFileSync, writeFileSync } = require("fs");

const path = "node_modules/source-map-loader/dist/utils.js";
const regex = /.*throw new Error\(`Failed to parse source map from '\${sourceURL}' file: \${error}`\);*/;

const text = readFileSync(path, "utf-8");
const newText = text.replace(regex, `buffer="";sourceURL="";`);
writeFileSync(path, newText, "utf-8");