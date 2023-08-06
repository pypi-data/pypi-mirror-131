import random
import string
import os
from zipfile import ZipFile


def enc(content):
  z = 0
  while z == 0:
    z = random.randint(1,11)
  cypher = {}
  cy = ""
  zero = ""
  neo = ""
  
  for i in range(z):
    zero += "0"
  #print(zero)
  temp_zero = zero
  total = list(string.ascii_lowercase)
  for item in string.ascii_uppercase:
    total.append(item)
  for alpha in total:
    cy = f"1{zero}1"
    cypher[alpha] = cy
    zero += "0"
  for value in string.punctuation:
    cy = f"1{zero}1"
    cypher[value] = cy
    zero += "0"

  
  cypher[" "] = "1010101010101"
  lines = content
  for line in lines:
    for word in line:
      for letter in word:
        neo += cypher[letter]




  return f"1{temp_zero}1{neo}"

def build_cypher(zero):
  cypher = {}
  cypher[" "] = "000Space000"
  cy = ""
  total = list(string.ascii_lowercase)
  for item in string.ascii_uppercase:
    total.append(item)
  for alpha in total:
    cy = f"1{zero}1"
    cypher[alpha] = cy
    zero += "0"
  for value in string.punctuation:
    cy = f"1{zero}1"
    cypher[value] = cy
    zero += "0"
  
  return cypher

def get_alpha(tof,cypher):
  if tof == "000Space000":
    return " "

  for alpha in cypher:
    if cypher[alpha] == f"1{tof}1":
      return alpha
  return ""

def dec(content):
  content = content.replace("1010101010101","000Space000")
  neo = ""
  con = content
  con = con.replace("11","1")
  con = con.split("1")
  con.remove("")
  con.remove(con[len(con)-1])
  zero = con[0]

  
  con.remove(zero)

  content = content.replace(f"1{zero}1","")
  cypher = build_cypher(zero)
  
  z = ""
  found = False
  content = content.replace("11","1")
  for val in con:
    neo += get_alpha(val,cypher)
  return neo



def enc_file(file,out):
  with open(f"{os.getcwd()}/{file}","r") as x:
    content = x.read()
  content = content.replace("\n","")
  tr = enc(content)
  os.system(f"touch {os.getcwd()}/{out}.elm")
  with open(f"{os.getcwd()}/{out}.elm","w") as elm:
    elm.write(tr)

def dec_file(file,out):
  with open(f"{os.getcwd()}/{file}.elm","r") as x:
    content = x.read()
  content.replace("1010101010101","000Space000")
  content = content.replace("\n","")
  os.system(f"touch {os.getcwd()}/{out}")
  with open(f"{os.getcwd()}/{out}","w") as elm:
    elm.write(dec(content))

# add support for \n later

def build_elm(neo,out):
  with ZipFile(f"{out}.zip","w") as zip:
    zip.write(f"{out}.elm")

def open_elm(file,out):
  unzipped_file = ZipFile(f"{file}.zip", "r")
  con = unzipped_file.read(f"{out}.elm")
  con = con.decode("utf-8")
  return con


