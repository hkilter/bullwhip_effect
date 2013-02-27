
# map function that counts the number of companies funded over $1 million from 2003 to 2008
function(doc) {
    var total_funding = 0;
    if(doc.permalink && doc.funding_rounds && doc.founded_year > 2002 && doc.founded_year < 2009) {
        doc.funding_rounds.forEach(function(round) {
           if('raised_amount' in round) {
                 total_funding += round.raised_amount;
           }
        });
    if(total_funding > 1000000) {
        emit(total_funding, doc.permalink+ "\t"+ doc.overview);
    }
  }   
}