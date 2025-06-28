import unittest
from app import app, initialize_knowledge_graph_and_context
from flask import url_for

class ChatbotTests(unittest.TestCase):
    def setUp(self):
        # Set up Flask test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Initialize knowledge graph and LLM context
        initialize_knowledge_graph_and_context()

    def test_tc1_insat_3dr(self):
        response = self.client.post('/ask', data={'query': 'What is INSAT-3DR?'})
        self.assertIn(b'INSAT-3DR', response.data)
        self.assertIn(b'2016-09-08', response.data)
        self.assertIn(b'meteorological satellite', response.data)

    def test_tc2_chandrayaan(self):
        response = self.client.post('/ask', data={'query': 'Chandrayaan'})
        self.assertIn(b'Chandrayaan-1', response.data)
        self.assertIn(b'Chandrayaan-2', response.data)

    def test_tc3_mangalyaan(self):
        response = self.client.post('/ask', data={'query': 'Mangalyaan mission'})
        self.assertIn(b'Mangalyaan', response.data)
        self.assertIn(b'2013-11-05', response.data)

    def test_tc4_pslv_c37(self):
        response = self.client.post('/ask', data={'query': 'What is PSLV-C37?'})
        self.assertIn(b'PSLV-C37', response.data)
        self.assertIn(b'2017-02-15', response.data)

    def test_tc5_aditya(self):
        response = self.client.post('/ask', data={'query': 'Aditya solar mission'})
        self.assertIn(b'Aditya-L1', response.data)
        self.assertIn(b'2023-09-02', response.data)

    def test_tc6_gsat(self):
        response = self.client.post('/ask', data={'query': 'GSAT satellite'})
        self.assertIn(b'GSAT-11', response.data)
        self.assertIn(b'2018-12-05', response.data)

    def test_tc7_invalid(self):
        response = self.client.post('/ask', data={'query': 'Invalid Mission'})
        self.assertIn(b"Sorry, I couldn't find any information", response.data)

    def test_tc8_risat(self):
        response = self.client.post('/ask', data={'query': 'What is RISAT?'})
        self.assertIn(b'RISAT-2B', response.data)
        self.assertIn(b'2019-05-22', response.data)

    def test_tc9_cartosat(self):
        response = self.client.post('/ask', data={'query': 'Cartosat-2F details'})
        self.assertIn(b'Cartosat-2F', response.data)
        self.assertIn(b'2018-01-12', response.data)

    def test_tc10_gslv(self):
        response = self.client.post('/ask', data={'query': 'GSLV Mk III mission'})
        self.assertIn(b'GSLV-MkIII-D1', response.data)
        self.assertIn(b'2017-06-05', response.data)

    def test_tc11_chandrayaan_purpose(self):
        response = self.client.post('/ask', data={'query': 'What does Chandrayaan-2 do?'})
        self.assertIn(b'LLM Answer', response.data)
        self.assertIn(b'moon', response.data)  # Loose check due to LLM variability

    def test_tc12_mangalyaan_purpose(self):
        response = self.client.post('/ask', data={'query': 'Why was Mangalyaan launched?'})
        self.assertIn(b'LLM Answer', response.data)
        self.assertIn(b'Martian', response.data)  # Loose check due to LLM variability

if __name__ == '__main__':
    unittest.main()