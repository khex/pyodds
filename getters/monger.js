/** это курсор запрос, антоним aggregate фреймворка **/ 
db.getCollection('matches').
    find({$or: [{'home.tid': 95}, {'away.tid': 95}]}).
    sort({'date.timestamp': -1}).
    // count()
    toArray();

db.getCollection('matches').find({$or: [{'home.tid': 95}, {'away.tid': 95}]})


for (var i = 0; i < asdf.length; i++) {
    asdf[i].home.name
};


db.getCollection('matches').find({$or: [{'home.team': 'Houston Astros'}, {'away.team': 'Houston Astros'}], 'seas_type': 'season'}).count();
    //).sort({'date.timestamp': -1}).count();

match_list = db.matches.find({'league': 'mlb', 'season': '2015', 'seas_type': 'season',
                              '$or': [{'home.team': 'Houston Astros'}, {'away.team': 'Houston Astros'}] }).sort("datetime.timestamp", -1)