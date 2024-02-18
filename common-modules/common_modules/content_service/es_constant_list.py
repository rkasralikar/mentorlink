######################
# All Mappings go here
######################

linkedin_user_profile_urls_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "linkedin_profile_id": {
                "type": "keyword"
            },
            "is_scraped": {
                "type": "boolean"
            },
            "created": {
                "type": "date"
            }
        }
    }
}

linkedin_user_profile_urls_mapping_rev2 = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "linkedin_profile_id": {
                "type": "keyword"
            },
            "is_scraped": {
                "type": "boolean",
                "null_value": False
            },
            "is_available": {
                "type": "boolean",
                "null_value": True
            }
        }
    }
}

linkedin_user_profile_urls_mapping_rev3 = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "user_id": {
                "type": "unsigned_long"
            },
            "linkedin_profile_id": {
                "type": "keyword"
            },
            "is_scraped": {
                "type": "boolean",
                "null_value": False
            },
            "is_available": {
                "type": "boolean",
                "null_value": True
            },
            "tag": {
                "type": "text"
            }
        }
    }
}

linkedin_user_profile_data_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "url": {
                "type": "text"
            },
            "name": {
                "type": "text"
            },
            "about": {
                "type": "text"
            },
            "location": {
                "type": "text"
            },
            "experience": {
                "type": "object",
                "dynamic": True
            },
            "education": {
                "type": "object",
                "dynamic": True
            },
            "certs": {
                "type": "object",
                "dynamic": True
            },
            "skill_endorsements": {
                "type": "flattened"
            },
            "recommendations": {
                "type": "object",
                "dynamic": True
            },
            "accomplishments": {
                "type": "object",
                "dynamic": True
            },
            "interests": {
                "type": "flattened"
            }
        }
    }
}

linkedin_user_profile_data_mapping_rev2 = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "url": {
                "type": "text"
            },
            "name": {
                "type": "text"
            },
            "about": {
                "type": "text"
            },
            "location": {
                "type": "text"
            },
            "num_jobs": {
                "type": "integer"
            },
            "experience": {
                "type": "object",
                "dynamic": True
            },
            "education": {
                "type": "object",
                "dynamic": True
            },
            "certs": {
                "type": "object",
                "dynamic": True
            },
            "skill_endorsements": {
                "type": "flattened"
            },
            "recommendations": {
                "type": "object",
                "dynamic": True
            },
            "accomplishments": {
                "type": "object",
                "dynamic": True
            },
            "interests": {
                "type": "flattened"
            }
        }
    }
}

linkedin_user_profile_data_mapping_rev3 = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "user_id": {
                "type": "unsigned_long"
            },
            "url": {
                "type": "text"
            },
            "name": {
                "type": "text"
            },
            "about": {
                "type": "text"
            },
            "location": {
                "type": "text"
            },
            "num_jobs": {
                "type": "integer"
            },
            "experience": {
                "type": "object",
                "dynamic": True
            },
            "education": {
                "type": "object",
                "dynamic": True
            },
            "certs": {
                "type": "object",
                "dynamic": True
            },
            "skill_endorsements": {
                "type": "flattened"
            },
            "recommendations": {
                "type": "object",
                "dynamic": True
            },
            "accomplishments": {
                "type": "object",
                "dynamic": True
            },
            "interests": {
                "type": "flattened"
            },
            "tags": {
                "type": "flattened"
            }
        }
    }
}

linkedin_user_profile_data_mapping_rev4 = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "user_id": {
                "type": "unsigned_long"
            },
            "url": {
                "type": "text"
            },
            "name": {
                "type": "text"
            },
            "about": {
                "type": "text"
            },
            "location": {
                "type": "text"
            },
            "num_jobs": {
                "type": "integer"
            },
            "experience": {
                "type": "object",
                "dynamic": True
            },
            "education": {
                "type": "object",
                "dynamic": True
            },
            "certs": {
                "type": "object",
                "dynamic": True
            },
            "skill_endorsements": {
                "type": "flattened"
            },
            "recommendations": {
                "type": "object",
                "dynamic": True
            },
            "accomplishments": {
                "type": "object",
                "dynamic": True
            },
            "interests": {
                "type": "flattened"
            },
            "tags": {
                "properties": {
                    "search_keyword": {
                        "type": "text"
                    },
                    "skills_from_li": {
                        "type": "flattened"
                    }
                }
            }
        }
    }
}

resource_data_index_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "title": {
                "type": "text"
            },
            "url": {
                "type": "text"
            },
            "desc": {
                "type": "text"
            },
            "inst_list": {
                "type": "text"
            },
            "ratings": {
                "type": "double"
            },
            "num_reviews": {
                "type": "long"
            },
            "tot_time": {
                "type": "double"
            },
            "num_lecs": {
                "type": "text"
            },
            "level": {
                "type": "text"
            },
            "tags": {
                "type": "text"
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

resource_data_key_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "key": {
                "type": "text"
            },
            "is_scraped": {
                "type": "boolean"
            },
            "count": {
                "type": "long"
            }
        }
    }
}

test_data_index_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "title": {
                "type": "text"
            },
            "url": {
                "type": "text"
            },
            "desc": {
                "type": "text"
            },
            "inst_list": {
                "type": "text"
            },
            "ratings": {
                "type": "double"
            },
            "num_reviews": {
                "type": "long"
            },
            "tot_time": {
                "type": "double"
            },
            "num_lecs": {
                "type": "text"
            },
            "level": {
                "type": "text"
            },
            "tags": {
                "type": "text"
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

test_data_key_index_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "key": {
                "type": "text"
            },
            "is_scraped": {
                "type": "boolean"
            },
            "count": {
                "type": "long"
            }
        }
    }
}

##############################
# New Constants
# These are used for new data.
# This will have the 'URL' field.
##############################
LINKEDIN_URLS_I = 'linkedin_user_profile_urls'
LINKEDIN_URLS_REV2_I = 'linkedin_user_profile_urls_rev4'
LINKEDIN_DATA_I = 'linkedin_user_profile_data_rev4'
RESOURCE_DATA_I = 'resource_data_documents_rev1'
RESOURCE_DATA_KEY_I = 'resource_data_key_documents_rev1'
RESOURCE_DATA_MEETUP_I = 'resource_meetup_data_documents_rev1'
RESOURCE_DATA_MEETUP_KEY_I = 'resource_meetup_data_key_documents_rev1'
TEST_DATA_I = 'test_data_rev1'
TEST_DATA_KEY_I = 'test_data_key_rev1'

###############################
# New Linkedin Data Tables
###############################
LINKEDIN_USER_PROFILE_REV_5 = 'linkedin_user_profile_data_rev5'


LINKEDIN_URLS_M = linkedin_user_profile_urls_mapping_rev3
LINKEDIN_DATA_M = linkedin_user_profile_data_mapping_rev4
RESOURCE_DATA_M = resource_data_index_mapping
RESOURCE_DATA_KEY_M = resource_data_key_mapping
TEST_DATA_M = test_data_index_mapping
TEST_DATA_KEY_M = test_data_key_index_mapping

######################
# Queries
######################

PROFILE_NOT_SCRAPED_Q = {
    "from": 0,
    "query": {
        "bool": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "is_scraped": "true"
                            }
                        }
                    ]
                }
            }
        }
    },
    "sort": [
        {
            "created": {
                "order": "asc"
            }
        }
    ]
}

PROFILE_NOT_SCRAPED_Q_ORI = {
    "from": 0,
    "query": {
        "bool": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "is_scraped": "true"
                            }
                        },
                    ]
                }
            }
        }
    },
    "sort": [
        {
            "created": {
                "order": "asc"
            }
        }
    ]
}

RESKEY_NOT_SCRAPED_Q = {
    "query": {
        "bool": {
            "filter": [
                {"term": {"is_scraped": False}}
            ]
        }
    }
}

WRONG_LINKEDIN_URLS_Q = {
    "query": {
        "bool": {
            "should": [
                {
                    "wildcard": {
                        "linkedin_profile_id": "https://*.linkedin.com/jobs/*"
                    }
                },
                {
                    "wildcard": {
                        "linkedin_profile_id": "https://*.linkedin.com/company/*"
                    }
                },
                {
                    "wildcard": {
                        "linkedin_profile_id": "https://*.linkedin.com/school/*"
                    }
                },
                {
                    "wildcard": {
                        "linkedin_profile_id": "https://*.linkedin.com/feed/*"
                    }
                },
                {
                    "wildcard": {
                        "linkedin_profile_id": "https://*.linkedin.com/pulse/*"
                    }
                },
                {  # 22
                    "wildcard": {
                        "linkedin_profile_id": "*trk=people-guest_profile-result-card_result-card_full-click*"
                    }
                },
                {  # 1
                    "wildcard": {
                        "linkedin_profile_id": "*showcase*"
                    }
                },
                {  # 65
                    "wildcard": {
                        "linkedin_profile_id": "https://*.linkedin.com/pub/dir/*"
                    }
                },
            ]
        }
    }
}

MATCH_ALL_Q = {
    "query": {
        "match_all": {}
    }
}

REINDEX_URLS_Q = {
    "source": {
        "index": LINKEDIN_URLS_I,
        "_source": ["created", "linkedin_profile_id"]
    },
    "dest": {
        "index": LINKEDIN_URLS_REV2_I
    }
}

TIMESTAMP_DATA_Q = {
    "query": {
        "range": {
            # "@timestamp": {
            "updated": {
                "gte": "2021-03-23T10:33:49",
                "lt": "2021-03-23T10:38:44"
            }
        }
    },
    "sort": [
        {
            "created": {
                "order": "asc"
            }
        }
    ]
}

URLS_SCRAPED_Q = {
    "query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "is_scraped": True}
                }
            ]
        }
    }
}

SPECIFIC_Q = {
    "query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "linkedin_profile_id": "https://www.linkedin.com/in/russell-fredrickson-5a450aa"
                    }
                }
            ]
        }
    }
}
