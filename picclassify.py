import pickle
import codecs
import os

class DataManagement:
    elements = []
    def __init__(self, filename):
        self.filename  = filename

    def load_data(self):
        if not(os.path.exists(self.filename) and os.path.isfile(self.filename)):
            with codecs.open(self.filename, "wb") as f:
                pickle.dump(self.elements, f)

        with codecs.open(self.filename, "rb") as f:
            elems = pickle.load(f)
        return elems

    def save_data(self):
        with codecs.open(self.filename, "wb") as f:
            pickle.dump(self.elements, f)

    def insert_save(self, new_element):
        self.elements = self.load_data()
        for elem in self.elements:
            if elem["url"] == new_element["url"]:
                return False
            else:
                self.elements.append(new_element)
                with codecs.open(self.filename, "wb") as f:
                    pickle.dump(self.elems, f)
                return True

    def query_db(self, url = None, name = None):
        self.elements = self.load_data()
        if url:
            for i, elem in enumerate(self.elements):
                if elem["url"] == url:
                    return i
                else:
                    return -1
        elif name:
            for i, elem in enumerate(self.elements):
                if elem["name"] == name:
                    return i
                else:
                    return -1
        else:
            return -1

def writeData():
    with open("fenlei.txt", encoding="utf-8") as f:
        lines = [i.strip() for i in f.readlines()][85:]
        dm = DataManagement("class02.dat")
        for i in lines:
            a = i.split("#")[1:]
            dm.elements.append(a)
        dm.save_data()


if __name__ == '__main__':
    print("pocclassify called!!")
    """
    writeData()
    dm = DataManagement("class02.dat")
    data = dm.load_data()
    for index, i in enumerate(data):
        if len(i) !=3:
            print(index,i)"""


    