#!/usr/bin/env python3
# Register entry is a Python (version 3) GTK3 program to register entry into buildings, offices etc (due to COVID)
# Copyright (c) 2021, Iwan van der Kleijn (iwanvanderkleijn@gmail.com)
# This is Free Software (BSD). See the file LICENSE.txt

import gi
import os, os.path
from datetime import datetime
from openpyxl import load_workbook

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import platform
global osk #onscreen keyboard
if platform.system() == "Windows":
    osk = "osk"
else: #only on Linux and must be installed. Will fail on MacOSX 
    osk = "onboard"

def read_employees():
    xlsx_path = os.path.join(os.getcwd(),"employees.xlsx")
    #print(xlsx_path)
    wb = load_workbook(xlsx_path)
    ws = wb.worksheets[0]
    people_list  = [[str(e[0]),str(e[1]),str(e[2])] for e in ws.values if e != (None, None, None)]

    return people_list[1:]

def write_registered(id, name,surname, mask_num, employee):
    xlsx_path = os.path.join(os.getcwd(),"registered.xlsx")
    #print(xlsx_path)
    wb = load_workbook(xlsx_path)
    # Select First Worksheet
    ws = wb.worksheets[0]

    # Append Row Values
    ws.append([datetime.now(), id, name, surname, mask_num, employee])

    wb.save(xlsx_path)

class DialogMasks(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Select Mask number (2 max.)", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,"None (0)", 0, "1 mask", 1, "2 masks", 2)

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Please select how many masks have been taken")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Register Entry")
        self.set_border_width(10)

        # Setting up the self.grid in which the elements are to be positioned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        label_id = Gtk.Label(label="ID")
        label_name = Gtk.Label(label="Name")
        label_surname = Gtk.Label(label="Surname")

        self.entry_id = Gtk.Entry(text="", placeholder_text="i.e NIF, NIE, Passport nr, etc.")
        self.entry_name = Gtk.Entry(text="", placeholder_text="One or all first names")
        self.entry_surname = Gtk.Entry(text="", placeholder_text="One or all family names")

        self.grid.attach(label_id, 0, 0, 2, 1)
        self.grid.attach_next_to(label_name,label_id, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(label_surname,label_name, Gtk.PositionType.RIGHT, 2, 1)

        self.grid.attach_next_to(self.entry_id,label_id, Gtk.PositionType.BOTTOM, 2, 1)
        self.grid.attach_next_to(self.entry_name,self.entry_id, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(self.entry_surname,self.entry_name, Gtk.PositionType.RIGHT, 4, 1)


        self.button_osk = Gtk.Button()
        self.button_osk.add(Gtk.Image.new_from_file("keyboard.png"))
        self.button_osk.connect("clicked", self.on_screen_keyboard)
        self.grid.attach(self.button_osk, 0, 2, 2, 2)

        self.button_new_reg = Gtk.Button(label="New entry (unregistered)")
        self.button_new_reg.connect("clicked", self.on_new_entry_button_clicked)
        self.grid.attach_next_to(self.button_new_reg,self.button_osk, Gtk.PositionType.RIGHT, 2, 2)
        

        self.filter_text = Gtk.SearchEntry(text="", placeholder_text="Filter for list of employees (down)")
        self.filter_text.connect("search-changed", self.on_filter_text_changed)
        self.grid.attach(self.filter_text, 0, 4, 6, 1)

        # Creating the ListStore model
        self.people_liststore = Gtk.ListStore(str, str, str)
        for people_ref in read_employees():
            self.people_liststore.append(list(people_ref))

        # Creating the filter, feeding it with the liststore model
        self.people_filter = self.people_liststore.filter_new()
        # setting the filter function
        self.people_filter.set_visible_func(self.people_filter_func)

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(model=self.people_filter)
        for i, column_title in enumerate(["ID", "First name", "Surname"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        self.reg_employee = Gtk.Button(label="Entree of Employee")
        self.reg_employee.connect("clicked", self.on_reg_employee_button_clicked)

        # setting up the layout, putting the treeview in a scrollwindow
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 5, 8, 20)
        self.grid.attach_next_to(self.reg_employee, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 2, 2)

        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def people_filter_func(self, model, iter, data):

        current_filter_str = self.filter_text.get_text().strip()
        if (current_filter_str == ""):
            return True
        else:
            text =  model[iter][0] +  model[iter][1] +  model[iter][2]
            return text.find(current_filter_str) > -1

    def on_filter_text_changed(self,widget):
        self.people_filter.refilter()

    def info_msg(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()

    def error_msg(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
            text=message,
        )
        dialog.run()
        dialog.destroy()

    def reset_input(self):
        self.filter_text.set_text("")
        self.entry_id.set_text("")
        self.entry_name.set_text("")
        self.entry_surname.set_text("")

    def on_reg_employee_button_clicked(self, widget):
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is None:
            self.error_msg("Employee needs to be selected")
        else:
            id = model[treeiter][0]
            name = model[treeiter][1]
            surname = model[treeiter][2]

            mask_num = self.run_mask_dialog()
            if not mask_num == Gtk.ResponseType.CANCEL:
                write_registered(id, name, surname, str(mask_num), "yes")
                self.info_msg(f"Registered entry of: {name} {surname}")
            self.reset_input()

    def on_screen_keyboard(self, widget):
        global osk
        os.popen(osk)

    def on_new_entry_button_clicked(self, widget):

        id = self.entry_id.get_text().strip()
        name = self.entry_name.get_text().strip()
        surname = self.entry_surname.get_text().strip()
        if (id == "" or name == "" or surname == ""):
            self.error_msg("All fields need to be filled")
        else:

            mask_num = self.run_mask_dialog()
            if not mask_num == Gtk.ResponseType.CANCEL:
                write_registered(id, name, surname, str(mask_num), "no")
                self.info_msg(f"Registered entry of: {name} {surname}")
            self.reset_input()

    def run_mask_dialog(self):
        dialog = DialogMasks(self)
        response = dialog.run()

        dialog.destroy()
        return response

win = TreeViewFilterWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
