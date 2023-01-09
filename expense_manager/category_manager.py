from category import Category

class DuplicateCategoryError(Exception):
    pass

class CategoryManager:
    def __init__(self, categories=[]):
        self._categories = {}
        for category in categories:
            name = category.get_name().upper()
            self._categories[name] = category

    def add_category(self, category):
        if type(category) is str:
            name = category.strip()
            key = category.upper().strip()
            if key in self._categories:
                raise DuplicateCategoryError()
            
            self._categories[key] = Category(name)
 
        elif type(category) is Category:
            key = category.get_name().upper().strip()
            if key in self._categories:
                raise DuplicateCategoryError()

            self._categories[key] = category
        
        else:
            raise TypeError()
    
    def get_category(self, name):
        return self._categories[name.strip().upper()]

    def get_all(self):
        return [category for key, category in self._categories.items()]
