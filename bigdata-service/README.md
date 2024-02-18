For Big data

1. Create docker image:

    $ docker build --no-cache --tag big-data --build-arg etl_list=<etl-list> --build-arg log_level=<log-level debug|error|info|critical> --build-arg freq=<frequency of etl runs in sec> --build-arg start_rest_server=<start the rest server, dont provide this option if you do not want to run the rest server> .

    Example:
    ============


    $ docker build --no-cache --tag big-data-user --build-arg etl_list="config_user_profile.json config_user_activity.json" --build-arg log_level="error" --build-arg freq=100 --build-arg start_rest_server="True" .


    $ docker build --no-cache --tag big-data-youtube --build-arg etl_list="config_youtube.json" --build-arg log_level="error" --build-arg freq=100 .

2. Run the docker container with the above image

        $ docker run --rm --name bigdata -d --network="host" big-data

3. Current runs:

    3.1 On bayes.mentorlink.ai:

   Rest Server:

        docker build --no-cache --tag big-data-rest --build-arg rest_server_config_file="config_rest_server.json" --build-arg log_level="error" .
        docker run --rm --name bigdata-rest -d --network="host" big-data-rest

   User Profile:

         docker build --no-cache --tag big-data-user --build-arg etl_list="config_user_profile.json" --build-arg log_level="error" --build-arg freq=600 .
         docker run --rm --name bigdata-user -d --network="host" big-data-user

   Youtube Item Normalization:

         docker build --no-cache --tag big-data-youtube --build-arg etl_list="config_youtube.json" --build-arg log_level="error" --build-arg freq=28800 .
         docker run --rm --name bigdata-youtube -d --network="host" big-data-youtube

   RSS Item Normalization :

         docker build --no-cache --tag big-data-rss --build-arg etl_list="config_rss.json" --build-arg log_level="error" --build-arg freq=7200 .
         docker run --rm --name bigdata-rss -d --network="host" big-data-rss

    Kafka Consumer:

         docker build --no-cache --tag big-data-kafka --build-arg kafka_config_file="config_kafka_topics.json" --build-arg log_level="debug" .
         docker run --rm --name bigdata-kafka -d --network="host" big-data-kafka

    3.2 on AWS:

   Rest Server (AWS):

        docker build --no-cache --tag big-data-rest --build-arg rest_server_config_file="config_aws_rest_server.json" --build-arg log_level="error" .
        docker run --rm --name bigdata-rest -d --network="host" big-data-rest

    User Profile:

        docker build --no-cache --tag big-data-user --build-arg etl_list="config_aws_user_profile.json config_aws_user_activity.json" --build-arg log_level="error" --build-arg freq=600 --build-arg start_rest_server="True" .
	     docker run --rm --name bigdata-user -d --network="host" big-data-user

    Youtube Item Normalization: 

        docker build --no-cache --tag big-data-youtube --build-arg etl_list="config_youtube.json" --build-arg log_level="error" --build-arg freq=28800 .
        docker run --rm --name bigdata-youtube -d --network="host" big-data-youtube

    RSS Item Normalization :

         docker build --no-cache --tag big-data-rss --build-arg etl_list="config_rss.json" --build-arg log_level="error" --build-arg freq=7200 .
         docker run --rm --name bigdata-rss -d --network="host" big-data-rss
    
    StackOverflow Item Normalization: 

        docker build --no-cache --tag big-data-stackoverflow --build-arg etl_list="config_stackoverflow.json" --build-arg log_level="error" --build-arg freq=28800 .
        docker run --rm --name bigdata-stackoverflow -d --network="host" big-data-stackoverflow
   
    Meetup Item Normalization: 

        docker build --no-cache --tag big-data-meetup --build-arg etl_list="config_meetup.json" --build-arg log_level="error" --build-arg freq=28800 .
        docker run --rm --name bigdata-meetup -d --network="host" big-data-meetup
