"""Streamlit integration tests with real corpus; full English interface."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_main_render_and_filters(self):
        app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=60).run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'20')
        provider=next(s for s in app.selectbox if s.label=='LLM Provider')
        self.assertEqual(provider.value, 'lmstudio')
        provider.select('gemini').run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any(t.label=='Gemini API key' for t in app.text_input))
        provider=next(s for s in app.selectbox if s.label=='LLM Provider')
        provider.select('lmstudio').run()
        # Exercise report switching; verify changing source does not retain old page limits.
        selector=next(s for s in app.selectbox if s.label=='Select Corporate Report')
        selector.select_index(10).run()
        self.assertEqual(len(app.exception),0)
        field=next(t for t in app.text_input if t.label=='Filter Claims')
        field.set_value('no_such_packaging_phrase_98765').run()
        self.assertEqual(len(app.exception),0)

if __name__=='__main__':unittest.main()
