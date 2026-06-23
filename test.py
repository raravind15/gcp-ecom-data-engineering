# class customer:
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

class customer:
        name=""
        age=0
        def set_info(name):
                customer.name=name
                

# cust1=customer("aravind",31)
# cust2=customer("Priya",29)
cust1=customer()
cust1.name=cust1.set_info("Aravind")
cust2=customer()
# cust2.name=cust2.set_info("Priya")

print(cust1.name,cust2.name)


 job_config = bigquery.QueryJobConfig()
 param1=bigquery.ScalarQueryParameter(
                "file_name",
                "STRING",
                file_name
            )
 job_config.query_parameters=[param1]