"""Unit test is expected to be here, while I use some usage cases instead."""

from name_analyzer.name_analysis import Name_analysis

if __name__ == '__main__':
    # query = 'Martin Reynolds British'
    # query = 'Martin Reynolds Maynard'
    # query = 'Darry Holliday University of Holy Cross'
    # query = 'Caron Anderson Emory University'
    # query = 'Darryl Holliday City Bureau'
    query = 'Yi Fang SCU'

    obj = Name_analysis(google_dir= 'Your directory for Google images', bing_dir= 'Your directory for Bing images')
    result = obj.analyze_name(query)
    print(result)
