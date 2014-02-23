#!/usr/bin/python

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

import time
import gtk
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import algos
from matplotlib import dates
import createOrder
from string import maketrans

class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()
       
	self.reset=1000*60*10
	self.interval=30*1000
	self.n=0
	self.selected = []
	self.buyprice=''
	self.sellprice=''
	self.balance=''

        self.connect("destroy", gtk.main_quit)
        self.set_size_request(690, 600)
        self.set_position(gtk.WIN_POS_CENTER)
	self.set_title("Coinbase Trader")

	self.hfmt = dates.DateFormatter('%b %d')

	self.fixed = gtk.Fixed()

	self.btn_buy = gtk.Button("Buy BTC")
	self.btn_buy.set_size_request(110,25)
	self.btn_buy.connect("clicked",self.buy_clicked)
        self.fixed.put(self.btn_buy, 570, 350)
	self.btn_buy.set_sensitive(False)
	
        self.btn_sell = gtk.Button("Sell BTC")
	self.btn_sell.set_size_request(110,25)
	self.btn_sell.connect("clicked",self.sell_clicked)
        self.fixed.put(self.btn_sell, 570, 385)
	self.btn_sell.set_sensitive(False)
        
	self.btn_del = gtk.Button("Delete")
        self.btn_del.set_size_request(110,25)
	self.btn_del.connect("clicked",self.del_clicked)
	self.fixed.put(self.btn_del, 570, 420)
	self.btn_del.set_sensitive(False)
	
	#self.btn_TRY = gtk.Button("TRY")
        #self.btn_TRY.set_size_request(110,25)
	#self.btn_TRY.connect("clicked",self.TRY)
	#self.fixed.put(self.btn_TRY, 570, 490)
	"""self.btn_save.set_sensitive(False)"""

	self.btn_load = gtk.Button("Begin")
        self.btn_load.set_size_request(110,25)
	self.btn_load.connect("clicked",self.load_clicked)
	self.fixed.put(self.btn_load, 570, 455)
	
	self.label_sell = gtk.Label("Sell: $"+self.sellprice)
	self.fixed.put(self.label_sell, 570, 490)
	self.label_buy = gtk.Label("Buy: $"+self.buyprice)
	self.fixed.put(self.label_buy, 570, 520)
	self.label_bal = gtk.Label("") #Balance: "+self.balance)
	self.fixed.put(self.label_bal, 570, 550)
	
	self.statusbar = gtk.Label("") #Balance: "+self.balance)
	self.fixed.put(self.statusbar, 10, 565)
	#------
	self.liststore = gtk.ListStore(bool, str)

        treeview = gtk.TreeView(model=self.liststore)
	
	renderer_radio = gtk.CellRendererToggle()
        renderer_radio.set_radio(False)
        renderer_radio.connect("toggled", self.order_selected)
	column_radio = gtk.TreeViewColumn("", renderer_radio, active=0)
        treeview.append_column(column_radio)

        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Orders", renderer_text, text=1)
        treeview.append_column(column_text)

	treeview.set_size_request(550,210)
	#------
	renderer_text.props.ellipsize=3 
	renderer_text.props.ellipsize_set= True #wrap_width = 80
	self.fixed.put(treeview,10,350)
	
	self.S=''
	self.n=0
	self.API_KEY=''
	self.API_SECRET=''
	self.pwd=''
	self.notAuth=True
	#self.load_file() #------------------------->COMMENT IT OUT LATER BUTTON WILL COME HERE

        self.add(self.fixed)
        self.show_all()
	self.update_graph()
	self.check_prices()
	
    def order_selected(self,widget,path):
	self.liststore[path][0] = not self.liststore[path][0]
	if (self.liststore[path][0]):
		self.selected.append(path)
	else:
		self.selected.remove(path)
	if(len(self.selected)>0):
		self.btn_del.set_sensitive(True)
	#print(self.selected)

    def buy_clicked(self,button):
	z=["Buy",1,"BTC","<",self.buyprice,-1] # Buy/Sell QTY BTC/USD >/< Rate state
	createOrder.create_order(z)
	if(z[5] > 0):
		ordo=z[0]+'\t'+str(z[1])+' '+z[2]+'\tif price '+z[3]+' '+str(z[4])
        	self.liststore.append([False, ordo])
		self.save_clicked() #btn_save.set_sensitive(True)
		

    def sell_clicked(self,button):
	z=["Sell",1,"BTC","<",self.sellprice,-1] # Buy/Sell QTY BTC/USD >/< Rate state
	createOrder.create_order(z)
	if(z[5] > 0):
		ordo=z[0]+'\t'+str(z[1])+' '+z[2]+'\tif price '+z[3]+' '+str(z[4])
        	self.liststore.append([False, ordo])
		self.save_clicked() #btn_save.set_sensitive(True)

    def del_clicked(self,button):
	self.selected.sort()
	self.selected.reverse()
	for i in self.selected:
		self.liststore.remove(self.liststore[i].iter)
	self.selected = [] #.clear()	
	self.btn_del.set_sensitive(False)
	self.save_clicked() #btn_save.set_sensitive(True)
  
    def load_clicked(self,button):
	if(button.get_label() == "Begin"):
		try:
			self.S,self.p,self.API_KEY,self.API_SECRET,self.pwd=algos.begin_auth()
			pp=self.p.split('\n')
			for tex in pp:
				if (tex !='') :
					self.liststore.append([False, tex])
			self.btn_buy.set_sensitive(True)
			self.btn_sell.set_sensitive(True)
	
			if (len(self.selected) > 0):
				self.btn_del.set_sensitive(True)
			self.btn_load.set_label("New Password")
			self.notAuth=False
			self.check_prices()
		except:
			print("Couldn't open file")
			raise
			return
		
	else:
		pold = algos.getText("","Current Password")
		count =0
		while( algos.pad(str(pold)) != self.pwd):
			pold = algos.getText("Incorrect Password","Current Password")
			count=count+1
			if(count == 5):
				return
		pwd = algos.getText('Enter new password','Password: ') #raw_input("Create passwd: ")
                pwd2 = algos.getText('','Re-enter new password') #raw_input("Re-enter passwd: ")
		count =0
                while (pwd != pwd2):
                        pwd = getText('Password mismatch, please try again','Password: ') # raw_input("Mismatched passwords.\nEnter: ")
                        pwd2 = getText('','Re-enter password') #raw_input("Re-enter passwd: ")  
			count = count +1
			if(count == 5):
				print("Password not changed")
                                return
                self.pwd = algos.pad(str(pwd)) #make it 32 chars long
	self.save_clicked()

		
    def save_clicked(self): #,button):
	self.p=''
	for k in self.liststore :
		self.p=self.p+k[1]+'\n'
	self.p=self.p[:-1]
	try:
		algos.end_auth(self.S,self.p,self.API_KEY,self.API_SECRET,self.pwd)
		#self.btn_save.set_sensitive(False)
	except:
		print("Couldn't save changes")
	
    def update_graph(self):
	self.f = Figure(figsize=(4,2.5), dpi=100)
        self.a = self.f.add_subplot(111)
	self.a.xaxis.set_major_formatter(self.hfmt)
	x,y=algos.update_mkt()
	self.a.plot(x,y)
	self.a.yaxis.grid()
	for item in ([self.a.title, self.a.xaxis.label, self.a.yaxis.label] + self.a.get_xticklabels() + self.a.get_yticklabels()):
    		item.set_fontsize(10)
	
        self.canvas = FigureCanvas(self.f)  # a gtk.DrawingArea
        self.canvas.set_size_request(670,330)
        self.fixed.put(self.canvas,10,10)
	self.show_all()
	return True

    def check_prices(self):
	s=algos.get_http("http://coinbase.com/api/v1/prices/buy").read()
	s=s.translate(maketrans(':',','),'[]{}\"').split(',')[-4:]
	if(s[3] == 'USD'):
		self.buyprice=s[1]
		self.label_buy.set_label("Buy: $"+self.buyprice)

	s=algos.get_http("http://coinbase.com/api/v1/prices/sell").read()
	s=s.translate(maketrans(':',','),'[]{}\"').split(',')[-4:]
	if(s[3] == 'USD'):
		self.sellprice=s[1]
		self.label_sell.set_label("Sell: $"+self.sellprice)
	if(self.notAuth):
		return True


	#We Have an API KEY :)	
	try:
		s = algos.get_https('https://coinbase.com/api/v1/account/balance',self.API_KEY,self.API_SECRET).read()
		s=s.translate(maketrans(':',','),'[]{}\"').split(',')
		if(s[0]=='amount' and s[3] == 'BTC'):
			self.balance=s[1]
			self.label_bal.set_label("Bal: "+self.balance)
		else:
			print("Wrong KEYS")
			self.notAuth=True
	except:
		print("Lost Internet connection perhaps?")

	for k in self.liststore :
		s=k[1]
		#check if this order is satisfied
		fullfillable=False;
		s=s.split()
		if(s[0] == "Sell"):
			price=float(self.sellprice)
		else:
			price=float(self.buyprice)
		if (s[5] == '>' and price > float(s[6]) ):
			fullfillable=True
		if (s[5] == '<' and price < float(s[6]) ):
                        fullfillable=True
		qty=float(s[1])
		if(s[2] == 'USD'):
			qty=qty/price
		if(fullfillable):
			try:
				bod='qty='+str(qty)
				if(s[0] == "Sell"):
					res=algos.get_https('https://coinbase.com/api/v1/sells',self.API_KEY,self.API_SECRET,bod).read()
					res=res.translate(maketrans(':',','),'[]{}\"').split(',')
					s=res[4]+": Sold "+s[1]+"BTC for "+res[20]+" "+res[48]
				if(s[0] == "Buy"):
					res=algos.get_https('https://coinbase.com/api/v1/buys',self.API_KEY,self.API_SECRET,bod).read()
					res=res.translate(maketrans(':',','),'[]{}\"').split(',')
					s=res[4]+": Bought "+s[1]+"BTC for "+res[20]+" "+res[48]
				
				if(res[:2] == ['success', 'true']):
					self.statusbar.set_label(s)	
					self.liststore.remove(k.iter)
					self.save_clicked() 	
			except:
				print("failed for some reason")
				fullfillable=False
				raise

	self.selected=[]
	i=0
	for k in self.liststore:
		if(k[0]):
			self.selected.append(str(i))
		i=i+1
	#self.clock.set_label('['+str(self.n)+']  '+str(time.strftime("%H:%M:%S")))
	self.n=self.n+1
	return True

def main():
	gtk.main()

if __name__ == "__main__":
	app=PyApp()
	gtk.timeout_add(app.reset, app.update_graph)
        gtk.timeout_add(app.interval, app.check_prices)

	main()

# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas


#win = gtk.Window()
#win.connect("destroy", lambda x: gtk.main_quit())
#win.set_default_size(400,300)
#win.set_title("Embedding in GTK")

#gtk.main()


