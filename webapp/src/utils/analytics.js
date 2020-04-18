import {sum} from "lodash"

export const TimeGroups = Object.freeze({
    Day : groupByDay,
    Week : groupByWeek,
    Month : groupByMonth,
    Global : groupByMonth,
});


export function groupByDay(data, date = new Date().getTime(), timeframe=10) {

    data = data || [];
    
    const start = new Date(date);
    start.setHours(0,0,0,0);
    start.setDate( start.getDate() - timeframe );
    
    let dateArray = []

    while(start.getTime() < date){
        dateArray.push(new Date(start));
        start.setDate(start.getDate()+1);
    }

    data = data.map(d=>{
        return{ 
            date: new Date(d["date"]).setHours(0,0,0,0),
            count: d["count"]
        }
    })


    return dateArray.map(d => {
        let dd = d.getDate();
        let mm = d.getMonth() + 1;
        dd = dd < 10 ? '0' + dd : dd;
        mm = mm < 10 ? '0' + mm : mm;
        return {
            date: dd + "/" + mm,
            count: sum(data.filter(c => c["date"] === d.getTime()).map(o => o["count"]))
        }
    });
}

export function groupByWeek(data, date = new Date().getTime(), timeframe=10) {

    data = data || [];
    
    const start = new Date(date);
    start.setHours(0,0,0,0);
    start.setDate( start.getDate() - timeframe*7 -start.getDay());
    
    let dateArray = []

    while(start.getTime() < date){
        dateArray.push(new Date(start));
        start.setDate(start.getDate()+7);
    }

    data = data.map(d=>{
        return{ 
            date: new Date(d["date"]).setHours(0,0,0,0),
            count: d["count"]
        }
    })

    return dateArray.map(d => {
        let dd = d.getDate();
        let mm = d.getMonth() + 1;
        dd = dd < 10 ? '0' + dd : dd;
        mm = mm < 10 ? '0' + mm : mm;
        return {
            date: dd + "/" + mm,
            count: sum(data.filter(c => c["date"] >= d.getTime() && c["date"] < new Date(d).setDate(d.getDate()+7)).map(o => o["count"]))
        }
    });
}

export function groupByMonth(data, date = new Date().getTime(), timeframe=12) {

    data = data || [];
    
    const start = new Date(date);
    start.setHours(0,0,0,0);
    start.setDate(1);
    start.setMonth( start.getMonth() - timeframe );
    
    let dateArray = []

    while(start.getTime() < date){
        dateArray.push(new Date(start));
        start.setMonth(start.getMonth()+1);
    }
    
    data = data.map(d=>{
        return{ 
            date: new Date(d["date"]).setHours(0,0,0,0),
            count: d["count"]
        }
    })

    return dateArray.map(d => {
        let mm = d.getMonth() + 1;
        let yy = d.getFullYear().toString().slice(2);
        mm = mm < 10 ? '0' + mm : mm;
        return {
            date: mm + "/" + yy,
            count: sum(data.filter(c => c["date"] >= d.getTime() && c["date"] < new Date(d).setMonth(d.getMonth()+1)).map(o => o["count"]))
        }
    });
}