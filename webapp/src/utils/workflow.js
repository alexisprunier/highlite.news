
export function getModuleName(module) {
    return module.split(".").pop();
}

export function getModuleNameFromOutput(output) {
    let module = output.split("/")[1];
    module = module.split("_")[0];
    return module;
}

export function getParentsOfModule(module, modules) {
    let parents = [];
    let moduleName = getModuleName(module);
    if (moduleName.startsWith("Shaker"))
        moduleName = "Shaker";

    for (let m in modules) {
        if (module !== m) {
            for (let o in modules[m].outputs) {
                if (o !== "bug" && o !== "valid" && modules[m].outputs[o].includes(moduleName) &&
                    (getModuleName(module) !== "Tickers" || getModuleName(m) !== "IndexStaticExtractor")) {
                    parents.push(m);
                }
            }
        }
    }

    return parents;
}

export function getLevelOfModule(module, modules, level) {
    let parents = getParentsOfModule(module, modules);
    let max_level = 0;

    if (parents.length === 0)
        return level;

    for (let i = 0; i < parents.length; i++) {
        let new_level = getLevelOfModule(parents[i], modules, level+1);
        if (max_level < new_level)
            max_level = new_level;
    }

    return max_level;
}