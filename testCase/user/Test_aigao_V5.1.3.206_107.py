from common import common


adx_xls = common.get_xls("adx.xlsx", "adx")
file = adx_xls[7][3]
filepath = common.download_js(file)
print("test js file path is ",filepath)
Hash = common.gethash(filepath)
print("Hash is ",Hash)
if Hash == "905d599984d54e9d32678a278199bd7f51135553":
    print("Hash test is pass.")
else:
    print("Hash test is fail.")
