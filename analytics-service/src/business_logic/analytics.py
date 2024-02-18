from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
from common_modules.logger.mnt_logging import MntLogging as MyLog
import pprint

analytics_item_info_table_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "activity": {
                "properties": {
                    "activity_info": {
                        "properties": {
                            "shared": {
                                "type": "integer"
                            },
                            "liked": {
                                "type": "integer"
                            },
                            "disliked": {
                                "type": "integer"
                            },
                        }
                    }
                }
            },
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            }
        }
    }
}


class Analytics:
    def __init__(self, config_data):
        # For debugging purposes.

        self.resMgr = ResourceMgr(StorageElastic(cleanup=False), cleanup=False)
        self.user_activity_table = config_data["user_activity_table"]
        self.user_profile_table = config_data["user_profile_table"]
        self.users_per_interest_datasets = ""
        self.user_login_table = config_data["user_login_table"]
        self.pause_time = config_data['sleep']
        self.top_n_user_table = config_data['top_n_user_table']
        self.popular_item_table = config_data['popular_item_table']
        self.num_top_users = config_data['num_top_users']
        self.popular_interest_table = config_data['popular_interest_table']
        self.user_chat_table = config_data['user_chat_table']
        MyLog().setloglevel(config_data['loglevel'])

    def start(self):
        pp = pprint.PrettyPrinter(indent=4)
        MyLog().getlogger().debug(f"Number of Users per interest:")
        #
        # Count Number of users for each interest and store it
        # in the DB config_data['popular_interest_table']
        #               {
        #                 "_index": "analytics_interests_count",
        #                 "_id": "2654109649639",
        #                 "_score": 1.0,
        #                 "_source": {
        #                     "keyword": "productmanagement",
        #                     "interest": 7,
        #                     "created": "2022-07-03T19:27:16.450337",
        #                     "updated": "2022-07-03T19:27:16.450342"
        #               }
        self.count_users_per_interest(self.popular_interest_table)

        MyLog().getlogger().debug("Feed stats:")
        #
        # Calculate popular items in the table
        self.compute_aggregated_feed_counts(self.popular_item_table)
        MyLog().getlogger().debug("Average Time Spent:")
        self.compute_average_feed_time(self.popular_item_table)
        MyLog().getlogger().debug("Top Users:")

        self.compute_top_n_users(pp=pp, table_name=self.top_n_user_table,
                                 num_top_users=self.num_top_users)
        # pp.pprint("User counts per device:")
        # self.count_users_per_device()

        MyLog().getlogger().debug(f"Sleeping for {self.pause_time} secs")

    def get_num_logins_in_last_1_day(self, user_id):
        analytics_login_query_body = {
            "query": {
                "bool": {
                    "must": {
                        "range": {
                            "profile_info.last_login_time": {
                                "gte": "now-1d/d",
                                "lt": "now"
                            }
                        }
                    },
                    "filter": [
                        {
                            "term": {
                                "user_id": user_id
                            }
                        }
                    ]
                }
            }
        }

        entries = self.resMgr.search(self.user_login_table,
                                     search_param=analytics_login_query_body,
                                     raw=True)

        return len(entries)

    def create_table(self, table_name, body={}):
        if self.resMgr.index_exist(table_name) is False:
            MyLog().getlogger().debug(f"Creating {table_name}")
            self.resMgr.create(table_name, body)

    # Not used
    def get_user_analytics(self):
        pass
        # cnt = len(self._db.search_with_filters(self.user_profile_table,
        #                                        {'profile_data.interest': '6c3737766f677831676b7a71'}))
        # print(cnt)

    def count_users_per_interest(self, table_name='analytics_interests_count'):
        counters = self.resMgr.aggregate_counter(self.user_profile_table,
                                                 'profile_data.interest')

        # Return interest in descending order of user counts
        self.users_per_interest_datasets = sorted(counters.items(), key=lambda x: x[1], reverse=True)
        # print(self.users_per_interest_datasets)

        # Make sure Previous data is purged.
        try:
            self.resMgr.delete(table_name, force=True)
        except:
            pass

        for key, value in self.users_per_interest_datasets:
            # if key is None or empty ignore it.
            if key is None or key == "":
                continue

            value = {"keyword": key, "interest": value}

            MyLog().getlogger().debug(f"Pushing key = {key}, value = {value}")
            self.resMgr.add(table_name, key, value)

        MyLog().getlogger().debug(f"User Interest count done")

    def compute_aggregated_feed_counts(self, table_name='analytics_item_info_table'):
        datasets = self.resMgr.aggregate_counter(self.user_activity_table,
                                                 'activity.item_id',
                                                 {'activity.activity_info.liked': True,
                                                  'activity.activity_info.disliked': True,
                                                  'activity.activity_info.shared': True})

        # Make sure Previous data is purged.
        try:
            self.resMgr.delete(table_name, force=True)
        except:
            pass

        for key, value in datasets.items():
            MyLog().getlogger().debug(f"Pushing key = {key}, value = {value}")
            self.resMgr.add(table_name, str(key), value)

    def compute_aggregated_user_activity(self):
        return self.resMgr.aggregate_counter(self.user_activity_table, 'user_id',
                                             {'activity.activity_info.liked': True,
                                              'activity.activity_info.disliked': True,
                                              'activity.activity_info.shared': True})

    def compute_aggregated_user_chat_activity(self):
        return self.resMgr.aggregate_counter(self.user_chat_table, 'user_id',
                                             {'chat_info.group_list': None,
                                              'chat_info.peer_list': None})

    def count_users_per_device(self):
        return self.resMgr.aggregate_counter(self.user_profile_table,
                                             'device_data.device_id',
                                             {'user_id': None})

    def compute_average_feed_time(self, table_name='analytics_item_info_table'):
        datasets = self.resMgr.aggregate_counter(self.user_activity_table,
                                                 'activity.item_id',
                                                 {'activity.activity_info.tot_dur': None})
        # pprint.pprint(datasets)
        # out expected as dictionary of  items with array of total duration
        # calculate average for each entry

        # Make sure Previous data is purged.
        try:
            self.resMgr.delete(table_name, force=True)
        except:
            pass

        # Make sure user count table exist
        item_time_list = dict()
        for key, value in datasets.items():
            value = value['activity.activity_info.tot_dur']
            average = sum(value) / len(value)
            value = {"avg_time_spent": average}
            MyLog().getlogger().debug(f"Pushing key = {key}, value = {value}")
            item_time_list[str(key)] = value
            self.resMgr.add(table_name, str(key), value)

    #
    # Algorithm here is simple.
    # top n users are those who gets maximum points.
    # points are calculated based of following
    #  Total points per users =
    #         upvotes + downvotes + shared + Number of Personal Chat
    #         + Number of Group Chat
    #
    def compute_top_n_users(self, pp, table_name='analytics_global_info_table', num_top_users=5):
        # Algorithm:
        #   Following Steps needs to be executed to find the top users
        # FOR EACH USER
        #   Step 1:
        #       Calculate total points for ups + down + shared items * weights for each
        #   Step 2:
        #   Step 3:
        #   Step 4:

        # Make sure Previous data is purged.
        try:
            self.resMgr.delete(table_name, force=True)
        except:
            pass

        #
        # Global Dictionary to track points for each user
        # each steps will add its points in this dictionary for each user
        # at the end, top N will be selected
        user_data = dict()

        #
        # STEP 1:
        #   Table: DEFAULT_USER_ACTIVITY_INDEX
        #   Calculate for each user -> total points for up,down,shared votes
        user_activity_votes = self.compute_aggregated_user_activity()

        # pp.pprint("Displaying user_activity_votes")
        # pp.pprint(user_activity_votes)
        # pp.pprint("Displaying user_activity_votes DONE ")
        weight = 1
        user_id_list = []

        for user_id, like_dislike_shared_values in user_activity_votes.items():
            user_data[user_id] = 0
            user_id_list.append(user_id)

            total_points = weight * (like_dislike_shared_values['activity.activity_info.disliked'] +
                                     like_dislike_shared_values['activity.activity_info.liked'] +
                                     like_dislike_shared_values['activity.activity_info.shared'])
            user_data[user_id] += total_points

        #
        # STEP 2:
        #   For user track chatting list
        user_activity_chat = self.compute_aggregated_user_chat_activity()
        # pp.pprint(user_activity_chat)
        weight_indv_chat = 0.9
        weight_grp_chat = 0.1
        for user_id, values in user_activity_chat.items():
            if user_id is not user_data.keys():
                user_data[user_id] = 0

            total_points = weight_grp_chat * len(values['chat_info.group_list']) + \
                           weight_indv_chat * len(values['chat_info.peer_list'])
            user_data[user_id] += total_points
        # pp.pprint(user_data)

        #
        # STEP 3:
        #   Number of times users logged in
        #   Increment number of last 1 days logins
        #   to total points.
        for user_id in user_id_list:
            num_logins = self.get_num_logins_in_last_1_day(user_id)
            user_data[user_id] += num_logins

        #
        # STEP 4:
        #   Based of Popular Interest
        #   Weights are given to top 4 most popular interests
        # §  Top 1st = W1  = 1
        # §  Top 2st = W2 = 0.9
        # §  Top 3rd  = W3 = 0.7
        # §  Rest All = W4 = 0.5
        #   For each user find the top most interest where it spent most of its time.
        #      total_points = time_spend_on_top_most interest * Weight for this
        #                                                       interest in popular list
        # default weights
        weight = [1, 0.9, 0.7, 0.5]
        default_weight = 0.4
        # print(self.users_per_interest_datasets)

        #   Create dictionary of most popular interest and its
        #   corresponding weights
        interest_weights = dict()
        count = 0
        for interest_pair in self.users_per_interest_datasets:
            interest_weights[interest_pair[0]] = weight[count]
            count = count + 1
            if count == 4:
                break
        #
        #   Calculate For each user which item it spent most of its time
        user_item_interest = self.resMgr.aggregate_counter(self.user_activity_table,
                                                           'user_id',
                                                           {'activity.item_id': None,
                                                            'activity.activity_info.tot_dur': None})
        # pp.pprint(user_item_interest)
        # pp.pprint("*****************")
        # pp.pprint(user_item_interest.items())
        # pp.pprint("*****************")

        for user_id, user_item_data_set in user_item_interest.items():
            item_duration = dict()

            # item_duration dictionary
            # of key being item_id and value = total_duration
            for i in range(len(user_item_data_set['activity.item_id'])):
                item_duration[user_item_data_set['activity.item_id'][i]] = \
                    user_item_data_set['activity.activity_info.tot_dur'][i]

            sorted_items_list = sorted(item_duration.items(), key=lambda x: x[1], reverse=True)
            # pp.pprint("==============")
            # item_id, total_duration
            # pp.pprint(sorted_items_list)
            # pp.pprint("==============")

            # find the weight for the first entry in sorted_item_list
            if len(sorted_items_list) > 0:
                my_popular_interest_item_id = sorted_items_list[0][0]

                if my_popular_interest_item_id in interest_weights.keys():
                    weight = interest_weights[my_popular_interest_item_id]
                else:
                    weight = default_weight
            else:
                weight = default_weight

            total_points = weight * sorted_items_list[0][1]
            user_data[user_id] += total_points

        # print(user_data)
        #
        #  FINAL STEP:
        #       Calculate top N users
        sorted_data = sorted(user_data.items(), key=lambda x: x[1], reverse=True)
        # pp.pprint(sorted_data)
        top_users_list = []
        num_top_users = min(num_top_users, len(sorted_data))
        for i in range(num_top_users):
            top_users_list.append(sorted_data[i][0])
            # pp.pprint(sorted_data[i])

        value = {'top_users': top_users_list}
        MyLog().getlogger().debug(f"{value}")
        self.resMgr.add(table_name, "top_users", value)
