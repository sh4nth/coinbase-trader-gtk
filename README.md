Coinbase-trader Gtk
===================

This is a Gtk Application for setting buy/sell limit orders on coinbase.com
I wrote this project mainly as a way to teach myself python and the Gtk API.  This also fills an important niche, as the web interface does not let you set limit orders and there seem to be no desktop applications that do this.

# Version
0.1

# Instructions

## Requirements
- [Coinbase Account](http://www.coinbase.com)
- [Python](http://www.python.org/downloads/)
- [PyGTK](http://www.pygtk.org/)
- [Matplotlib](http://matplotlib.org/downloads.html)

## Install
To install simply clone the repository or download the [zip](https://github.com/sh4nth/coinbase-trader-gtk/archive/master.zip) archive and run main.py

## Settings
1. You will need to create an API KEY buy going to https://coinbase.com/account/api
2. Give the key permission to `buy`, `sell` and view your `balance`
3. On the first run, you will be asked for a password and your `API_KEY` and `API_SECRET`
4. Your keys and order data will be stored in an AES encrypted file `$HOME/.coinbase-trader-gtk`
5. In case you forget your password you can delete the `$HOME/.coinbase-trader-gtk` file and re-enter the `API_KEY` and `API_SECRET`

## Interface
![The Coinbase-trader Gtk interface](http://i.imgur.com/02c7Yaj.png)
Once you have provided your `API_KEY` and `API_SECRET` you can ask the application to set `Buy` and `Sell` orders that will execute when the price is more or less than a particular value.

# TODO
- Improve UI and implement multi-threading and as well as option to minimize to system tray
- Improve error handling
- Add more complex trades, and sequential queued orders
- Make market graoh dynamic and enable zooming etc.


# Disclaimer

This program executes trades between your coinbase account and linked bank account using the Coinbase API.  Use and trade with this program at your own risk.  I am not liable for any losses incurred by using this software.
