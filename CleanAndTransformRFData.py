#Clean and transform radio frequency data for further data validation and loading into db
import pandas as pd
import datetime as dt


def roundField(value):
    n = 0

    if (100 > value >= -10):
        n = 4
    elif ((1000 > value >= 100) | (-10 >= value > -100)):
        n = 3
    elif ((10000 > value >= 1000) | ((-100 >= value > -1000))):
        n = 2
    elif (100000 > value >= 10000 | (-1000 >= value > -10000)):
        n = 1
    else: n = 0
    return (round(value, n))

marketSIDName = "Market SID"
switchNumber = "Switch Number"
siteNumber = "Site Number"
sector = "Sector"
TCT = "Trans-Cell Type"
technology = "Technology"
mcc = 'MCC'
mnc = 'MNC'
ecgi = 'ECGI'
lteMarket = 'LTE Market'
totalEIRPName = "LTE Total EIRP (W)"
pilotERP = "Pilot ERP (W)"
Azimuth = "Azimuth (deg)"
antModel = "Antenna Model"
antManufact = "Antenna Manufacturer"
antCenterline = "Antenna Centerline (ft)"
antMG = "Antenna Max Gain (dBd)"
mechTilt = "Mechanical Tilt (deg)"
address = "E-911 Street Address"




# Read the file
fileName = 'vzw_atoll/national_e911.csv'
try:
    data = pd.read_csv(fileName, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
except:
    data = pd.read_csv(fileName, sep=",", skip_blank_lines=True, skipinitialspace=True, error_bad_lines=False,
                       index_col=False, dtype='unicode')

data.info()

#ECGI to lowercase
print("{0}: {1}".format(ecgi, data[ecgi].head()))
data = data.sort_values(by=[ecgi])

data.loc[(~data[ecgi].isna()), ecgi] = data.loc[(~data[ecgi].isna()), ecgi].astype('str')
data.loc[(~data[ecgi].isna()), ecgi] = data.loc[(~data[ecgi].isna()), ecgi].map(lambda x: str.lower(x))
print("{0}: {1}".format(ecgi, data[ecgi].head()))

#Addres formatting
data.loc[(~data[address].isna()), address] = data.loc[(~data[address].isna()), address].astype('str')
data.loc[(~data[address].isna()), address] = data.loc[(~data[address].isna()), address].map(lambda x: str.upper(x))
data.loc[(~data[address].isna()), address] = data.loc[(~data[address].isna()), address].map(lambda x: str.strip(x))

data.loc[(~data[address].isna()), address] = data.loc[(~data[address].isna()), address].map(lambda x: x.replace('STREET', 'ST'))
data.loc[(~data[address].isna()), address] = data.loc[(~data[address].isna()), address].map(lambda x: x.replace('ROAD', 'RD'))

# Round totalEIRPName to desired numbers of digits after point
data[totalEIRPName] = pd.to_numeric(data[totalEIRPName], errors='coerce')
data[totalEIRPName] = data[totalEIRPName].astype('float64')
data[totalEIRPName] = data[totalEIRPName].map(lambda x: roundField(x))
print("{0}: {1}".format(totalEIRPName, data[totalEIRPName].unique()))

print("\n{0}: {1}".format(pilotERP, data[pilotERP].unique()))
data[pilotERP] = pd.to_numeric(data[pilotERP], errors='coerce')
data[pilotERP] = data[pilotERP].astype('float64')
data[pilotERP] = data[pilotERP].map(lambda x: roundField(x))
print("{0}: {1}".format(pilotERP, data[pilotERP].unique()))

# Round Azimuth to whole number
data[Azimuth] = pd.to_numeric(data[Azimuth], errors='coerce')
data[Azimuth] = data[Azimuth].astype('float64')
data[Azimuth] = round(data[Azimuth], 0)
print(data[Azimuth].unique())

# Populate blanks with 'unknown" for Antenna Model and Antenna Manufacturer
data[antModel].fillna("unknown", inplace=True)
print(data[antModel].unique())

data[antManufact].fillna("unknown", inplace=True)
print(data[antManufact].unique())

# Round Antenna Max Gain to desired numbers of digits after a point
data[antMG] = pd.to_numeric(data[antMG], errors='coerce')
data[antMG] = data[antMG].astype('float64')
data[antMG] = data[antMG].map(lambda x: roundField(x))
print(data[antMG].unique())

#Round Antenna Centerline till 2 digits after a point
data[antCenterline] = pd.to_numeric(data[antCenterline], errors='coerce')
data[antCenterline] = data[antCenterline].astype('float64')
data[antCenterline] = round(data[antCenterline], 2)
print(data[Azimuth].unique())

# Fill blank MCC and MNC with 311 and 480  accordingly
data[mcc].fillna(311, inplace=True)
print("{0}: {1}".format(mcc, data[mcc].unique()))

data[mnc].fillna(480, inplace=True)
print("{0}: {1}".format(mnc, data[mnc].unique()))

data[mechTilt] = pd.to_numeric(data[mechTilt], errors='coerce')
data[mechTilt] = data[mechTilt].astype('float64')
data[mechTilt] = round(data[mechTilt], 0)
print("{0}: {1}".format(mechTilt, data[mechTilt].unique()))

# create Eran Data
eranData = data[data[TCT].isin(['E-RAN'])]


# create LTE and CDMA data files
lteData = data[(data[technology].isin(['LTE']) | data[technology].isin(['5G'])) & ~data[TCT].isin(['E-RAN'])]
lteData = lteData.append(data[data[technology].isna() & ((~data[totalEIRPName].isna()) | (~data[ecgi].isna()) | (~data[lteMarket].isna()))],
               ignore_index=True)


cdmaData = data[data[technology].isin(['CDMA']) & (~data[TCT].isin(['E-RAN']))]
cdmaData = cdmaData.append(data[data[technology].isna() & data[totalEIRPName].isna() & data[ecgi].isna() & data[lteMarket].isna()],
               ignore_index=True)
cdmaData = cdmaData.sort_values(by=[marketSIDName, switchNumber, siteNumber, sector])
# Calculate control sum:
print("ERAN {0} + LTE {1} + CDMA {2} = {3}".format(len(eranData), len(lteData), len(cdmaData),
                                                   len(eranData) + len(lteData) + len(cdmaData)))
print("All data: {0}".format(len(data)))


#Clean data and write it to files
today = dt.datetime.now().strftime("%y%m%d")
eranData.to_csv('../output/ERAN_V0000_{0}.csv'.format(today), sep=',', encoding='utf-8', index=False)
print("Eran data saved to ERAN_V0000_{0}.csv file.".format(today))

lteData.to_csv('../output/LTE_V0000_{0}.csv'.format(today), sep=',', encoding='utf-8', index=False)
print("LTE data saved to LTE_V0000_{0}.csv".format(today))

cdmaData.to_csv('../output/CDMA_V0000_{0}.csv'.format(today), sep=',', encoding='utf-8', index=False)
print("CDMA data saved to CDMA_V0000_{0}.csv".format(today))


