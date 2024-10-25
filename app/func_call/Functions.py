from langchain_community.chat_message_histories import (
    PostgresChatMessageHistory,
)
from app.settings import settings
from app.dependencies.Postgre import PostgreClient

class FunctionsTools:
    def __init__(self,):
        pass
    
    def greetings(self):
        '''This function is triggered from greetings'''
        greeting_message = "Hai! Apakah ada yang bisa saya bantu?"

        return greeting_message

    def closing(self):
        '''This function is triggered from closing'''
        closing_message = "Terimakasih! sampai berjumpa kembali."
        
        return closing_message

    def tourist_count(self, location, month, year):
        """Retrieves the visitor count for a specific location, month, and year."""
        result = PostgreClient().get_tourist_cont(location=location, month=month, year=year)
        return result

    def tourist_trend(self, location, year):
        """Retrieves the monthly visitor count trend for a specific location and year ."""
        result = PostgreClient().get_monthly_trend(location=location, year=year)
        return result
    
    def top_location(self, year, ascending="DESC"):
        """Retrieves the top locations with the highest visitor count for a specific year."""
        result = PostgreClient().get_top_locations(year=year, ascending=ascending)
        return result