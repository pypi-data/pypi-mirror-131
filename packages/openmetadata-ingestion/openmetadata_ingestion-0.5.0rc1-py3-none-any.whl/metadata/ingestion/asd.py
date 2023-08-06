from sqlalchemy import create_engine

engine = create_engine(
            "snowflake://test_openmetadata:Welcome123%21@yq17661.us-east-2.aws.snowflakecomputing.com?account=YQ17661",
            connect_args={
                'authenticator': 'externalbrowser',
                }
            )
connection = engine.connect()