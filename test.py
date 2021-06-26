import os
from pync import Notifier
import webbrowser
from mechanize import Browser
from bs4 import BeautifulSoup
import re
import mechanize
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))
    #webbrowser.open("https://selfregistration.cowin.gov.in")

notify(title    = 'Aster MIMS',
       subtitle = 'vaccine',
       message  = 'Opening webbrowser')