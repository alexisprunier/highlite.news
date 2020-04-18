
export function getNameOfInstrumentFromBasylysk(instrument, staticData) {
    // 205 --> ETFS EUR DAILY HEDGED COPPER
    let indexInstrument = staticData[1][0].map(o => {return o[staticData[0].indexOf("basylysk")]}).indexOf(instrument);
    let indexName = staticData[1][0][indexInstrument][staticData[0].indexOf("name")] - 1;
    return  staticData[1][1]["name"][indexName];
}

export function getNameOfInstrumentFromUniqueName(uniqueName, staticData) {
    // AUGBP_FP --> ETFS EUR DAILY HEDGED COPPER
    let indexName = staticData[1][0]
        .filter((o) => o[staticData[0].length] === uniqueName)
        .map((o) => { return o[staticData[0].indexOf('name')]; })[0] - 1;
    let result = staticData[1][1]["name"][indexName];
    return typeof result !== "undefined" ? result : "undefined";
}

export function getDisplayNameOfInstrument(instrument, staticData) {
    // 205 --> AUGBP FP - ETFS EUR DAILY HEDGED COPPER
    let indexInstrument = staticData[1][0].map(o => {return o[staticData[0].indexOf("basylysk")]}).indexOf(instrument);
    let indexName = staticData[1][0][indexInstrument][staticData[0].indexOf("name")] - 1;
    let realName = staticData[1][1]["name"][indexName];
    let indexTicker = staticData[1][0][indexInstrument][staticData[0].indexOf("ticker_bbg")] - 1;
    let ticker = staticData[1][1]["ticker_bbg"][indexTicker];
    return  ticker + " - " + realName;
}

export function getBasylyskFromUniqueName(uniqueName, staticData) {
    // AUGBP_FP --> 205
    return staticData[1][0]
        .filter((o) => o[staticData[0].length] === uniqueName)
        .map((o) => { return o[staticData[0].indexOf('basylysk')]; })[0];
}

export function getUniqueNameFromBasylysk(basylysk, staticData) {
    // 205 --> AUGBP_FP
    return staticData[1][0]
        .filter((o) => o[staticData[0].indexOf('basylysk')] === basylysk)
        .map((o) => { return o[staticData[0].length]; })[0];
}

export function getNameOfPropertyOfInstrument(instrumentID, property, staticData) {
    /*
    instrumentID : 255
    property : "asset_class"

    return : "COMMODITIES"
     */
    let basylyskIndex = staticData[0].indexOf("basylysk");
    let propertyIndex = staticData[0].indexOf(property);
    let valueIndex = staticData[1][0]
        .filter((o) => o[basylyskIndex] === instrumentID)[0][propertyIndex] - 1;
    let result = staticData[1][1][property][valueIndex]
    return typeof result !== "undefined" ? result : "undefined";
}

export function getInstrumentsWithFilters(filters, staticData) {
    let usefulFilters = Object.keys(filters)
        .filter(o => (staticData[0].indexOf(o) >= 0 && filters[o].length > 0));
    let basylyskIndex = staticData[0].indexOf("basylysk");

    if (usefulFilters.length === 0) {
        return [];
    } else {
        let selectedInstruments = staticData[1][0];

        for (let k in usefulFilters) {
            let filterIDs = filters[usefulFilters[k]]
                .map(o => { return staticData[1][1][usefulFilters[k]].indexOf(o) + 1 });

            selectedInstruments = selectedInstruments
                .filter(o => filterIDs.indexOf(o[staticData[0].indexOf(usefulFilters[k])]) >= 0)
        }

        return selectedInstruments.map(o => o[basylyskIndex]);
    }
}

export function hasInstrumentsWithProductType(property, value, productType, staticData) {
    /*
    property : "ISIN"
    value : "FR0000013216"
    productType : "EXCHANGE TRADED FUNDS"

    return : true
     */
    let propertyIndex = staticData[0].indexOf(property);
    let productTypeIndex = staticData[0].indexOf("product_type");
    let productTypeID = staticData[1][1]["product_type"].indexOf(productType) + 1;
    let valueID = staticData[1][1][property].indexOf(value) + 1;

    for (let i = 0; i < staticData[1][0].length; i++) {
        if (staticData[1][0][i][propertyIndex] === valueID && staticData[1][0][i][productTypeIndex] === productTypeID)
            return true;
    }

    return false;
}

export function getStaticsOfInstrumentFromBasylysk(instrument, staticData) {
    let values = [];

    for (let i = 0; i < staticData[0].length; i++) {
        values.push(getNameOfPropertyOfInstrument(instrument, staticData[0][i], staticData));
    }

    return values;
}