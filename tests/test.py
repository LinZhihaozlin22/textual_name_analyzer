"""Unit test is expected to be here, while I use some usage cases instead."""

from name_analyzer import name_analysis

if __name__ == '__main__':
    # query = 'Martin Reynolds British'
    # query = 'Martin Reynolds Maynard'
    # query = 'Darry Holliday University of Holy Cross'
    # query = 'Caron Anderson Emory University'
    # query = 'Darryl Holliday City Bureau'
    query = 'Yi Fang SCU'

    num, search_face = 2, False
    obj = name_analysis.Name_analysis(google_dir= '/Users/linzhihao/PycharmProjects/Gender_API/Photo/google/', bing_dir= '/Users/linzhihao/PycharmProjects/Gender_API/Photo/bing/')
    result = obj.analyze_name(query, 2)
    print(result)