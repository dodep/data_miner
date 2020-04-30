from billboard_app import Billboard
from genius_app import Genius
import datetime

class Data_miner:
    
    current_year = datetime.datetime.now().year

    def find_all(self):
        pass
    
    def find_by_date(self):
        input_date = {
            'year': self.get_year(),
            'mounth': self.get_mounth(),
            'day': self.get_day()
        }
        Billboard().req_to_billboard(input_date)
        
    def get_year(self):
        year = input(f'Enter year from 1958 to {self.current_year}: ')
        return self.check_year(year)
        
    def get_mounth(self):
        mounth = input('Enter mounth: from 01 to 12: ')
        return self.check_mounth(mounth)
        
    def get_day(self):
        day = input('Enter day: from 01 to 31: ')
        return self.check_day(day)
        
    def check_year(self,year):
        if year.isnumeric():
            
            if int(year) <= self.current_year and int(year) >= 1958:
                return year
            else:
                print(f'Year must be a number from 1958 to {self.current_year}')
                self.get_year()
        else:
            print('Year must be a number')
            self.get_year()
        
    def check_mounth(self,mounth):
        if mounth.isnumeric():
            
            if int(mounth) <= 12 and int(mounth) >= 1:
                if len(mounth) != 2:
                    mounth = '0' + mounth
                return mounth
            else:
                print(f'Mounth must be a number from 1 to 12')
                self.get_mounth()
        else:
            print('Mounth must be a number')
            self.get_mounth()
    
    def check_day(self,day):
        if day.isnumeric():
            
            if int(day) <= 31 and int(day) >= 1:
                
                if len(day) != 2:
                    day = '0' + day
                return day
            else:
                print(f'Day must be a number from 1 to 31')
                self.get_day()
        else:
            print('Day must be a number')
            self.get_day()
            
instance = Data_miner().find_by_date()