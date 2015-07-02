var pref = 'http://www.oddsportal.com/baseball/usa/mlb-2014/',
   teams = require('./teamList.js'),
  moment = require('moment'),
    util = require('util'),
  colors = require('colors'),
 phantom = require('phantom');

/**
 * Array : A, Object: O, Number: N, String: S, Date: D, Function: F
 *
 * #home-away
 * return callback(@boolean: null, @object:
 *    teams:[$, $], oddsFtot:[№], crawlDate:#, matchDate:#, score:[№], resBox:[№]
 */
// ex scrapFtot
exports.main = function (url, callback) {
  console.log(url.green);
  phantom.create(function (ph) {
    ph.createPage(function (page) {
      page.open(pref + url, function (status) {
        if (status !== 'success') {
          callback('scrapFtot unable to access the network');
        } else {
      ////page.evaluate(function (tesa) { ... }, function (res) { ... }, matchData);    
          page.evaluate(function () {
              var match = {};
              /** **/
              var teams = document.getElementsByTagName("h1")[0].innerHTML.split(' - ');
              match.teams = [teams[0], teams[1]];
              match.oddsFtot = [
                  Number(document.getElementsByClassName("aver")[0].getElementsByClassName("right")[0].innerHTML),
                  Number(document.getElementsByClassName("aver")[0].getElementsByClassName("right")[1].innerHTML)
              ];
              /** date & time **/
              match.timeDate = new Date(document.getElementsByClassName("date")[0].innerHTML);
              /** score & resalt box **/
              var scoreData = document.getElementById("event-status").innerText.replace(/\u0028|\u0029/g, "").split(' ');
              match.score = scoreData[2].split(':').map(function (val) { return parseInt(val, 10); });
              match.resBox = scoreData.slice(3).join(' ');
              return match;
            },
            function (res) {
                console.log('Scrapped #home-away %s'.green, res.oddsFtot);
                callback(null, res);
                ph.exit(); 
                /**
                if(res.oddsFtot[0]  < 0 || res.oddsFtot[0] > 10) {
                    callback(throw new Error('Какаето херня с коефициентами'));
                    ph.exit(); 
                } else {
                    console.log('Scrapped #home-away %s'.green, res.oddsFtot);
                    callback(null, res);
                    ph.exit();             
                }
                **/                
            }
          );
        }
      });
    });
  });
}

/**
 * #ah;1 вытягивает коефициенты на handyCap
 *
 * return: callback(@null, @object:
 *   oddsHandy:[[homeHandy, homeOdd],[awayHandy, awayOdd]]
*/
// ex scrapHandy
exports.handy = function (url, matchData, callback) {
  phantom.create(function (ph) {
    ph.createPage(function (page) {
      page.open(pref + url + "/#ah;1", function (status) {
        if (status !== 'success') {
          callback('scrapHandy unable to access the network');
        } else {
          page.evaluate(function (tesa) {
              var maslo = document.getElementsByClassName("table-header-light");
              var handyOdds;
              for (var i = 0, l = maslo.length; i < l; i += 1) {
                var odd = maslo[i].getElementsByTagName("strong")[0].getElementsByTagName("a")[0].innerHTML.substring(15).trim();
                if (odd === '-1.5' || odd === '1.5') {
                  //почему-то поменяны местами кф. на первую и вторую команды
                  var home = maslo[i].getElementsByClassName("nowrp")[1].getElementsByTagName("a")[0].innerHTML;
                  var away = maslo[i].getElementsByClassName("nowrp")[0].getElementsByTagName("a")[0].innerHTML;
                //var cnt = maslo[i].getElementsByClassName("odds-cnt")[0].innerHTML.replace(/\u0028|\u0029/g, "");// unicode-table.com
                  handyOdds = [odd, (-1 * odd), home, away];
                }
              }
              tesa.handy = handyOdds.map(function (val) { return Number(val); });
              //util.isArray([]) // true
              return tesa;
            },
            function (res) {
              console.log('Scrapped handy: %s'.green, res.handy);
              callback(null, res);
              ph.exit();
            },
            matchData // аргумент из предыдущей функции
          );
        }
      });
    });
  });
}

/*
 * "#over-under;1" вытягивает значение тотала
 *
 * arguments:
 *   @matchData {Object} [это данные матча от scrapHandy]
 *   @callback {Function} [возвращает данные матча + тотал]
 *
 * #home-away
 * return callback(@boolean: null, @object:
 *    total:[value, under, over]
*/
// ex scrapTotal
exports.total = function (url, matchData, callback) {
  phantom.create(function (ph) {
    ph.createPage(function (page) {
      /*****************************************
      ***              START                 ***
      *****************************************/
      page.open(pref + url + "/#over-under;1", function (status) {
        if (status !== 'success') {
          callback('scrapHandy unable to access the network');
        } else {
          page.evaluate(function (argum) {
              /** @type {NodeList} */
              var node = document.getElementsByClassName("table-header-light");
              var arry = [];
              for (var i = 0, l = node.length; i < l; i += 1) {
                /** величина тотала **/
                var value = node[i].getElementsByTagName("strong")[0].getElementsByTagName("a")[0].innerHTML.substring(12);
                /**  кофициенты на тотал **/
                var smth = node[i].getElementsByClassName("nowrp")[0].querySelector('a');
                if (smth !== null && value % 1 !== 0) {
                  /** кф. на меньше **/
                  var over = node[i].getElementsByClassName("nowrp")[0].getElementsByTagName("a")[0].innerHTML;
                  /** кф. на больше **/
                  var under = node[i].getElementsByClassName("nowrp")[1].getElementsByTagName("a")[0].innerHTML;
                  /** разница коефициентов **/
                  var diff = Math.abs(over - under);
                  arry.push([value, over, under, diff]);
                }
              }
              /** сортирует массив по наименьшей diff и возв 1й елемент **/
              argum.total = arry
                  .sort(function (a, b) { return a[3] > b[3] ? 1 : a[3] < b[3] ? -1 : 0;})[0].slice(0,3)
                  .map(function (val) { return Number(val); });
              return argum; // убрать последний елемент diff
            },
            /** return resalts **/
            function (res) {
              console.log('Scrapped total %s'.green, res.total);
              callback(null, res);
              ph.exit();
            },
            matchData // argument #1
          );
        }
      });
    });
  });
}
//ex beautifuler
exports.builder = function (match, callback) {
    console.log('Start buliding the match'.green);
    /** metaData **/
    var Match = {odds: {}, stats:{}, profit: {}};
    Match.homeTeam = teams(match.teams[0]),
    Match.awayTeam = teams(match.teams[1]),
    Match.crawlDate = moment().format('DD/MM/YYYY HH:mm:ss,SSS'),
    Match.timeDate = moment(match.timeDate).format('DD/MM/YYYY HH:mm'),
    Match.unixDate = moment(match.timeDate).format('X'),
    Match.score = match.score,
    Match.resBox = match.resBox,
    Match.overTime = (match.resBox.split(',').length === 9) ? 0 : 1;
    
    try {
        if (match.oddsFtot[0] < 0 || match.oddsFtot[0] > 10) throw new Error('Левый ftot');      
        Match.odds.ftot = match.oddsFtot;
        if (match.handy.length == 0 || match.handy == undefined ) throw new Error('Нима форы');
        if (match.handy[2] < -10 || match.handy[2] > 10 ) throw new Error('Лошадиный кф. на фору');
        Match.odds.handyCap = match.handy;
        if (match.total.length == 0 || match.total[0] == undefined) throw new Error('Нима тотала');
        Match.odds.total = match.total;
        Match.odds.iTot = [
            statsIndy(match.total[0], match.oddsFtot[0]),
            statsIndy(match.total[0], match.oddsFtot[1])
        ];

        /** stats **/
        Match.stats.ftot = statsFtot(match.score, match.oddsFtot);
        Match.stats.hCap = handyCounter(match.handy, match.score);
        Match.stats.total = (match.score[0] + match.score[1]) - match.total[0];
        Match.stats.iTot = [
            match.score[0] - Match.odds.iTot[0],
            match.score[1] - Match.odds.iTot[1]
        ];
        /** profit **/
        Match.profit.ftot = profitFtot(match.score, match.oddsFtot);
        Match.profit.hCap = handyCounter(match.handy, match.score, 1);
    }
    catch(e) {
        console.log(e);
        Match.odds.ftot = [0, 0];
        Match.odds.handyCap = [0, 0, 0, 0];
        Match.odds.total = [0, 0, 0];
        Match.odds.iTot = [0, 0];
        Match.stats.ftot = [0, 0];
        Match.stats.hCap = [0, 0];
        Match.stats.total = 0;
        Match.stats.iTot = [0, 0];
        Match.profit.ftot = [0, 0];
        Match.profit.hCap = [0, 0];
        Match.profit.ftot = [0, 0];
        Match.profit.hCap = [0, 0];
    }
    callback(Match);
  }

// lose|favor: -2, lose|under: -1, win|favor: 1, win|under: -2
function statsFtot(odds, score) {
    if(odds[0] < odds[1]) {
        return (score[0] > odds[1]) ? [1, -1] : [-2, 2];
    } else {
        return (score[0] < odds[1]) ? [-1, 1] : [2, -2];
    }
}

function statsIndy(total, ftot) {
    if (total == 7.5) {
      return (ftot < 1.7)
        ? 4.5
        : (ftot < 2.7)
          ? 3.5
          : 2.5; }
    else if (total == 6.5) { return (ftot < 2) ? 3.5 : 2.5; }
    else if (total == 8.5) { return (ftot < 1.9) ? 4.5 : 3.5; }
    else if (total == 9.5) { return (ftot < 1.55) ? 5.5 : (ftot < 2.2) ? 4.5 : 3.5; }
    else if (total == 10.5) { return (ftot < 2) ? 5.5 : 4.5; }
    else if (total == 5.5) { return 2.5 }
    else { return 'zero' }
}

function handyCounter(handy, score, n) {
    //handy [-1.5, 1.5, 1.65, 2.65]
    var home = score[0] - score[1];
    var away = score[1] - score[0];
    var stats = (handy[0] < handy[1])
        ? [home - 1.5, away + 1.5]
        : [home + 1.5, away - 1.5];
    if (n) { return (stats[0] > stats[1]) 
        ? [Math.round((handy[2] - 1) * 100), -100]
        : [-100, Math.round((handy[3] - 1) * 100)];}
    else {
        return stats;
    } 
}

//function profithCap (stats, odds) {
//    return (stats[0] > stats[1]) ? [rnd(odds[2] - 1), 0] : [0, rnd(odds[3] - 1)];
//}

function profitFtot (score, odds) {
    return (score[0] > score[1]) 
        ? [Math.round((odds[0] - 1) * 100), -100]
        : [-100, Math.round((odds[1] - 1) * 100)];
}