import unittest
from clock import *


class TestClock(unittest.TestCase):
    def test_current_w_h(self):
        resultado = Clock.current_w_h()
        # com canvas width = 1000 e height = 1000, o winfo_width e windo_height retornam 1004
        self.assertEqual(resultado,(1004,1004))

    def test_get_city_from_offset(self):
        resultado = Clock.get_city_from_offset()
        self.assertEqual(resultado,"Sao_Paulo")

    def test_polar2cartesian(self):
        # assumindo hora = 22 e min = 10
        resultado = Clock.polar2cartesian(11.6064395258,200.8)
        self.assertEqual(resultado,(-164.48573048888642,115.17414842549269))

    ## Nao sei como testar as outras funcoes, ja que elas nao possuem um return claro, na construcao
    ## eu fiz debug e testei os valores que passavam na draw_handle porem nao sei se era isso que deveria ter
    ## sido feito no unittest ja que nao possui um return

if __name__ == '__main__':
    Main = Tk()
    Clock = Clock(Main)
    unittest.main()