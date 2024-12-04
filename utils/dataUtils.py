import pickle

class DataUtils:
    @staticmethod
    def saveData(data, filename):
        with open(filename, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def loadData(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
