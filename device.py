class DeviceList :
    def read_List(self,file):
        try:
            with open(file+".txt", "r") as file_list:
                self._list=file_list.read().split("\n")
                ##print(list_ip)
        except Exception as error:
            return error
        return self._list
        