
export function getAllIndexes(csv_content) {
    let indexes = [];
    let lines = csv_content.split("\n");

    for (let i = 0; i < lines.length; i++)
        indexes.push(lines[i].split(",")[0]);

    indexes.shift();

    return indexes;
}

export function parseCSV(csv_content) {
    let lines = csv_content.split("\n").filter(o => o.trim().length > 0);
    let columns = lines.shift().split(",");
    let result = [];

    for (let i = 0; i < lines.length; i++) {
        let row = {};
        let values = lines[i].split(",");

        for (let y = 0; y < values.length; y++)
            row[columns[y]] = values[y];

        result.push(row);
    }

    return result;
}

export function getColumnNames(csv_content) {
    let lines = csv_content.split("\n");
    let str = lines.shift();
    let columns = str.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
    return columns;
}