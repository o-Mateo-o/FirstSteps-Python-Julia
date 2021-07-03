#!/usr/bin/env python

# List 6, Prog.-L, PWr
# Mateusz Machaj, 15.05.2021

# All the parts written in one file
import os
import random
from kivy.uix.gridlayout import GridLayout
import numpy as np
from matplotlib import pyplot as plt
import re
import string
import sympy
from sympy.printing.latex import latex
from sympy.calculus.singularities import singularities
from sympy import Symbol, S

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty

if __name__ == "__main__":

    ##########################################################################################
    #############################        FORMULA PARSING       ###############################
    ##########################################################################################

    # dictionaries of available functions and operators
    symbols_oper = {',': '.', '·': '*', '÷': '/',
                    '+': '+', '^': '**', '*': '*', '/': '/'}
    symbols_spec_oper = {'-': '-'}
    symbols_fnct = {'abs': 'abs', 'sqrt': 'np.sqrt', 'tg': 'np.tan', 'sin': 'np.sin', 'cos': 'np.cos', 'exp': 'np.exp',
                    'arcsin': 'np.arcsin', 'arccos': 'np.arccos', 'arctg': 'np.arctan', 'ln': 'np.log',
                    'asin': 'np.arcsin', 'acos': 'np.arccos', 'atan': 'np.arctan'}
    symbols_brack = {'(': '(', ')': ')'}
    symbols = {**symbols_oper, **symbols_fnct,
               **symbols_brack, **symbols_spec_oper}

    def separate_formulas(written_formulas: str) -> set:
        '''
        Split input string into separate raw formulas.
        :param written_formulas: raw input text (str)
        :return: set of sepatated formulas (set of str)
        '''
        formulas_raw = set([elem.strip()
                           for elem in written_formulas.split(';')])
        if '' in formulas_raw:
            formulas_raw.remove('')
        return formulas_raw

    def examine_expression(written_formula: str) -> str:
        '''
        Find the variable used in formula. 
        Throw error in case of invalid format.
        :param written_formula: raw text - singe formula (str)
        :return: variable name (str)
        '''
        if written_formula.count('(') != written_formula.count(')'):
            raise Exception("Nawiasy nie są domknięte.")
        if re.search(r'\d\s+\d', written_formula):
            raise Exception("Nierozpoznana spacja pomiędzy liczbami.")
        if any([re.search(pattern, written_formula) for pattern in [r'\D,', r',\D']]):
            raise Exception("Przecinek w nieznanym kontekście.")
        if any([written_formula[idx] in list(symbols_oper.keys()) for idx in [0, -1]]):
            raise Exception("Operator nie może zaczynać ani kończyć wzoru.")
        for funct in symbols_fnct.keys():
            if re.search(r'({})(?!\()'.format(funct), ''.join(written_formula.split())) != None:
                raise Exception(
                    "Wyrażenie następujące po funkcji\npowinno znaleźć się w nawiasach.")
        if re.search(r'\(\)', written_formula) != None:
            raise Exception("Znaleziono puste nawiasy.")

        formula_analysed = written_formula[:]
        symbols_list_re = list(symbols.keys()) + \
            list(string.digits)+[' ', '\t', '\n', ';']

        for seq in sorted(symbols_list_re, key=len, reverse=True):
            formula_analysed = re.sub(r'({})'.format(
                re.escape(seq)), '', formula_analysed)

        remaining_chars = set(formula_analysed)

        remaining_chars_number = len(remaining_chars)
        if remaining_chars_number > 1:
            if 'x' in remaining_chars:
                remaining_chars.remove('x')
            else:
                remaining_chars.pop()
            raise Exception("Nieznane symbole: {}.".format(
                ', '.join(list(remaining_chars))))
        elif remaining_chars_number == 0:
            variable = 'x'
        else:
            variable = list(remaining_chars)[0]

        return variable

    def formula_conv_exec(written_formula: str, dict_of_sym: dict, variable_name: str) -> str:
        '''
        Prepare the formula for execution.
        :param written_formula: raw input text (str)
        :param dict_of_sym: dictionary of available operators and functions (dict)
        :param variable_name: variable name for particular formula (str)
        :return: formula ready for python execution (str)
        '''
        proc_formula = written_formula[:]
        substit_mask = written_formula[:]
        proc_formula = re.sub(r'\s', ' ', proc_formula)
        for key in sorted(dict_of_sym, key=len, reverse=True):
            loop_flag = True
            key_esc = re.escape(key)
            while loop_flag:
                occur = re.search(key_esc, substit_mask)
                if occur != None:
                    stt_i = occur.start()
                    end_i = occur.end()
                    proc_formula = proc_formula[:stt_i] + \
                        dict_of_sym[key]+proc_formula[end_i:]
                    substit_mask = substit_mask[:stt_i]+r'#' * \
                        len(dict_of_sym[key])+substit_mask[end_i:]
                else:
                    loop_flag = False

        loop_flag = True

        while loop_flag:
            occur = re.search(re.escape(variable_name), substit_mask)
            if occur != None:
                stt_i = occur.start()
                end_i = occur.end()
                proc_formula = proc_formula[:stt_i] + "x"+proc_formula[end_i:]
                substit_mask = substit_mask[:stt_i]+r'#'+substit_mask[end_i:]
            else:
                loop_flag = False
        proc_formula = re.sub(r'(\d)\s*([a-zA-Z])', r'\1*\2', proc_formula)
        proc_formula = re.sub(r'([a-zA-Z])\s*(\d)', r'\1*\2', proc_formula)
        proc_formula = re.sub(r'\)\s*([\w\(])', r')*\1', proc_formula)
        proc_formula = re.sub(r'(\[^a-zA-Z][\w\()])\(', r'\1*(', proc_formula)
        return proc_formula

    def formula_conv_latex(exec_formula: str, variable_name: str) -> str:
        '''
        Prepare a formula to be dispayed in latex.
        :param exec_formula: string of a formula ready to execution (str)
        :param variable_name: variable name for particular formula (str)
        :return: formula in latex format (str)
        '''
        converted_formula = re.sub(r'np\.', r'sympy.', exec_formula)
        x = Symbol(variable_name)
        converted_formula = re.sub(r'arc', 'a', converted_formula)
        try:
            converted_formula = latex(eval(converted_formula))
        except NameError:
            raise Exception(
                "Błąd w konwersji.\nZmienna może mieć tylko jeden znak.")
        converted_formula = re.sub('log', 'ln', converted_formula)

        return converted_formula

    def parse_formulas(input_string: str) -> tuple:
        '''
        Get data from raw input string. Parse all the formulas.
        :param input_string: raw text from input (str)
        :return: tuple of data (list of executable formulas, list of latex formulas,\
             list of variables), where each index stands for one formula (tuple of lists)
        '''
        try:
            formulas_list = separate_formulas(input_string)
            variables = [examine_expression(formula_raw)
                         for formula_raw in formulas_list]
        except Exception as err:
            raise Exception(err)
        formulas_exec = []
        formulas_latex = []
        for idx, formula_raw in enumerate(formulas_list):
            converted_formula = formula_conv_exec(
                formula_raw, symbols, variables[idx])
            formulas_exec.append(converted_formula)
            formulas_latex.append(formula_conv_latex(
                converted_formula, variables[idx]))

        return formulas_exec, formulas_latex, variables

    ##########################################################################################
    #############################           PLOTTING           ###############################
    ##########################################################################################

    def range_validity(xlim: tuple, ylim: tuple) -> bool:
        '''
        Check if given range is proper.
        :param xlim: min and max arguments (tuple of floats)
        :param ylim: min and max values (tuple of floats)
        :return: info about validity (bool)
        '''
        if (xlim[0] >= xlim[1]) or (ylim[0] >= ylim[1]):
            return False
        return True

    def plot_funct(functs_data: tuple, xlim: tuple, ylim: tuple, legend_flg: bool=True, 
        title: str="", xlabel: str="Arguments", ylabel: str="Values"):
        '''
        Do all the operations to create the plot from given data.
        :param functs_data: lists with parsed formulas (tuple)
        :param xlim: min and max arguments (tuple of floats)
        :param ylim: min and max values (tuple of floats)
        :param legend_flg: presence of legend (bool)
        :param title: title of a plot figure (str) 
        :param xlabel: arguments axis label (str)
        :param ylabel: values axis label (str)
        Void function updating the plt object.
        '''
        plt.clf()

        if not range_validity(xlim, ylim):
            raise Exception("Błąd zakresów.")

        funct_names = range(ord('f'), ord('z'))
        funct_limit = len(funct_names)

        for idx in range(0, len(functs_data[0])):
            x = Symbol(functs_data[2][idx])
            arguments = np.linspace(xlim[0], xlim[1], 1001)

            if 'x' in functs_data[0][idx]:
                prep_str = functs_data[0][idx]
                prep_str = re.sub(r'np\.', 'sympy.', prep_str)
                prep_str = re.sub(r'arc', 'a', prep_str)
                sing_points = list(singularities(
                    eval(prep_str), x, sympy.Interval(xlim[0], xlim[1])))
                sing_points_numb = len(sing_points)
            else:
                sing_points_numb = 0

            legend_label = '${f}\,({v}) = '.format(f=chr(
                funct_names[idx % funct_limit]), v=functs_data[2][idx])+functs_data[1][idx]+'$'
            plot_color = [random.random()/1.1, random.random() /
                          1.1, random.random()/1.1]

            values = [eval(functs_data[0][idx]) for x in arguments]
            if sing_points_numb > 0:
                slice_points = [xlim[0]]+sing_points+[xlim[1]]
                for point_idx in range(0, sing_points_numb+1):
                    slice_inter = np.where((float(slice_points[point_idx]) < arguments) & (
                        arguments < float(slice_points[point_idx+1])))

                    if len(slice_inter[0] > 0):
                        slice_range = slice(
                            slice_inter[0][0], slice_inter[0][-1])
                        plt.plot(arguments[slice_range], values[slice_range],
                                 label=legend_label, color=plot_color)
                    legend_label = None
            else:
                plt.plot(arguments, values,
                         label=legend_label, color=plot_color)
        if legend_flg:
            plt.legend(loc="upper right")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.ylim(ylim)
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.grid(linewidth=1)

    #========================================================================================#
    #========================================================================================#
    #========================================================================================#

    ##########################################################################################
    #############################           GUI STYLE          ###############################
    ##########################################################################################


    # Kivy lang layout and basic events
    kv = '''
GridLayout:
    cols: 1
    padding: [20, 20]
    GridLayout:
        cols: 2      
        GridLayout:
            cols: 1
            size_hint: 0.8, 1
            GridLayout:
                rows: 4
                spacing: [0, 30]
                GridLayout:
                    size_hint_y: 0.6
                    spacing: [5, 5]
                    padding: [5, 5]
                    rows: 2
                    GridLayout:
                        cols: 2
                        padding: [0, 15]
                        Button:
                            background_color: 0.5, 0.5, 0.5, 1
                            text: "Pomoc"
                            size_hint_x: 0.3
                            on_press: mf.helper()
                        Label:
                            text: "Wzory funkcji:"
                    AsciiInput:
                        id: formulas_input
                        text: ""
                        on_text: mf.formulas_input = args[1]
                GridLayout:
                    cols: 4
                    rows: 2
                    size_hint_y: 0.5
                    spacing: [5, 10]
                    padding: [5, 10]
                    Label:
                        text: "Zakres\\nargumentów: "
                        halign: "center"
                    CommaFloatInput:
                        id: xmin_input
                        halign: "center"
                        valign: "middle"
                        text: '-5'
                        on_text: mf.xmin_input = args[1]
                    Label: 
                        text: " - "
                        size_hint_x: 0.2
                    CommaFloatInput:
                        id: xmax_input
                        halign: "center"
                        valign: "middle"
                        text: '5'
                        on_text: mf.xmax_input = args[1]
                    Label:
                        text: "Zakres\\nwartości: "
                        halign: "center"
                    CommaFloatInput:
                        id: ymin_input
                        halign: "center"
                        valign: "middle"
                        text: '-5'
                        on_text: mf.ymin_input = args[1]
                    Label: 
                        text: " - "
                        size_hint_x: 0.2
                    CommaFloatInput:
                        id: ymax_input
                        halign: "center"
                        valign: "middle"
                        text: '5'
                        on_text: mf.ymax_input = args[1]
                GridLayout:
                    rows: 3
                    spacing: [5, 5]
                    padding: [5, 5]
                    GridLayout:
                        rows: 2
                        Label:
                            text: "Tytuł wykresu:"
                        TextInput:
                            id: title_input
                            text: 'Wykres'
                            on_text: mf.title_input = args[1]
                    GridLayout:
                        cols: 2
                        rows: 2
                        spacing: [5, 5]
                        padding: [5, 5]
                        Label:
                            text: "Etykieta argumentów:"
                        TextInput:
                            id: xlabel_input
                            text: 'Argumenty'
                            on_text: mf.xlabel_input = args[1]
                        Label:
                            text: "Etykieta wartości:"
                        TextInput:
                            id: ylabel_input
                            text: 'Wartości'
                            on_text: mf.ylabel_input = args[1]
                    GridLayout:
                        cols: 2
                        Label:
                            text: "Wyświetlanie legendy:"
                        CheckBox:
                            id: legend_input
                            active: True
                            on_active: mf.legend_input = not mf.legend_input
                GridLayout:
                    cols: 1
                    size_hint: [0, 0.25]
                    padding: [60, 10]
                    Button:
                        background_color: 0.8, 0.4, 0.4, 1
                        text: "ZAKOŃCZ"
                        on_press : app.stop()
                    
                        
        GridLayout:
            padding: [10, 0]
            spacing: [10, 10]
            rows: 2
            size_hint: 2, 1.5
            PlotFigure:
                id: mf
            GridLayout:
                cols: 2
                size_hint: 1, 0.4
                
                GridLayout:
                    spacing: [15, 0]
                    padding: [5, 5]
                    cols: 3

                    GridLayout:
                        cols: 4
                        rows: 3
                        spacing: [5, 5]
                        size_hint_x: 0.55
                        Button:
                            text: '1'
                            on_press: formulas_input.insert_text('1')
                        Button:
                            text: '2'
                            on_press: formulas_input.insert_text('2')
                        Button:
                            text: '3'
                            on_press: formulas_input.insert_text('3')
                        Button:
                            text: '4'
                            on_press: formulas_input.insert_text('4')
                        Button:
                            text: '5'
                            on_press: formulas_input.insert_text('5')
                        Button:
                            text: '6'
                            on_press: formulas_input.insert_text('6')
                        Button:
                            text: '7'
                            on_press: formulas_input.insert_text('7')
                        Button:
                            text: '8'
                            on_press: formulas_input.insert_text('8')
                        Button:
                            text: '9'
                            on_press: formulas_input.insert_text('9')
                        Button:
                            text: '0'
                            on_press: formulas_input.insert_text('0')
                        Button:
                            text: ','
                            on_press: formulas_input.insert_text(',')
                        Button:
                            text: 'x'
                            background_color: 0.7, 0.7, 0.9, 1
                            on_press: formulas_input.insert_text('x')


                    GridLayout:
                        spacing: [5, 5]
                        rows: 3
                        cols: 6
                        Button:
                            text: '+'
                            on_press: formulas_input.insert_text('+')
                        Button:
                            text: '-'
                            on_press: formulas_input.insert_text('-')
                        Button:
                            text: '×'
                            on_press: formulas_input.insert_text('*')
                        Button:
                            text: '÷'
                            on_press: formulas_input.insert_text('/(')
                        Button:
                            text: 'a^b'
                            on_press: formulas_input.insert_text('^(')
                        Button:
                            text: '√'
                            on_press: formulas_input.insert_text('sqrt(')
                        Button:
                            text: '('
                            on_press: formulas_input.insert_text('(')
                        Button:
                            text: ')'
                            on_press: formulas_input.insert_text(')')
                        Button:
                            text: '|...|'
                            on_press: formulas_input.insert_text('abs(')
                        Button:
                            text: 'ln'
                            on_press: formulas_input.insert_text('ln(')
                        Button:
                            text: 'sin'
                            on_press: formulas_input.insert_text('sin(')
                        Button:
                            text: 'cos'
                            on_press: formulas_input.insert_text('cos()')
                        Button:
                            text: 'tg'
                            on_press: formulas_input.insert_text('tg(')
                        Button:
                            text: 'arcsin'
                            on_press: formulas_input.insert_text('arcsin(')
                        Button:
                            text: 'arccos'
                            on_press: formulas_input.insert_text('arccos(')
                        Button:
                            text: 'arctg'
                            on_press: formulas_input.insert_text('arctg(')
                        Button:
                            text: 'e^a'
                            on_press: formulas_input.insert_text('exp(')

                    GridLayout:
                        spacing: [5, 5]
                        size_hint_x: 0.25
                        rows: 3
                        cols: 1
                        Button:
                            text: 'Cofnij'
                            background_color: 0.7, 0.7, 0.9, 1
                            on_press: formulas_input.do_undo()
                        Button:
                            text: 'Wyczyść'
                            background_color: 0.7, 0.7, 0.9, 1
                            on_press: formulas_input.text = ""
                        Button:
                            halign: "center"
                            background_color: 0.7, 0.7, 0.9, 1
                            text: 'Następny\\nwzór'
                            on_press: formulas_input.insert_text('; ')

                    
                GridLayout:
                    cols: 1
                    size_hint_x: 0.25
                    padding: [10, 5]
                    Button:
                        id: plot_exec
                        size_hint_y: 0.2
                        background_color: 0.5, 0.8, 0.5, 1
                        halign: "center"
                        text: "POKAŻ\\nWYKRES"
                        on_press: mf.update()
                
<MessageBox>:
    rows:1
    id: err_window
    Label:
        halign: "center"
        text: err_window.message
        size_hint: 0.8, 0.2
        pos_hint: {"x":0, "top":1}                
    '''

    ##########################################################################################
    #############################   additional info-string     ###############################
    ##########################################################################################

    # info for the 'help-button'
    help_str = '''
Aby zobaczyć wzory wpisanych funkcji, 
skorzystaj z polskiej notacji funkcji i liczb
(z ograniczeniami do symboli z klawiatury).

Cała funkcjonalność jest dostępna także na
klawiaturze ekranowej.

Dostępne są tylko funkcje jedej zmiennej.

Zapisuj same wzory funkcji; oddzielaj je średnikiem. 
    '''

    ##########################################################################################
    #############################           GUI classes        ###############################
    ##########################################################################################

    class MessageBox(GridLayout):
        '''
        Message box class. Inherts from grid layout.
        :artibte message: text to show in the box (str) 
        '''
        message = StringProperty()

        def __init__(self, mess: str, **kwargs):
            super(MessageBox, self).__init__(**kwargs)
            self.message = mess

    def show_error_box(err_mess: str):
        '''
        Show the message box with given error info.
        :param err_mess: error info (str)
        '''
        show = MessageBox(err_mess)
        popup_window = Popup(title="Nieprawidłowe dane.",
                             content=show, size_hint=(None, None), size=(400, 200))
        popup_window.open()

    def show_help(help_mess):
        '''
        Show the message box with given helping info.
        :param help_mess: helping info (str)
        '''
        show = MessageBox(help_mess)
        popup_window = Popup(title="Pomoc.",
                             content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()

    class PlotFigure(FigureCanvasKivyAgg):
        '''
        Basic app class servicing its main part - figure.
        :attribute: formulas_input: raw formulas text (str)
        :attribute: xmin_input: minimal argument (str)
        :attribute: xmax_input: maximal argument (str)
        :attribute: ymin_input: minimal value (str)
        :attribute: ymax_input: maximal value (str)
        :attribute: title_input: plot title (str)
        :attribute: xlabel_input: arguments axis label (str)
        :attribute: ylabel_input: values axis label (str)
        :attribute: legend_input: legend presence (bool)

        :method update: Update the figure with new data.
        :method helper: Show the helper window.
        '''
        formulas_input = ''
        xmin_input = '-5'
        xmax_input = '5'
        ymin_input = '-5'
        ymax_input = '5'
        title_input = 'Wykres'
        xlabel_input = 'Argumenty'
        ylabel_input = 'Wartości'
        legend_input = True

        def update(self):
            '''
            Update the figure with plot.
            In case of invalid data, service an error with error box.
            '''
            ranges = [float(re.sub(r',', r'.', numb)) for numb in [
                self.xmin_input, self.xmax_input, self.ymin_input, self.ymax_input]]
            try:
                plot_funct(parse_formulas(self.formulas_input), (ranges[0], ranges[1]), (
                    ranges[2], ranges[3]), self.legend_input, self.title_input, self.xlabel_input, self.ylabel_input)
                self.draw()
            except Exception as err:
                show_error_box(str(err))

        def helper(self):
            '''
            Show the helper window.
            '''
            show_help(help_str)

        def __init__(self, **kwargs):
            super(PlotFigure, self).__init__(plt.gcf(), **kwargs)
            self.update()

    # ** succeeding two classes based on the ones found on stackoverflow.com *********
    class CommaFloatInput(TextInput):
        '''
        Class for text input allowing only polish float notation.
        '''
        pat = re.compile('[^0-9\-]')

        def insert_text(self, substring, from_undo=False):
            pat = self.pat
            if ',' in self.text:
                s = re.sub(pat, '', substring)
            else:
                s = ','.join([re.sub(pat, '', s)
                             for s in substring.split(',', 1)])
            return super(CommaFloatInput, self).insert_text(s, from_undo=from_undo)

    class AsciiInput(TextInput):
        '''
        Class for text input allowing only ascii letters and symbols from global dictionaries.
        '''
        operators_strl = re.escape(''.join([';']+list(symbols_oper.keys(
        ))+list(symbols_spec_oper.keys())+list(symbols_brack.keys())))
        pat = re.compile(r'[^0-9a-zA-Z\s'+operators_strl+']')

        def insert_text(self, substring, from_undo=False):
            pat = self.pat
            s = re.sub(pat, '', substring)

            return super(AsciiInput, self).insert_text(s, from_undo=from_undo)

    # *********************************************************************************

    ##########################################################################################
    #############################           execution          ###############################
    ##########################################################################################

    # Window configuration and app execution
    Config.set('graphics', 'width', 1200)
    Config.set('graphics', 'height', 700)
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 100)
    Config.set('graphics', 'top',  50)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.write()

    class PlotApp(App):
        '''
        Main app class.
        :method build: Build and app using kivy lang script.
        '''
        def build(self):
            '''
            Build an app and set title.
            '''
            self.title = ' Kalkulator graficzny'
            return Builder.load_string(kv)

    PlotApp().run()
