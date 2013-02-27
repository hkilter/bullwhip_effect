#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     30/07/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import couchdb
from couchdb.design import ViewDefinition
from prettytable import PrettyTable

def main():
    pass

permalinks = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\growthscout_test.txt', 'r')]

for link in permalinks:
    DB = 'tweets_user_timeline_%s' % (link)
    frequency = 1
    server = couchdb.Server('http://localhost:5984')
    db = server[DB]

    if len(sys.argv) > 2 and frequency.isdigit():
        FREQ_THRESHOLD = int(frequency)
    else:
        FREQ_THRESHOLD = 1
    def entityCountMapper(doc):
        if not doc.get('entities'):
            import twitter_text

            def getEntities(tweet):
                # Now extract various entities from it and build up a familiar structure
                extractor = twitter_text.Extractor(tweet['text'])

                # Note that the production Twitter API contains a few additional fields in
                # the entities hash that would require additional API calls to resolve
                entities = {}
                entities['user_mentions'] = []
                for um in extractor.extract_mentioned_screen_names_with_indices():
                    entities['user_mentions'].append(um)
                    entities['hashtags'] = []
                for ht in extractor.extract_hashtags_with_indices():
                    # Massage field name to match production twitter api
                    ht['text'] = ht['hashtag']
                    del ht['hashtag']
                    entities['hashtags'].append(ht)
                    entities['urls'] = []
                for url in extractor.extract_urls_with_indices():
                    entities['urls'].append(url)
                return entities

            doc['entities'] = getEntities(doc)

        if doc['entities'].get('user_mentions'):
            for user_mention in doc['entities']['user_mentions']:
                yield ('@' + user_mention['screen_name'].lower(), [doc['_id'], doc['id']])
        if doc['entities'].get('hashtags'):
            for hashtag in doc['entities']['hashtags']:
                yield ('#' + hashtag['text'], [doc['_id'], doc['id']])
        if doc['entities'].get('urls'):
            for url in doc['entities']['urls']:
                yield (url['url'], [doc['_id'], doc['id']])

    def summingReducer(keys, values, rereduce):
        if rereduce:
            return sum(values)
        else:
            return len(values)

    view = ViewDefinition('index', 'entity_count_by_doc', entityCountMapper,
                 reduce_fun=summingReducer, language='python')
    view.sync(db)

    # Print out a nicely formatted table. Sorting by value in the client is cheap and easy
    # if you're dealing with hundreds or low thousands of tweets
    entities_freqs = sorted([(row.key, row.value) for row in
                        db.view('index/entity_count_by_doc', group=True)],
                        key=lambda x: x[1], reverse=True)

    fields = ['Entity', 'Count']
    pt = PrettyTable(field_names=fields)
    for f in fields:
        pt.align = "l"
    for (entity, freq) in entities_freqs:
        if freq > FREQ_THRESHOLD:
            pt.add_row([entity, freq])
    print pt.get_string()

# Map entities in tweets to the docs that they appear in

if __name__ == '__main__':
    main()
