function(doc) {
      for(var idx in doc.triplestore.relationships) {
        for(var jdx in doc.triplestore.relationships[idx]) {
            for(var kdx in doc.triplestore.relationships[idx][jdx]) {
                var relations = [];
                if(doc.triplestore.relationships[idx][jdx].length > 1) {
                    for (var kdx in doc.triplestore.relationships[idx][jdx]) {
                            var compound_relation = doc.triplestore.relationships[idx][jdx][kdx][0];
                            relations.push(compound_relation);
                    }
                    emit(relations, doc.triplestore.objects[0][0][0][0]);
                } else {                
                var relation = doc.triplestore.relationships[idx][jdx][kdx][0];
                emit(relation, doc.triplestore.objects[0][0][0][0]);
                  }
            }
         }
     }
}