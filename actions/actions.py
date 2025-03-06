from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,EventType
from news import NewsFromBBC
from stock_news import stocknews
from stocks import get_data,clean,stock_analysis
from yahoo_fin import stock_info
from vslots import dose_avai_pincode,main_task
import requests

class ActionNewsTracker(Action):
    def name(self) -> Text:
        return "action_news_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            message = NewsFromBBC()
            #print(message)
            dispatcher.utter_message(text=message)

        except:
            m = "Sorry your request could not be processed."
            dispatcher.utter_message(text=m)

        return []


class ActionStocksTracker(Action):

    def name(self) -> Text:
        return "action_stocks_tracker"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            ticker = tracker.get_slot('stock')
            message = stock_analysis(ticker)
            dispatcher.utter_message(text=message)

        except:
            m = "Sorry your request could not be completed"
            dispatcher.utter_message(text=m)

        return [SlotSet('stock',ticker)]


class ActionStockNewsTracker(Action):
    def name(self) -> Text:
        return "action_stock_news_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            message = stocknews()
            #print(message)
            dispatcher.utter_message(text=message)

        except:
            m = "Sorry your request could not be processed."
            dispatcher.utter_message(text=m)

        return []

class ActionCurrentPrice(Action):
    def name(self) -> Text:
        return "action_current_price"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            tckr = tracker.get_slot('ticker')
            price = stock_info.get_live_price(tckr)
            if(tckr[-2:]=='NS' or tckr[-2]=='BO'):
                message = "Current price of " + tckr + " is " + str(price) + " INR."
                dispatcher.utter_message(text=message)
            else:
                message = "Current price of " + tckr+ " is " + str(price) + " USD."
                dispatcher.utter_message(text=message)

        except:
            m = "Sorry data could not be fetched. Please ensure that you have typed the ticker correctly."
            dispatcher.utter_message(text=m)

        return []

