from aiogram.utils.helper import Helper, HelperMode, ListItem, Item

class TestStates(Helper):
    mode = HelperMode.snake_case

    GET_REQUEST = Item()
    GET_SCREENSHOT = Item()