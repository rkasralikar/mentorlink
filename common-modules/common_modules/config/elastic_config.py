###################
#   Credentials   #
###################
"""
Credentials is also used in kibana.yml
"""
server_port = 5601
remote_host = 'https://mentorlink-dl-staging.es.us-west-2.aws.found.io'
remote_port = 9243
username = 'ml-es'
password = 'es_ment0r_link'
cluster_name = 'mentorlink-dl-staging'

####################
#    Index Info    #
####################
DEFAULT_USER_ACTIVITY_INDEX = 'user_activity_data_etl_1'
DEFAULT_USER_PROFILE_INDEX = 'user_profile_data_etl_0'
DEFAULT_USER_CHAT_INDEX = 'user_chat_analytics_etl_0'
DEFAULT_ITEM_NORMALIZED_INDEX = 'item_normalization_table_etl'

index_info = {
    DEFAULT_USER_ACTIVITY_INDEX: {
        'desc': 'Index to store user activity data.'
        # More fields TBD
    },
    DEFAULT_USER_PROFILE_INDEX: {
        'desc': 'Index to store user profile.'
        # More fields TBD
    }
}


def get_index_desc(index: str):
    return index_info[index]['desc']
