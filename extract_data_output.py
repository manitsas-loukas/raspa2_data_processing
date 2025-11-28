from RASPA2.output_parser import parse
import json
import pandas as pd


filename = [
'output_IRMOF-1_1.1.1_298.000000_100000.data',
'output_IRMOF-1_1.1.1_298.000000_500000.data',
'output_IRMOF-1_1.1.1_298.000000_1e+06.data',
'output_IRMOF-1_1.1.1_298.000000_2e+06.data',
'output_IRMOF-1_1.1.1_298.000000_5e+06.data',
'output_IRMOF-1_1.1.1_298.000000_1e+07.data'
        ]

mofs = [
'IRMOF-1'
        ]

press = [
'1bar',
'5bar',
'10bar',
'20bar',
'50bar',
'100bar'
        ]


#### Μετατροπή το output file σε purse
#i --> filename, press
#j --> IRMOF-1
infos=[]
for i in range(0, len(filename)):
    for j in range(0,len(mofs)):
        with open(f"./{mofs[j]}_{press[i]}/Output/System_0/{filename[i]}") as f:
            info = parse(f.read()) # --> dictionary
            infos.append(info)

'''
Εξετάζω τα αποτελέσματα
print(info['Number of molecules']['methane']['Average loading absolute [mol/kg framework]'])
# θα μπορούσα να το γράψω ως εξής
#list(info["Number of molecules"].keys())[0]
#loading_abs = info["Number of molecules"][molecule_name]["Average loading absolute [mol/kg framework]"][0]
'''
avg_load = []
unit_load = 'cm3 methane /cm3 MOF'
enthalpy = []
unit_enth = 'K'
avg_energy = []
unit_ener = 'K'


for i in range(0, len(infos)):
    result = json.dumps(infos[i], indent=4)
    
    # Μετατρέπω το dictionary --> json για καλύτερη ανάγνωση + εξορύξη δεδομένων
    # Εισάγω σε λίστες τα αποτελέσματα ώστε να φτιάξω τα data
    with open(f"./results/results_{press[i]}.json", 'w') as f:
        f.write(result)
        avg_load.append(infos[i]["Number of molecules"]["methane"]["Average loading absolute [cm^3 (STP)/cm^3 framework]"][0])
        avg_energy.append(infos[i]["Total energy"]["[K]"][0])
        enthalpy.append(infos[i]["Enthalpy of adsorption"]["[K]"][0])


# εδω χρειάζεται κάθε key να έχει ίδιο πλήθος values
#data = {
#        'mof':mofs,
#        'press':press, 
#        'avg_load':avg_load, 
#        'unit_load':unit_load,
#        'enthalpy': enthalpy, 
#        'unit_enth':unit_enth, 
#        'avg_energy':avg_energy, 
#        'unit_ener':unit_ener
#        }
data =[]
for i in range(0, len(filename)):
    for j in range(0, len(mofs)):
        data.append({
            'mof':mofs[j],
            'press':press[i], 
            'avg_load':avg_load[i], 
            'unit_load':unit_load,
            'enthalpy': enthalpy[i], 
            'unit_enth':unit_enth, 
            'avg_energy':avg_energy[i], 
            'unit_ener':unit_ener
        }
        )


df = pd.DataFrame(data)
print(df)
df.to_csv('data_absorption_flex.csv', index=False)






