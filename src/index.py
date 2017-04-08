from preprocessing import *
import argparse
from partition import *
from content.content_recommender import ContentRecommender
import datetime

def content_classifier(repo, timestamp):
    #Wrapper for content classification.
    #call train and test for all member and
    #events and print the results

    training_events_dict = get_member_events_dict_in_range(repo, timestamp - train_data_interval, timestamp)

    potential_events = filter_events_by_time_range(repo, list(repo['events_info'].keys()), timestamp,
                                                   timestamp + train_data_interval)

    contentRecommender = ContentRecommender()
    contentRecommender.train(training_events_dict, repo)
    print contentRecommender.test('11173777', potential_events, repo)

def main():
    parser = argparse.ArgumentParser(description='Run Event Recommender')
    parser.add_argument('--city', help='Enter the city name')
    args = parser.parse_args()

    city = args.city
    group_members, group_events = load_groups("../crawler/cities/" + city + "/group_members.json",
                                                            "../crawler/cities/" + city + "/group_events.json")
    events_info = load_events("../crawler/cities/" + city + "/events_info.json")
    members_info = load_members("../crawler/cities/" + city + "/members_info.json")
    member_events = load_rsvps("../crawler/cities/" + city + "/rsvp_events.json")

    repo = dict()
    repo['events_info'] = events_info
    repo['members_info'] = members_info
    repo['members_events'] = member_events

    start_time = 1262304000 # 1st Jan 2010
    end_time = 1451606400 # 1st Jan 2016

    timestamps = get_timestamps(start_time, end_time)

    for t in timestamps:
        print "Partition at timestamp ", datetime.datetime.fromtimestamp(t), " are : "

        partitioned_repo = get_partitioned_repo(t, repo)


        #Call content based classifer train and test functions from here. Pass the repo
        #as an argument to these functions.
        content_classifier(partitioned_repo, t)

if __name__ == "__main__":
    main()