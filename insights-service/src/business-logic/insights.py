from common_modules.storage.storage_elastic import StorageElastic


# index2 = 'user_profile_data_etl_1'
# y = db.search(index2, {'user_id': 18})

class Insights:
    def __init__(self):
        self._db = StorageElastic()
        self._user_activity_index = "user_activity_data_etl_1"

    def get_user_insights(self, user_id: int):
        read_cnt = len(self._db.search_with_filters(self._user_activity_index, {'user_id': user_id}))
        if read_cnt == 0:
            return 0, 0, 0
        saved_cnt = len(self._db.search_with_filters(self._user_activity_index,
                                        {'user_id': user_id, 'activity.activity_info.saved': True}))
        liked_cnt = len(self._db.search_with_filters(self._user_activity_index,
                                        {'user_id': user_id, 'activity.activity_info.liked': True}))
        return read_cnt, saved_cnt, liked_cnt


if __name__ == '__main__':
    insights = Insights()
    for user_id in range(16):
        read, saved, liked = insights.get_user_insights(user_id=user_id)
        print(f'user_id:{user_id}, read:{read}, saved:{saved}, liked:{liked}')
