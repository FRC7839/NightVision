
class Setting:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def return_list(self):
        return [self.name, self.value]

def main():
    settings = []
    settings = addSetting("robot_location", "middle", settings)
    settings = addSetting("camera_tolerance", "15", settings)
    settings = tuncode(settings)
    print(settings)
    settings = settings.split("#")
    print(settings)    

def tuncode(input_settings):
    final = ""
    i = 0
    while i < len(input_settings):
        try:
            final += input_settings[i] + "#"
        except TypeError:
            final += tuncode(input_settings[i])
        i-=-1
    return final
    
def addSetting(name, value, input_array):
    if input_array == []:
        input_array = ["tunapro"]
        
    input_array.append(Setting(str(name), str(value)).return_list())
    return input_array

if __name__ == "__main__":
    print("Started")
    main()