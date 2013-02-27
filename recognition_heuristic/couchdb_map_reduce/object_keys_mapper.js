//fetch object keys 
function(doc) {
   
        var getKeys = function(obj){
            var keys = [];
            for(var key in obj){
                keys.push(key);
           }
        return keys;
}
        emit(doc.id, getKeys(doc.words_tags_data) )

}
 