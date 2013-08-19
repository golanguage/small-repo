head93='aa 93'

did = {'speed' : '00', 'engineLoad':'02','engineRpm':'04','throttlePosition':'05', \
'brakePedalStatus':'0b','massAirFlow':'0d','calculatedFuelUsed':'0e','safetyStatus':'11', \
 'milStatus':'01','coolantTemperature':'03','PTOStatus':'06','odometer':'09', \
  'vehicleBattery':'08', 'fuelLevel':'07', 'totalfuel':'0a', 'engineHours':'0c','FLI1':'13', 'FLI2':'14','ACC1':'15'}
def int2little(value):
        bigend=format(value,'04x')
        return bigend[2:4]+' '+bigend[0:2]
        
        
j1708_speed = {'value': '50',  'uid': '04', }
j1939_speed = {'value': '00 00', 'uid': '05', }
obdii_speed = {'value': '00', 'uid': '06', }
def set_speed(value):
        j1708_speed['value']=format(value*8//5,"02x") 
        j1939_speed['value']=int2little(value*256)
        obdii_speed['value']=format(value,"02x")


j1708_engineLoad = {'value': '5e',  'uid': '0c', }
j1939_engineLoad = {'value': '20', 'uid': '09', }
obdii_engineLoad = {'value': '21', 'uid': '0a', }

def set_engineLoad(value):
        print('set_engineLoad')
        j1708_engineLoad['value']=format(value*2,"02x") 
        j1939_engineLoad['value']=format(value,"02x")
        obdii_engineLoad['value']=format(value*255//100,"02x")

j1708_engineRpm = {'value': '00 00',  'uid': '07', }
j1939_engineRpm = {'value': '11 11', 'uid': '08', }
obdii_engineRpm = {'value': 'a0 00', 'uid': '07', }

def set_rpm(value):
        print('set_rpm')
        j1708_engineRpm['value']=int2little(value*4)
        j1939_engineRpm['value']=int2little(value*8)
        obdii_engineRpm['value']=int2little(value*4)
        
j1708_throttlePosition = {'value': '50',  'uid': '0b', }
j1939_throttlePosition = {'value': '19', 'uid': '0b', }
obdii_throttlePosition = {'value': '60', 'uid': '0a', }
def set_throttlePosition(value):
        print('set_throttlePosition')
        j1708_throttlePosition['value']=format(value*5//2,"02x") 
        j1939_throttlePosition['value']=format(value*5//2,"02x") 
        obdii_throttlePosition['value']=format(value*255//100,"02x")

j1708_brakePedalStatus = {'value': '00',  'uid': '16', }
j1939_brakePedalStatus = {'value': '00', 'uid': '19', }
obdii_brakePedalStatus = {'value': '', 'uid': '00', }
def swtich(which,pressed):
        print('set ',which)
        if which == 'brake':
                if pressed:
                        j1708_brakePedalStatus['value']='50'
                        j1939_brakePedalStatus['value']='10'
                else:
                        j1708_brakePedalStatus['value']='00'
                        j1939_brakePedalStatus['value']='00'
        
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
def set_coolantTemperature(value):
        print('set_coolantTemperature')
        j1708_coolantTemperature['value']=format((value*9//5+32),"02x") 
        j1939_coolantTemperature['value']=format((value+40),"02x") 
        obdii_coolantTemperature['value']=format((value+40),"02x")
        

j1708_PTOStatus = {'value': '00',  'uid': '17', }
j1939_PTOStatus = {'value': '80 00 00 00 00 00 00 00', 'uid': '18', }
obdii_PTOStatus = {'value': '81', 'uid': '14', }

j1708_odometer = {'value': 'ce 22 08 00',  'uid': '01', }
j1939_odometer = {'value': 'a0 00 00 00', 'uid': '02', }
obdii_odometer = {'value': '', 'uid': '00', }

j1708_vehicleBattery = {'value': '0a 00',  'uid': '11', }
j1939_vehicleBattery = {'value': '00 ff 53 00 26 00 13 00', 'uid': '1a', }
obdii_vehicleBattery = {'value': '00 a0', 'uid': '12', }

j1708_fuelLevel = {'value': '14',  'uid': '0c', }
j1939_fuelLevel = {'value': '19', 'uid': '0b', }
obdii_fuelLevel = {'value': '21', 'uid': '0a', }

j1708_totalfuel = {'value': '64 00 00 00',  'uid': '0f', }
j1939_totalfuel = {'value': '64 00 00 00', 'uid': '10', }
obdii_totalfuel = {'value': '', 'uid': '00', }

j1708_engineHours = {'value': '10 00 00 00',  'uid': '1b', }
j1939_engineHours = {'value': '01 02 03 04 01 02 03 04', 'uid': '1f', }
obdii_engineHours = {'value': '', 'uid': '00', }

j1939_FLI1 = {'value': '00 00 00 00 00 00 00 00', 'uid': '29'}
j1939_FLI2 = {'value': 'f5 00 00 00 00 00 00 00', 'uid': '2a'}
j1939_ACC1 = {'value': 'ff ff 00 00 00 00 00 00', 'uid': '2b' }

fast_set = ['speed','engineLoad','engineRpm','throttlePosition','brakePedalStatus','massAirFlow','calculatedFuelUsed','safetyStatus']
slow_set = ['milStatus','coolantTemperature','PTOStatus','odometer','vehicleBattery','fuelLevel', 'totalfuel','engineHours']
molileye_set = ['FLI1','FLI2','ACC1']
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
                        #print(item)
                        key=protocol+"_"+item
                        if item == 'speed':
                                print('speed=',(eval(key))['value'])
                        #print(key)

                        if key in globals():
                                value_len=format((len((eval(key))['value'])+1)//3,"02x")
                                return_string=obdcat(return_string,did[item],(eval(key))['uid'],value_len,(eval(key))['value'],age)
                                element_number=element_number+1
                #print(return_string)
                print(len(return_string))
                byte_len=(len(return_string)+1)//3+2

                return_string=obdcat(head93, format(byte_len,"02x"), idset[setname], format(element_number,"02x"),return_string)
                return return_string

if __name__ == '__main__':
        print(int2little(255*256))
        print(dataset_age('obdii','slow'))
