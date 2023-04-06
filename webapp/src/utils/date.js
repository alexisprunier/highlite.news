
export function stringToDate(date) {
    if (typeof date === "string")
        return new Date(date);
    else if (date instanceof Date)
        return date;
    else
        return null;
}

export function dateToString(date) {
    if (typeof date === "string")
        return date.substring(10, 0);
    else if (date instanceof Date)
        return date.getFullYear() + "-" + String(date.getMonth()+1).padStart(2, '0') +
            "-" + String(date.getDate()).padStart(2, '0');
    else
        return date.format("YYYY-MM-DD");
}