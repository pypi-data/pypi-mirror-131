"""This script fetches  information from API and generates html,excel, pdf, xml,
   csv files of the response received from API    Author - Mohammad Toseef """
import json
import sys
import requests
import pandas as pd
import pdfkit
import numpy as np
import logging
import os

# noinspection SpellCheckingInspection
from save_file import save

logging.basicConfig(filename='GenerateFiles.log', level=logging.DEBUG,
                    format='%(asctime)s // %(levelname)s : %(message)s // line no. %(lineno)d',
                    filemode='w')


class GenerateFiles:
    """ Takes API URL and file name without extension and generates CSV ,
    HTML , EXCEL , XML , PDF files as per the function call
    Methods
    -------
    load_dataframe():
            Initialize dataframe either by reading csv or making API call
    api_call():
            request the server and fetch the data
    to_excel(file_name=None):
            save the dataframe as Excel file
    normalize(dataframe=None):
        normalize json data and return dataframe
    to_csv(file_name=None):
        saves dataframe  as csv file
    to_xml(file_name=None):
        saves dataframe as xml file
    html_to_pdf(html_filename=None, pdf_filename=None):
        convert html file to pdf file
    """

    def __init__(self, api_url, file_name=None):
        self.api_url = api_url
        if file_name is None:
            file_name = 'default'
        self.csv_filename = file_name + '.csv'
        self.html_filename = file_name + '.html'
        self.pdf_filename = file_name + '.pdf'
        self.excel_filename = file_name + '.xlsx'
        self.xml_filename = file_name + '.xml'
        self.dataframe = pd.DataFrame()

    def load_dataframe(self):
        """  Initialize dataframe with json normalized data   """
        try:
            # checking if CSV File is present in current working directory
            if os.path.isfile(os.path.dirname(os.path.realpath(__file__))
                              + '\\' + self.csv_filename):
                self.dataframe = pd.read_csv(self.csv_filename)
                logging.info("Reading data from " + self.csv_filename)
            else:
                # Fetching data from API in case of CSV file not present
                response = self.api_call()
                self.dataframe = self.normalize(response.json())

                # Replacing NaN values with whitespace
                self.dataframe = self.dataframe.replace(np.nan, '', regex=True)
                logging.info('Status Code : ' + str(response.status_code))
        except json.JSONDecodeError as e:
            logging.error('json_data data in response is not correct ')
            logging.exception(e)
            sys.exit(1)

    def api_call(self):
        """
        :return: response of the request from API
        """
        try:
            response = requests.get(self.api_url)
            if response.status_code >= 400:
                raise ConnectionError
            return response
        except requests.exceptions.RequestException as e:
            logging.error('Error in establishing connection with API ')
            logging.exception(e)
            sys.exit(1)
        except ConnectionError as ce:
            logging.error('A Connection error occurred ')
            logging.exception(ce)
            sys.exit(1)

    def to_excel(self, file_name=None):
        """
        Saves dataframe as Excel
        :param file_name: (optional) takes Excel file name as input else uses self.excel_filename
        :return: None
        """
        if file_name is None:
            file_name = self.excel_filename
        try:
            if not isinstance(self.dataframe, pd.DataFrame):
                raise AttributeError('self.dataframe arg in to_excel() is not a dataframe')
            if not isinstance(file_name, str) and not file_name.endswith('.xlsx'):
                raise NameError('Please Provide Valid Excel File Name')
            excel_writer = pd.ExcelWriter(file_name)
            self.dataframe.to_excel(excel_writer, index=False)
            excel_writer.save()
            logging.info('Excel file has been generated : Filename - {}'.format(file_name))
        except NameError as ne:
            logging.error(ne)
        except AttributeError as ae:
            logging.error(ae)
        except PermissionError:
            logging.error('Got Permission Error while trying to write Excel File')

    @staticmethod
    def normalize(data):
        """
        :param data: contains json data to be normalized
        :return: dataframe having normalized data
        """
        all_column = []
        selected_column = []

        for item in data:
            if isinstance(item, dict):
                for key in item.keys():
                    if isinstance(item[key], list):
                        if key not in selected_column and item[key]:
                            selected_column.append(key)
                    elif key not in selected_column:
                        if key not in all_column:
                            all_column.append(key)
                if len(selected_column) + len(all_column) == len(item.keys()):
                    break
            elif isinstance(item, str):
                if isinstance(data[item], list) or isinstance(data[item], dict):
                    if item not in selected_column:
                        selected_column.append(item)
                elif item not in all_column:
                    all_column.append(item)
        print("len of all column is {} and selected column is {}".format(len(all_column), len(selected_column)))
        if selected_column:
            pf = pd.json_normalize(data, record_path=selected_column[0], meta=all_column,
                                   errors='ignore', record_prefix=str(selected_column[0] + '-'))
            if all_column:
                for i in range(1, len(selected_column)):
                    pf1 = pd.json_normalize(data, record_path=selected_column[i], meta=all_column[0],
                                            errors='ignore', record_prefix=str(selected_column[i] + '-'))
                    pf = pf.merge(pf1, on=all_column[0])
        else:
            pf = pd.json_normalize(data)
        return pf

    def to_csv(self, file_name=None):
        """ Save Dataframe  as CSV file
        :param file_name : (optional) takes Excel file name as input else uses the self.csv_filename
        """
        if file_name is None:
            file_name = self.csv_filename
        try:
            self.dataframe.to_csv(file_name, index=False)
        except PermissionError as e:
            logging.error('Got Permission Error inside to_csv()' + str(e))
        logging.info('CSV File has been Generated : Filename - {}'.format(file_name))

    def to_html(self, file_name=None):
        """
        Saves dataframe as HTML File
        :param file_name: (optional) takes HTML file name as input else uses the self.html_filename
        :return: str
        """
        if file_name is None:
            file_name = self.html_filename
        try:
            if not isinstance(self.dataframe, pd.DataFrame):
                raise AttributeError('self.dataframe arg in to_html() is not a dataframe')
            if not isinstance(file_name, str) or not file_name.endswith('.html'):
                raise NameError('Please Provide Valid HTML File Name')
            index = 0
            # converting urls in image column to its corresponding html_data <img> tag
            if self.dataframe.get('image'):
                for item in self.dataframe['image']:
                    # url = item.split('.png')[0] + '.png'
                    self.dataframe["image"].at[index] = '<img src="' + str(item) + '" width = 50>'
                    index += 1
            html_data = self.dataframe.to_html(escape=False)
            logging.debug('inside to_html()')
            save(filename=file_name, content=html_data)
            logging.debug('after save()')
            logging.info('HTML is generated from CSV : Filename - {}'.format(file_name))
        except AttributeError as e:
            logging.error(e)
        except NameError as ne:
            logging.error(ne)
        except PermissionError:
            logging.error('Got Permission Error while trying to write HTML File')

    def to_xml(self, file_name=None):
        """
        Saves dataframe as XML File
        :param file_name: (optional) takes XML file name as input else uses self.xml_filename
        :return: None
        """
        if file_name is None:
            file_name = self.xml_filename
        try:
            if not isinstance(self.dataframe, pd.DataFrame):
                raise AttributeError('self.dataframe arg in to_xml() is not a dataframe')
            if not isinstance(file_name, str) and not file_name.endswith('.xml'):
                raise NameError('Please Provide Valid XML File Name')
            self.dataframe.to_xml(file_name)
            logging.info('XML file has been generated : Filename - {}'.format(file_name))
        except AttributeError as e:
            logging.error(e)
        except NameError as ne:
            logging.error(ne)
        except PermissionError as e:
            logging.error('Got Permission Error while trying to write HTML File')
            logging.exception(e)

    def html_to_pdf(self, html_filename=None, pdf_filename=None):
        """
        Converts HTML file to PDF
        :param html_filename:  takes HTML file name as input
        :param pdf_filename: takes PDF file name as input
        :return: None
        """
        if html_filename is None:
            html_filename = self.html_filename
        if pdf_filename is None:
            pdf_filename = self.pdf_filename
        try:
            if not isinstance(html_filename, str) or not html_filename.endswith('.html'):
                raise NameError('Please Provide Valid HTML file name')
            if not isinstance(pdf_filename, str) or not pdf_filename.endswith('.pdf'):
                raise NameError('Please provide valid pdf file name')
            options = {
                'page-size': 'B0',
                'dpi': 400
            }
            if not os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '\\' + html_filename):
                logging.error(html_filename + ' not present : Error in generating pdf in html_to_pdf()')
                return
            pdfkit.from_file(html_filename, pdf_filename, options=options)
            logging.info('PDF File has been Generated : Filename {}'.format(pdf_filename))
        except NameError as ne:
            logging.error(ne)
        except FileNotFoundError as e:
            logging.error('file is not present')
            logging.exception(e)
        except OSError as ose:
            logging.error(ose)


if __name__ == '__main__':
    crypto_api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=' \
                     + 'market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage' \
                     + '=1h%2C24h'
    carbon_api_url = 'https://api.carbonintensity.org.uk/intensity'
    ghibli_api_url = 'https://ghibliapi.herokuapp.com/films/58611129-2dbc-4a81-a72f-77ddfc1b1b49'
    police_api_url = 'https://data.police.uk/api/forces'
    basketball_api_url = 'https://www.balldontlie.io/api/v1/players'
    fakestore_api_url = 'https://fakestoreapi.com/products'
    aviation_api_url = 'https://api.aviationapi.com/v1/charts/changes'
    # filename without extension
    filename = 'aviation_API'

    obj = GenerateFiles(api_url=aviation_api_url, file_name=filename)

    # initialize Dataframe with normalized API response
    obj.load_dataframe()

    # saving files as CSV ,Excel ,  html , xml , PDF
    obj.to_csv()
