fields = ['Word','Occurances']
    
with open("tokens.csv",'w') as tokens_csv:
    writer = csv.DictWriter(tokens_csv,fieldnames=fields)

    writer.writeheader()

    writer.writerows(TOKENS_DICTIONARY)