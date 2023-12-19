# Controller Utils

class Utils:

    def sortStudent(Students):
        result_data = [(item[0], index + 1, *item[2:]) for index, item in enumerate(Students)]
        return result_data