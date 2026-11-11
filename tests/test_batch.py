import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

import run_llm
from src.common import save_json, load_json


class BatchTests(unittest.TestCase):
    def test_resume_and_config_change_preserve_previous_run(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(run_llm, 'DATA', Path(tmp)):
            root = Path(tmp)
            report = dict(report_id='r', company='A', report_year=2024)
            save_json(root/'manifest.json', [report])
            save_json(root/'processed/r.json', dict(pages=[dict(pdf_page=1, text='test', packaging_relevant=True)], chunks=[]))
            client = Mock(model='local', base_url='http://localhost/v1')
            result = dict(claims=[], rejected=[], processed_pages=[1], metadata={'model':'local'})
            with patch.object(run_llm, 'make_client', return_value=client), patch.object(run_llm, 'extract', return_value=result) as extract:
                with patch('sys.argv', ['run_llm.py','--stage','extract']):
                    run_llm.main()
                    run_llm.main()
                self.assertEqual(extract.call_count, 1)
                self.assertEqual(load_json(root/'results/summary.json')[0]['processed_pages'], 1)
                client.model = 'changed'
                with patch('sys.argv', ['run_llm.py','--stage','verify']):
                    with self.assertRaises(RuntimeError):
                        run_llm.main()
                self.assertEqual(load_json(root/'llm_claims/r.json')['config']['model'], 'local')
                with patch('sys.argv', ['run_llm.py','--stage','extract']):
                    run_llm.main()
                self.assertEqual(extract.call_count, 2)
                self.assertEqual(len(list((root/'run_archive').glob('*.json'))), 1)


if __name__ == '__main__':
    unittest.main()
