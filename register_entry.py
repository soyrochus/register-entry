#!/usr/bin/env python3
# Register entry is a Python (version 3) GTK3 program to register entry into buildings, offices etc (due to COVID)
# Copyright (c) 2021, Iwan van der Kleijn (iwanvanderkleijn@gmail.com)
# This is Free Software (BSD). See the file LICENSE.Tex

import sys
import gi
import os, os.path
from data import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

logo_image = os.path.join(os.path.dirname(__file__), "logo.png")
keyboard_image = os.path.join(os.path.dirname(__file__), "keyboard.png")
icon_image = os.path.join(os.path.dirname(__file__), "entry.png")
app_css = os.path.join(os.path.dirname(__file__), "styles.css")

if len(sys.argv) == 2:
    basedir = sys.argv[1]
else:
    basedir = os.getcwd()

settings = Gtk.Settings.get_default()

import platform
if platform.system() == "Windows":  #osk -> onscreen keyboard or equivalent
    osk = "osk"
else:  # only on Linux and must be installed. Will fail on MacOSX
    osk = "onboard"
class ExtraDataDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Select Mask number (2 max.)", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "None (0)", 0, "1 mask", 1, "2 masks", 2)

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Please select how many masks have been taken")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

def load_store(liststore, lst):
    liststore.clear()
    for ref in lst:
        liststore.append(list(ref))

class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Register Entry")
        self.set_icon_from_file(icon_image)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        stack.set_transition_duration(300)
        self.setup_list_panel(stack)
        self.setup_form_panel(stack)

        logo = Gtk.Image.new_from_file(logo_image)
        logo.props.halign = Gtk.Align.START
        vbox.pack_start(logo, False, False, 0)

        button_osk = Gtk.Button(label="Open Keyboard")
        button_osk.set_image(Gtk.Image.new_from_file(keyboard_image))
        button_osk.set_always_show_image(True)
        button_osk.set_image_position(Gtk.PositionType.TOP)
        button_osk.connect("clicked", self.on_screen_keyboard)
        button_osk.props.halign = Gtk.Align.END

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        hbox.pack_start(stack_switcher, False, False, 0)
        hbox.pack_start(button_osk, True, False, 0)

        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(stack, True, True, 0)
        self.stack = stack

        self.styling_app()
        self.show_all()
        self.grab_focus_active_input()

    def styling_app(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        provider.load_from_path(app_css)

    def setup_form_panel(self, stack):

        panel_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        panel_box.get_style_context().add_class("box")
        label_form = Gtk.Label(label="Register here with your ID, name and surname if you register for the "
                  "first time (check employee)")
        label_form.set_halign(Gtk.Align.START)
        label_form.set_name("formlabel")
        panel_box.pack_start(label_form, False, False, 0)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(False)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        label_id = Gtk.Label(label="ID")
        label_id.set_halign(Gtk.Align.START)
        label_name = Gtk.Label(label="Name")
        label_name.set_halign(Gtk.Align.START)
        label_surname = Gtk.Label(label="Surname")
        label_surname.set_halign(Gtk.Align.START)

        check_employee = Gtk.CheckButton(label="Employee")
        entry_id = Gtk.Entry(text="", placeholder_text="i.e NIF, NIE, Passport nr, etc.")
        entry_name = Gtk.Entry(text="", placeholder_text="One or all first names")
        entry_surname = Gtk.Entry(text="", placeholder_text="One or all family names")

        grid.attach(check_employee, 1, 0, 1, 1)
        grid.attach(label_id, 0, 1, 1, 1)
        grid.attach_next_to(entry_id, label_id, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach(label_name,0, 2, 1, 1)
        grid.attach_next_to(entry_name, label_name, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach(label_surname,0, 3, 1, 1)
        grid.attach_next_to(entry_surname, label_surname, Gtk.PositionType.RIGHT, 2, 1)

        self.entry_id = entry_id
        self.entry_name = entry_name
        self.entry_surname = entry_surname
        self.check_employee = check_employee

        panel_box.pack_start(grid, True, True, 0)
        stack.add_titled(panel_box, "form", "First time registration")

        button_new_reg = Gtk.Button(label="Register Entry")
        button_new_reg.connect("clicked", self.on_new_entry_button_clicked)
        button_new_reg.props.halign = Gtk.Align.END
        button_new_reg.get_style_context().add_class("buttonregperson")
        panel_box.pack_start(button_new_reg, False, False, 0)


    def setup_list_panel(self, stack):
        # Setting up the self.grid in which the elements are to be positioned

        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        list_box.get_style_context().add_class("box")
        label_entry_from_list = Gtk.Label(label="Lookup and choose your name from the list below")
        label_entry_from_list.set_halign(Gtk.Align.START)
        label_entry_from_list.set_name("searchlabel")
        list_box.pack_start(label_entry_from_list, False, False, 0)

        filter_text = Gtk.SearchEntry(text="", placeholder_text="Filter for list of people (down)")
        filter_text.connect("search-changed", self.on_filter_text_changed)
        list_box.pack_start(filter_text, False, False, 0)
        self.filter_text = filter_text
        filter_text.set_name("filtertext")

        # Creating the ListStore model
        self.people_liststore = Gtk.ListStore(str, str, str)
        load_store(self.people_liststore, read_people())

        # Creating the filter, feeding it with the liststore model
        self.people_filter = self.people_liststore.filter_new()
        # setting the filter function
        self.people_filter.set_visible_func(self.people_filter_func)

        # creating the treeview, making it use the filter as a model, and adding the columns
        treeview = Gtk.TreeView(model=Gtk.TreeModelSort(model=self.people_filter))
        treeview.connect("row-activated", self.on_reg_person_clicked)
        for i, column_title in enumerate(["ID", "First name", "Surname"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sort_column_id(i)
            treeview.append_column(column)
            if i == 0:
                column.set_visible(False) #Hide ID
        self.treeview = treeview
        # setting up the layout, putting the treeview in a scrollwindow
        scrollable_treelist = Gtk.ScrolledWindow()
        scrollable_treelist.set_vexpand(True)
        scrollable_treelist.add(treeview)
        list_box.pack_start(scrollable_treelist, True, True, 0)

        reg_person = Gtk.Button(label="Register Entry")
        reg_person.connect("clicked", self.on_reg_person_clicked)
        reg_person.props.halign = Gtk.Align.END
        reg_person.get_style_context().add_class("buttonregperson")
        list_box.pack_start(reg_person, False, False, 0)

        stack.add_titled(list_box, "list", "Select your name\nonce registered")

    def people_filter_func(self, model, iter, data):

        current_filter_str = self.filter_text.get_text().strip().lower()
        if current_filter_str == "":
            return True
        else:
            text = (model[iter][0] + model[iter][1] + model[iter][2]).lower()
            return text.find(current_filter_str) > -1

    def on_filter_text_changed(self, widget):
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

        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter != None:
            selection.unselect_iter(treeiter)

        self.filter_text.set_text("")
        self.entry_id.set_text("")
        self.entry_name.set_text("")
        self.entry_surname.set_text("")
        self.check_employee.set_active(False)
        self.grab_focus_active_input()

    def on_reg_person_clicked(self, ignore=None, ignore2=None, ignore3=None, ignore4=None):
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is None:
            self.error_msg("Person needs to be selected")
        else:
            id = model[treeiter][0]
            name = model[treeiter][1]
            surname = model[treeiter][2]

            mask_num = self.run_extra_data_dialog()
            if mask_num != Gtk.ResponseType.CANCEL and mask_num != Gtk.ResponseType.CLOSE and mask_num != Gtk.ResponseType.DELETE_EVENT:
                write_entry(id, name, surname, str(mask_num), "yes")
                self.info_msg(f"Registered entry of: {name} {surname}")
            self.reset_input()

    def grab_focus_active_input(self):
        if self.stack.props.visible_child_name == "form":
            self.check_employee.grab_focus()
        else:
            self.filter_text.grab_focus()

    def on_screen_keyboard(self, widget):
        os.popen(osk)
        self.grab_focus_active_input()

    def on_new_entry_button_clicked(self, widget):

        id = self.entry_id.get_text().strip()
        name = self.entry_name.get_text().strip()
        surname = self.entry_surname.get_text().strip()
        if id == "" or name == "" or surname == "":
            self.error_msg("All fields need to be filled")
        else:
            mask_num = self.run_extra_data_dialog()
            if mask_num != Gtk.ResponseType.CANCEL and mask_num != Gtk.ResponseType.CLOSE and mask_num != Gtk.ResponseType.DELETE_EVENT:
                is_employee = "yes" if self.check_employee.get_active() else "no"

                write_entry(id, name, surname, str(mask_num), is_employee)
                write_person(id, name, surname, is_employee)
                load_store(self.people_liststore, read_people())

                self.info_msg(f"Registered entry of: {name} {surname}")
            self.reset_input()

    def run_extra_data_dialog(self):
        dialog = ExtraDataDialog(self)
        response = dialog.run()

        dialog.destroy()
        return response

win = TreeViewFilterWindow()
win.connect("destroy", Gtk.main_quit)

win.maximize()
win.set_resizable(True)
# win.full screen()

win.show_all()
Gtk.main()
