import argparse
import re

def getTransactionsList(data):
  transactions = []

  for htmlLine in data:
    entries = htmlLine.split(';')
    del entries[0] # Remove Reskontradatum
    if (len(entries)>1):
      transaction=[]

      for entry in entries:
        es = stripHtml(entry)
        if (es != ""):
          transaction.append(es)

      transactions.append(list(filter(None, transaction)))
    transactions = list(filter(None, transactions))
  transactions.sort(reverse=True)
  return transactions

def stripHtml(entry):
  es = re.findall('\>.*?\<',entry) 
  while ("><" in es):
    es.remove("><")
  for n,i in enumerate(es):
    es[n] = i[1:-1]
  return es[0] if len(es) > 0 else ""

def parseArgs():
  parser = argparse.ArgumentParser(description='Converts a Handelsbanken Excel file to YNAB friendly CSV')
  parser.add_argument('-i','--input', help='The input file name', required=True)
  parser.add_argument('-o','--output', help='The output file name', required=True)
  return parser.parse_args()
  
def main():
  args = parseArgs()
  input = args.input
  output = args.output
  print("Converting " + input + " to " + output + "\n")
  
  with open (input) as inputFile:
    data = inputFile.readlines()

  transactions = getTransactionsList(data)

  open(output, 'w').close()
  with open(output, 'a') as outputFile:
    outputFile.write("Date,Payee,Category,Memo,Outflow,Inflow\n")
    for t in transactions[1:]:
      outputFile.write(t[0]+","+t[1]+",,,")
      flow = float(t[2].replace(',','.').replace(' ',''))
      if (flow < 0):
        outputFile.write(str(abs(flow))+",")
      else:
        outputFile.write(",")
        outputFile.write(str(flow))
      outputFile.write("\n")
      print("Added    "+str(t))
  
  print("\nFinished converting "+input+"\nOutput file is "+output)

main()