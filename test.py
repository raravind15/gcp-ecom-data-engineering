# # class customer:
# #     def __init__(self,name,age):
# #         self.name=name
# #         self.age=age

# class customer:
#         name=""
#         age=0
#         def set_info(name):
#                 customer.name=name
                

# # cust1=customer("aravind",31)
# # cust2=customer("Priya",29)
# cust1=customer()
# cust1.name=cust1.set_info("Aravind")
# cust2=customer()
# # cust2.name=cust2.set_info("Priya")

# print(cust1.name,cust2.name)


#  job_config = bigquery.QueryJobConfig()
#  param1=bigquery.ScalarQueryParameter(
#                 "file_name",
#                 "STRING",
#                 file_name
#             )
#  job_config.query_parameters=[param1]

# docker run --rm -p 8080:8080 ^
# -v "%APPDATA%\gcloud:/root/.config/gcloud" ^
# -e GOOGLE_APPLICATION_CREDENTIALS=/root/.config/gcloud/application_default_credentials.json ^
# -e GOOGLE_CLOUD_PROJECT=di-dev-aravind ^
# -e SOURCE_BUCKET=aravind-de-dev-aravind-source-asia-south1 ^
# -e LANDING_BUCKET=aravind-de-dev-landing-asia-south1 ^
# src_to_land_gcs:v3



# docker run --rm -p 8080:8080 ^
# -v "%APPDATA%\gcloud:/root/.config/gcloud" ^
# -e GOOGLE_APPLICATION_CREDENTIALS=/root/.config/gcloud/application_default_credentials.json ^
# -e GOOGLE_CLOUD_PROJECT=di-dev-aravind ^
# -e SOURCE_BUCKET=aravind-de-dev-aravind-source-asia-south1 ^
# -e LANDING_BUCKET=aravind-de-dev-landing-asia-south1 ^
# src_to_land_gcs:latest






def star(func):

    def wrapper():
        print("*****")
        func()
        print("*****")

    return wrapper


@star
def welcome():
    print("Welcome")


welcome()