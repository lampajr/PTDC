"""
Data module provides default dictionary that are used by the default collectors,
representing which features/attributes are collected from users and statuses

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""

from ptdc.support import get_attribute, get_date, get_media, get_quoted_user_id, get_retweeted_status, get_retweeted_user_id
from functools import reduce


default_account_features = {"id": get_attribute,
                            "name": get_attribute,
                            "screen_name": get_attribute,
                            "location": get_attribute,
                            "url": get_attribute,
                            "description": get_attribute,
                            "protected": get_attribute,
                            "verified": get_attribute,
                            "followers_count": get_attribute,
                            "friends_count": get_attribute,
                            "listed_count": get_attribute,
                            "favourites_count": get_attribute,
                            "statuses_count": get_attribute,
                            "created_at": get_attribute,
                            "utc_offset": get_attribute,
                            "time_zone": get_attribute,
                            "geo_enabled": get_attribute,
                            "lang": get_attribute,
                            "contributors_enabled": get_attribute,
                            "profile_background_color": get_attribute,
                            "profile_background_image_url": get_attribute,
                            "profile_background_image_url_https": get_attribute,
                            "profile_background_tile": get_attribute,
                            "profile_image_url": get_attribute,
                            "profile_image_url_https": get_attribute,
                            "profile_link_color": get_attribute,
                            "profile_text_color": get_attribute,
                            "profile_use_background_image": get_attribute,
                            "default_profile": get_attribute,
                            "default_profile_image": get_attribute,
                            "profile_crawled": lambda x, y: get_date(),
                            "is_suspended": lambda x, y: 0,
                            "following_followers_ratio": lambda user, _: user.friends_count / user.followers_count if user.followers_count != 0 else None,
                            "followers_following_ratio": lambda user, _: user.followers_count / user.friends_count if user.friends_count != 0 else None}


default_account_timeline_features = {"n_statuses_collected": lambda statuses_data, _: statuses_data.shape[0],
                                     "mean_status_length": lambda statuses_data, _: statuses_data["text_length"].mean(),
                                     "media_shared_urls": lambda statuses_data, _: reduce(lambda x,y: x+y, [], [x for x in statuses_data["media_urls"] if x is not None]),
                                     "mean_shared_media": lambda statuses_data, _: (len(reduce(lambda x,y: x+y, [], [x for x in statuses_data["media_urls"] if x is not None])) / statuses_data.shape[0]) if statuses_data.shape[0] != 0 else None,
                                     "quoted_user_ids": lambda statuses_data, _: [x for x in statuses_data["quoted_user_id"] if x is not None],
                                     "replied_status_ids": lambda statuses_data, _: [x for x in statuses_data["in_reply_to_status_id"] if x is not None],
                                     "replied_user_ids": lambda statuses_data, _: [x for x in statuses_data["in_reply_to_user_id"] if x is not None],
                                     "retweeted_status_ids": lambda statuses_data, _: [x for x in statuses_data["retweeted_status"] if x is not None],
                                     "retweeted_user_ids": lambda statuses_data, _: [x for x in statuses_data["retweeted_user_id"] if x is not None]}


default_statuses_features = {"id": get_attribute,
                             "created_at": get_attribute,
                             "full_text": get_attribute,
                             "lang": get_attribute,
                             "coordinates": get_attribute,
                             "retweet_count": get_attribute,
                             "favorite_count": get_attribute,
                             "source": get_attribute,
                             "place": get_attribute,
                             "truncated": get_attribute,
                             "is_quote_status": get_attribute,
                             "in_reply_to_status_id": get_attribute,
                             "in_reply_to_user_id": get_attribute,
                             "in_reply_to_screen_name": get_attribute,
                             "user_id": lambda status, _: status.user.id,
                             "text_length": lambda status, _: len(status.full_text),
                             "hashtags": lambda status, _: [ht["text"] for ht in status.entities["hashtags"]],
                             "media_urls": lambda status, _: get_media(status),
                             "quoted_user_id": lambda status, _: get_quoted_user_id(status),
                             "retweeted_status": lambda status, _: get_retweeted_status(status),
                             "retweeted_user_id": lambda status, _: get_retweeted_user_id(status)}
