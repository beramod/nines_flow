class ModuleUtil:
    @classmethod
    def moduleFieldInfo(cls, module):
        if module == 'inverter':
            return [
                ['inverters', 'invno']
            ]
        elif module == 'bms':
            return [
                ['bms', 'bmsno']
            ]
        elif module == 'pcs':
            return [
                ['pcs', 'pcsno']
            ]
        elif module == 'meter':
            return [
                ['meters', 'meterno']
            ]
        elif module == 'emsEnv':
            return [
                ['aircons', 'airconno'],
                ['tempHumiditySensors', 'sensorNo'],
                ['trSensors', 'trno'],
                ['doorSensors', 'doorno'],
                ['fireSensors', 'firno'],
                ['ups', 'upsno']
            ]
        elif module == 'combinerBox':
            return [
                ['combinerBoxes', 'combinerboxno']
            ]
        elif module == 'pms':
            return [
                ['pms', 'pmsno']
            ]
        elif module == 'weather':
            return [
                ['insolations', 'insolationno'],
                ['winds', 'windno']
            ]
