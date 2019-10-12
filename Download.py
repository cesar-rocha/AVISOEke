import os
import calendar
import datetime

def date_range(year,month):
    """
        Get date range for a particular month and year.

        ---
        Returns
            - dateini: initial date [string, %Y-%m-%d]
            - dateend final date    [string, %Y-%m-%d]
    """
    _, numdays = calendar.monthrange(year, month)
    dateini = (datetime.date(year,month,1)).strftime("%Y-%m-%d")
    dateend = (datetime.date(year,month,numdays)).strftime("%Y-%m-%d")

    return dateini,dateend

def build_command(datemin,datemax,path,filename):
    """
        Build python motuclient command to download data from 
        http://marine.copernicus.eu/services-portfolio/access-to-products

        Adapted from Dante Napolitano's download_aviso.py script.
    
        ---
        Return
        A string with the command

    """

    string ='python -m motuclient --motu http://my.cmems-du.eu/motu-web/Motu --service-id SEALEVEL_GLO_PHY_L4_REP_OBSERVATIONS_008_047-DGF --product-id dataset-duacs-rep-global-merged-allsat-phy-l4 --date-min ' + datemin + ' --date-max ' + datemax + ' --out-dir ' + path + ' --out-name ' + filename + ' --user cbarbedorocha --pwd rimhy5-zafcAn-pohxim'

    return string

def download_data(download_command, datamin):
    """ 
        Execute the python command in encoded in the string download_command
        and logs whether the download was successful/unsuccessful.

        Adapted from Dante Napolitano's download_aviso.py script.

    """
    
    print(' ')
    print('Downloading ' + datamin[:7] + ' data...')
    print(' ')

    out = os.system(download_command)

    if out == 0:
        print(' ')
        print('Succesfully downloaded ' + datamin[:7] + ' data.')
        print(' ')
    else:
        print(' ')
        print('Failed to download ' + datamin[:7] + ' data.')
        print(' ')

def create_directory(directory):
    
    try:
        os.stat(directory)
    except:
        os.mkdir(directory) 


if __name__=="__main__":

    create_directory('Data')

    for year in range(1995,2019):

        create_directory('./data/' + str(year))

        for month in range(1,13):

            if month < 10:
                path = './Data/' + str(year) + '/0' + str(month)
            else:
                path = './Data/' + str(year) + '/' + str(month)

            create_directory(path)

            datemin, datemax = date_range(year,month)

            filename = str(month) + '.zip'

            download_command = build_command(datemin,datemax,path,filename)
            download_data(download_command,datemin)

