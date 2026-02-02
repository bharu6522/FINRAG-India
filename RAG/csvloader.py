from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path= r"D:\Pinnacle_WorkSpace\CSC_SPV\VenturaSecurities\Data\cob_leads_data_v1\cob_leads_part2_jan2025_sep2025_decr.csv",
                   encoding= 'utf-8')
docs = loader.load()

# print(len(docs))

print(docs[0])