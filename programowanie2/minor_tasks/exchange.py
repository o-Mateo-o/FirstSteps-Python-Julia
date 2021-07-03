#!/usr/bin/env python

# List 5, Prog.-L, PWr
# Mateusz Machaj, 03.05.2021

# All the three parts written in one file

### running cmd command:    python "c:\Users\cp\VS proj\exchange.py""


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os


if __name__ == "__main__":
    
    # constant values regarding the pc and nbp site
    DATA_DIR = r"c:\Users\cp\CurrencyExchangeRateProgram"
    TABLE_NAMES = ['A', 'B']
    FILE_BASENAME = "table"
    ICON_PATH = r"c:\Users\cp\VS proj\money.ico"

#
# BACKEND part
#

    def request_url():
        """
        Get data from NBP API
        :return: list of raw text xmls - exchange rates from NBP (list)
        Multiple errors handling
        """
        data = []
        for url in [f"http://api.nbp.pl/api/exchangerates/tables/{table}/?format=xml" for table in TABLE_NAMES]:
            try:
                response = requests.get(url)
                response.raise_for_status()
            except (requests.ConnectionError, requests.Timeout):
                raise Exception("Connection Error")
            except requests.exceptions.HTTPError:
                raise Exception("HTTP Error")
            except Exception:
                raise Exception("Unknown Error")
            else:
                data.append(response.text)
        return data


    def provide_directory():
        """
        Make a storage directory and document it - unless it exists
        """
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
            print(f"New directory for data storage added at {DATA_DIR}.")
        with open(DATA_DIR+r"\README.md", 'w') as readmefile:
            readmefile.write(f"Don't modify '{FILE_BASENAME}{TABLE_NAMES[0]}.xml' \
            and '{FILE_BASENAME}{TABLE_NAMES[1]}.xml' files, otherwise you can loose your data.")


    def open_archive_files():
        """
        Open files saved previously in storage
        :return: archival text data -list of raw text xmls from NBP (list)
        """
        arch_data = []
        for table in TABLE_NAMES:
            with open(f"{DATA_DIR}\\{FILE_BASENAME}{table}.xml", 'r') as filename:
                arch_data.append(filename.read())
        return arch_data


    def old_data_presence():
        """
        Check if storage contains archival data.
        :return: True if it contains (bool)
        """
        for table in TABLE_NAMES:
            if not os.path.isfile(DATA_DIR+f"\\{FILE_BASENAME}{table}.xml"):
                return False
        return True


    def get_data(request_funct, storage_getter):
        """
        Get the data for processing, searching in both sources
        :param request_funct: function that gets data from api(function)
        :param storage_getter: function that gets data from storage (function)
        :return: tuple of raw data and information about validity (tuple)
        Exceptions from url getter and storage getter
        """
        uptodate = True
        try:
            data = request_funct()
        except Exception as err:
            uptodate = False
            if old_data_presence():
                data = storage_getter()
            else:
                raise Exception(
                    f"{err} and no saved data in the storage directory.")
        return (data, uptodate)


    def conv_data_xml(data):
        """
        Convert raw xml text data to xml tree
        :param data: raw xml text list (list)
        :return: converted xml trees (list)
        """
        converted = []
        for table in data:
            converted.append(ET.XML(table))
        return converted


    def save_files(data_tb):
        """
        Save files in storage
        :param data_tb: raw xml data (list)
        """
        for idx, table in enumerate(TABLE_NAMES):
            with open(f"{DATA_DIR}\\{FILE_BASENAME}{table}.xml", 'w') as filename:
                filename.write(data_tb[idx])


    def parse_data(xml_data):
        """
        Create pandas dataframes representing the downloaded data
        :param xml_data: xml trees (list)
        :return: pandas dataframes (list)
        """
        final_dfs = []
        for table in [0, 1]:
            rows = []
            for child in xml_data[table][0][3]:
                rows.append([subchild.text for subchild in child])

            cols = ([elem.tag for elem in xml_data[table][0][3][0]])

            df = pd.DataFrame(rows)
            df.columns = cols
            final_dfs.append(df)
        return final_dfs


    def get_xml_date(xml_data):
        """
        Get the date from currently used data
        :param xml_data: xml trees (list)
        :return: date of the rates in the files (str)
        """
        return xml_data[0][0][2].text


    def complete_table(ab_dataframes):
        """
        Concatenate pandas tables and add 'złoty' to them
        :param ab_dataframes: dataframes of NBP data (list)
        :return: table of all the downloaded data (pd.DataFrame) 
        """
        pln_row = pd.DataFrame(
            {"Currency": ["złoty"], "Code": ["PLN"], "Mid": ["1"]})
        table_all = pd.concat([pln_row]+ab_dataframes, ignore_index=True)
        return table_all


    def calculate(init_curr_n, target_curr_n, amount, data_table):
        """
        Calculate the amount after exchange
        :param init_curr_n: initial currency index (str)
        :param target_curr_n: target currency index (str)
        :param amount: amount of money in initial currency (str)
        :param data_table: table of all the data (pd.DataFrame)
        :return: value after exchange (float)
        """
        init_curr_rate = float(data_table.iloc[init_curr_n]["Mid"])
        target_curr_rate = float(data_table.iloc[target_curr_n]["Mid"])
        amount = float(amount)
        return amount*init_curr_rate/target_curr_rate


    def prepare_data():
        """
        Prepare the collected data for processing.
        not marked usage of predefined functions
        :return: complete table of all the data(pd.DF), file dates (str), validity info(bool) (tuple)
        """
        # funcions not given as arguments are used
        provide_directory()
        try:
            datacoll = get_data(request_url, open_archive_files)
        except Exception as err:
            raise Exception(err)
        save_files(datacoll[0])
        try:
            data_xmltree = conv_data_xml(datacoll[0])
        except:
            raise Exception(
                "Problems occured when converting the data to processable type.")
        try:
            dataframes = parse_data(data_xmltree)
        except:
            raise Exception("Problems occured when parsing the data.")

        compl_table = complete_table(dataframes)
        str_date = get_xml_date(data_xmltree)

        return (compl_table, str_date, datacoll[1])


    def get_result(initial_currency_index, target_currency_index, money_amount, prepare_data_function):
        """
        Calculate the amount after exchange
        :param initial_currency_index: initial currency index (str)
        :param target_currency_index: target currency index (str)
        :param money_amount: amount of money in initial currency (str)
        :param prepare_data_function: function preparing the data for procesing (function)
        :return: final value after exchange
        Handle possible exceptions
        """
        try:
            currency_rates_table = prepare_data_function()[0]
        except Exception as err:
            raise Exception(f"Unable to get the data for calculation: {err}")
        else:
            total_length = len(currency_rates_table)
            curr_list = [initial_currency_index, target_currency_index]

            if any([idx >= total_length for idx in curr_list]) or any([idx < 0 for idx in curr_list]):
                raise IndexError("Currency index out of range")
            elif curr_list[0] == curr_list[1]:
                raise Exception(
                    "Can't convert the amount to the same currency!")
            elif money_amount <= 0:
                raise Exception("Amount can't be negative!")
            else:
                result = calculate(
                    initial_currency_index, target_currency_index, money_amount, currency_rates_table)
                result = round(result, 2)
            return result


#
# FRONTEND part
#

    def head_text(data_prepare_funct):
        """
        Prepare a message for the top of the frame - containing data vaidity info
        :param prepare_data_function: function preparing the data for procesing (function)
        :return: header text (str)
        """
        base = "Currency Exchange Calculator. "
        try:
            getf = data_prepare_funct()
        except:
            return base
        if getf[2]:
            return base+"Rates up-to-date."
        else:
            return base+"Can't get current rates. Data from: "+getf[1]


    def choice_list(prepare_data_function):
        """
        Prepare choice list for Comboboxes
        :param prepare_data_function: function preparing the data for procesing (function)
        :return: tags for the Combobox (tuple)
        """
        try:
            database = prepare_data_function()[0]
        except Exception as err:
            raise Exception(err)

        temp_list = []
        curr_name_list = list(database["Currency"])
        symbol_list = list(database["Code"])
        for idx in range(0, len(curr_name_list)):
            temp_list.append(f"{symbol_list[idx]} -- {curr_name_list[idx]}")

        return tuple(temp_list)


    def show_result(main_label_name, lst1, lst2, entry, data_prepare_funct):
        """
        Show the calculation result in label
        :param main_label_name: result label name
        :param lst1: initial currency box
        :param lst2: target currency box
        :param entry: entry box to write text in
        :param prepare_data_function: function preparing the data for procesing (function)
        In case of errors show them in message windows
        """
        idx1, idx2 = lst1.current(), lst2.current()
        valid = True
        # Initial amount check
        try:
            enter_val = float(entry.get())
        except:
            valid = False
            msg.showerror("Error", "Amount field expects a number.")

        # Currency choice check
        if idx1 in [-1, None] or idx2 in [-1, None]:
            main_label_name["text"] = "Choose the currencies."
        elif valid:
            try:
                main_label_name.config(font=(20))
                table = data_prepare_funct()[0]
                main_label_name["text"] = str(get_result(
                    idx1, idx2, enter_val, data_prepare_funct))+" "+table.iloc[idx2]["Code"]
            except Exception as err:
                msg.showerror("Error", err)

    
    def reverse(lst1, lst2):
        """
        Reverse the currencies selected in boxes (if defined)
        :param lst1: initial currency box
        :param lst2: target currency box
        """
        tmp1 = lst1.current()
        tmp2 = lst2.current()
        if tmp1 > -1 and tmp2 > -1:
            lst1.current(tmp2)
            lst2.current(tmp1)


    class CurrencyList(ttk.Combobox):
        """
        Choice box class for currencies
        names on the list already set
        possible index getting
        """
        def __init__(self, master_r, currency_names):
            self.index = tk.StringVar(master_r)
            self.index.set("Select From List")
            ttk.Combobox.__init__(self, master=master_r, width=35,
                                  state="readonly", textvariable=self.index)
            self.current(None)
            self["values"] = currency_names


    class Widgets(tk.Frame):
        """
        Class containing all the aplication widgets
        """
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            # Create all the widgets along with the features
            self.heading = tk.Label(self, text=head_text(prepare_data))
            self.curr_combox1 = CurrencyList(self, combox_choices)
            self.curr_combox2 = CurrencyList(self, combox_choices)

            self.amount_field = tk.Entry(self)
            self.rever = tk.Button(self, text="  "+'\u21C4'+"  ", bg='#c5dde6', command=lambda: reverse(
                self.curr_combox1, self.curr_combox2))
            self.rever.config(font=(15))
            self.execute_b = tk.Button(self, text="Compute", bg='#c5dde6', command=lambda: show_result(
                self.result_lab, self.curr_combox1, self.curr_combox2, self.amount_field, prepare_data))
            self.result_lab = tk.Label(self, relief=tk.RAISED)
            self.label_result_lab = tk.Label(
                self, text="Amount after exchange:")
            self.quiter = tk.Button(
                self, text="Quit", command=quit, bg='#c5dde6')
            self.label_curr1 = tk.Label(self, text="Initial currency:")
            self.label_curr2 = tk.Label(self, text="Target currency:")
            self.label_amount = tk.Label(
                self, text="Amount of money in given currency:")

            # Place the widgets on the grid
            self.heading.grid(row=0, columnspan=2, pady=10)
            self.quiter.grid(row=0, column=3, columnspan=2)
            self.label_curr1.grid(row=1, column=0)
            self.label_curr2.grid(row=2, column=0, padx=30)
            self.curr_combox1.grid(row=1, column=1, pady=20)
            self.curr_combox2.grid(row=2, column=1, pady=20)
            self.rever.grid(row=2, column=3, columnspan=2)
            self.label_amount.grid(row=1, column=3, rowspan=1, padx=30)
            self.amount_field.grid(row=1, column=4, rowspan=1, padx=20)
            self.execute_b.grid(row=4, column=1, columnspan=3,
                                pady=20, sticky="we")
            self.label_result_lab.grid(
                row=5, column=1, pady=40, columnspan=2, sticky="we", rowspan=2)
            self.result_lab.grid(row=5, column=3, pady=40,
                                 columnspan=1, sticky="we", rowspan=2)

#
# Execution
#
    root = tk.Tk()
    root.title(" Currency Exchange Calculator")
    root.iconbitmap(ICON_PATH)
    root.resizable(width=False, height=False)
    root.geometry('+300+100')

    # loading attempt
    try:
        combox_choices = choice_list(prepare_data)
    except Exception as err:
        msg.showerror("Loading error", str(
            err)+"\nTry to restart the program, check your internet connection or search for problems in storage folder.")
        combox_choices = ("NO DATA",)

    Widgets(root).grid(sticky="nsew")
    root.mainloop()
