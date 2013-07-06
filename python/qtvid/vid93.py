head93='aa 93'

did = {'speed' : '00', 'engineLoad':'02','engineRpm':'04','throttlePosition':'05', \
'brakePedalStatus':'0b','massAirFlow':'0d','calculatedFuelUsed':'0e','safetyStatus':'11', \
 'milStatus':'01','coolantTemperature':'03','PTOStatus':'06'}

j1708_speed = {'value': '00',  'uid': '04', }
j1939_speed = {'value': '00 00', 'uid': '05', }
obdii_speed = {'value': '00', 'uid': '06', }
def set_speed(value):
        j1708_speed['value']=format((value+1)//10,"02x")
        j1939_speed['value']='00 '+format((value+1),"02x")
        obdii_speed['value']=format((value+1)//3,"02x")
        print(j1708_speed)
        
j1708_engineLoad = {'value': '5e',  'uid': '0c', }
j1939_engineLoad = {'value': '20', 'uid': '09', }
obdii_engineLoad = {'value': '21', 'uid': '0a', }

j1708_engineRpm = {'value': '00 20',  'uid': '07', }
j1939_engineRpm = {'value': '11 11', 'uid': '08', }
obdii_engineRpm = {'value': 'a0 00', 'uid': '07', }

def set_rpm(rpm):
        j1708_engineRpm['value']='00 '+format((value+1),"02x")
        j1939_engineRpm['value']='00 '+format((value+1),"02x")
        obdii_engineRpm['value']=format((value+1),"02x")+' 00'
        
j1708_throttlePosition = {'value': '50',  'uid': '0b', }
j1939_throttlePosition = {'value': '19', 'uid': '0b', }
obdii_throttlePosition = {'value': '60', 'uid': '0s', }

j1708_brakePedalStatus = {'value': '00',  'uid': '16', }
j1939_brakePedalStatus = {'value': '00', 'uid': '19', }
obdii_brakePedalStatus = {'value': '', 'uid': '00', }

j1708_massAirFlow = {'value': '10 00',  'uid': '1d', }
j1939_massAirFlow = {'value': '28 00', 'uid': '1e', }
obdii_massAirFlow = {'value': '64 00', 'uid': '1c', }

j1708_calculatedFuelUsed = {'value': '10 00',  'uid': '20', }

j1708_safetyStatus = {'value': '00',  'uid': '24', }
j1939_safetyStatus = {'value': '00', 'uid': '24', }

j1708_milStatus = {'value': '00',  'uid': '15', }
j1939_milStatus = {'value': '', 'uid': '00', }
obdii_milStatus = {'value': '80 00 00 80', 'uid': '13', }

j1708_coolantTemperature = {'value': '40',  'uid': '0e', }
j1939_coolantTemperature = {'value': '64', 'uid': '0d', }
obdii_coolantTemperature = {'value': '64', 'uid': '0d', }

j1708_PTOStatus = {'value': '00',  'uid': '17', }
j1939_PTOStatus = {'value': '80 00 00 00 00 00 00 00', 'uid': '18', }
obdii_PTOStatus = {'value': '81', 'uid': '14', }

j1708_ = {'value': '',  'uid': '', }
j1939_ = {'value': '', 'uid': '', }
obdii_ = {'value': '', 'uid': '', }

j1708_ = {'value': '',  'uid': '', }
j1939_ = {'value': '', 'uid': '', }
obdii_ = {'value': '', 'uid': '', }

fast_set = ['speed','engineLoad','engineRpm','throttlePosition','brakePedalStatus','massAirFlow','calculatedFuelUsed','safetyStatus']
fast_set = ['speed','engineRpm']
slow_set = ['milStatus','coolantTemperature','PTOStatus']
molileye_set = []
allset={'fast':fast_set, 'slow':slow_set,'molileye': molileye_set}
idset={'fast':'03', 'slow':'02','molileye': '04'}


def obdcat(*strlist):
                local_str=''
                for onebyte in strlist:
                        if  (onebyte != ''):
                                onebyte=str.strip(onebyte)
                                if (local_str== ''):
                                        local_str=onebyte
                                else:
                                        local_str=local_str+' '+onebyte
                return local_str

def dataset_age(protocol,setname,age='10 00'):

                return_string=''
                element_number=0
                set=allset[setname]
                for item in set:
                        print(item)
                        key=protocol+"_"+item
                        print(key)

                        if key in globals():
                                value_len=format((len((eval(key))['value'])+1)//3,"02x")
                                return_string=obdcat(return_string,did[item],(eval(key))['uid'],value_len,(eval(key))['value'],age)
                                element_number=element_number+1
                print(return_string)
                print(len(return_string))
                byte_len=len(return_string)//3+2

                return_string=obdcat(head93, format(byte_len,"02x"), format(element_number,"02x"),return_string)
                return return_string
if __name__ == '__main__':
        print ("start:")
        print(dataset_age('obdii','fast'))
