"""
coinbase-trader-gtk
Copyright (C) 2014  Shanthanu Bhardwaj

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import gtk
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import algos
from matplotlib import dates

class order_box(gtk.Window):
    def __init__(self, a=None):
        super(order_box, self).__init__()
        
	
        self.connect("destroy", gtk.main_quit)
        self.set_size_request(300, 200)
        self.set_position(gtk.WIN_POS_CENTER)
	
	if(a[0] == "Buy"):
		self.set_title("Create Buy Order")
		s="Buy"
	else:
		self.set_title("Create Sell Order")
		s="Sell"
	self.curr="BTC"
	
	label_bs = gtk.Label(s+" Amount: ")
	self.fixed = gtk.Fixed()
	self.fixed.put(label_bs, 10,14)
        self.qty = gtk.Entry()
        self.qty.set_text("1")
	self.qty.set_size_request(70,25)
	self.fixed.put(self.qty, 100,10)
	
	#curr_store = gtk.ListStore(str)
	curr_combo = gtk.combo_box_new_text()
        curr_combo.append_text("BTC")
        curr_combo.append_text("USD")
	curr_combo.set_active(0)
        curr_combo.connect("changed", self.curr_changed)
	
	cond_combo = gtk.combo_box_new_text()
        cond_combo.append_text("If BTC/USD is less than")
        cond_combo.append_text("If BTC/USD is more than")
	if(s == "Buy"):
		cond_combo.set_active(0)
		self.cond = "<"
	else:
		cond_combo.set_active(1)
		self.cond = ">"
        cond_combo.connect("changed", self.cond_changed)
	
	curr_combo.set_size_request(70,25)
	self.fixed.put(curr_combo, 180,10)
	
	cond_combo.set_size_request(185,25)
	self.fixed.put(cond_combo, 10,50)
	
        self.rate = gtk.Entry()
        self.rate.set_text(a[4])
	self.rate.set_size_request(70,25)
	self.fixed.put(self.rate, 200,50)
	
        btn_ok = gtk.Button("Create Order")
	btn_ok.set_size_request(100,25)
	btn_ok.connect("clicked", self.ok_clicked,a)
	self.fixed.put(btn_ok, 100, 80)
	
	
        self.add(self.fixed)
        self.show_all()

    def ok_clicked(self,button,a):
	z=["Buy",1,"BTC","<",0.0,-1] # Buy/Sell QTY BTC/USD >/< Rate state
	a[1]=float(self.qty.get_text())
	a[2]=self.curr
	a[3]=self.cond
	a[4]=float(self.rate.get_text())
	a[5]=+1
	self.destroy()#gtk.main_quit()

    def curr_changed(self,combobox):
	index = combobox.get_active()
	if (index == 0):
		self.curr = "BTC"
	else:
		self.curr="USD"

    def cond_changed(self,combobox):
	index = combobox.get_active()
	if (index == 0):
		self.cond ="<"
	else:
		self.cond = ">"

def create_order(a):
	order_box(a)
	gtk.main()

