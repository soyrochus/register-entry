#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

people_list = [
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python"),
    ("X7286364X", "Iwan Rochus", "van der Kleijn"),
    ("A1234567", "Marta", "Martinez de los Santos"),
    ("B456432", "Inma", "Pastor"),
    ("X1234X", "Pytha", "Python")

]


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

        label_id = Gtk.Label("ID")
        # label_id.set_width_chars(5)
        label_id = Gtk.Label("ID")
        # label_id.set_width_chars(5)
        label_name = Gtk.Label("Name")
        # label_id.set_width_chars(5)
        label_surname = Gtk.Label("Surname")
        # label_id.set_width_chars(5)

        label_box.pack_start(label_id, False, False, 0)
        label_box.pack_start(label_name, False, False, 0)
        label_box.pack_start(label_surname, False, False, 0)
        self.grid.attach(label_box, 0, 0, 8, 1)

        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        entry_id = Gtk.Entry()
        entry_name = Gtk.Entry()
        entry_surname = Gtk.Entry()

        entry_box.pack_start(entry_id, False, False, 0)
        entry_box.pack_start(entry_name, False, False, 0)
        entry_box.pack_start(entry_surname, False, False, 0)
        self.grid.attach(entry_box, 0, 1, 8, 1)

        self.filter_text = Gtk.SearchEntry()
        self.grid.attach(self.filter_text, 0, 2, 6, 1)

        # Creating the ListStore model
        self.people_liststore = Gtk.ListStore(str, str, str)
        for people_ref in people_list:
            self.people_liststore.append(list(people_ref))
        self.current_filter_str = None

        # Creating the filter, feeding it with the liststore model
        self.people_filter = self.people_liststore.filter_new()
        # setting the filter function, note that we're not using the
        self.people_filter.set_visible_func(self.people_filter_func)

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(model=self.people_filter)
        for i, column_title in enumerate(
                ["ID", "First name", "Surname"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for prog_language in ["Java", "C", "C++", "Python", "None"]:
            button = Gtk.Button(label=prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 3, 8, 20)
        self.grid.attach_next_to(
            self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1
        )
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(
                button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1
            )
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def people_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if (
                self.current_filter_str is None
                or self.current_filter_str == "None"
        ):
            return True
        else:
            return model[iter][2] == self.current_filter_str

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        # we set the current language filter to the button's label
        self.current_filter_str = widget.get_label()
        print("%s language selected!" % self.current_filter_str)
        # we update the filter, which updates in turn the view
        self.people_filter.refilter()


win = TreeViewFilterWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
