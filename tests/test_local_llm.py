import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.llm import LMStudio, extract, verify


class LocalLLMTests(unittest.TestCase):
    def response(self, result, finish='stop'):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({
            'choices':[{'finish_reason':finish,'message':{'content':json.dumps(result)}}],
            'usage':{'total_tokens':42}}).encode()
        return response

    def test_local_request_schema_cache_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp, patch('src.llm.DATA', Path(tmp)):
            with patch('urllib.request.urlopen', return_value=self.response({'claims':[]})) as http:
                client = LMStudio()
                result = extract(client, [{'pdf_page':1,'text':'Nothing relevant.'}],
                                 {'report_id':'r','company':'A','report_year':2024})
                self.assertEqual(result['metadata']['provider'], 'lmstudio')
                request = http.call_args.args[0]
                self.assertEqual(request.full_url, 'http://127.0.0.1:1234/v1/chat/completions')
                self.assertEqual(json.loads(request.data)['response_format']['type'], 'json_schema')
                again = extract(client, [{'pdf_page':1,'text':'Nothing relevant.'}],
                                {'report_id':'r','company':'A','report_year':2024})
                self.assertTrue(again['metadata']['cache_hit'])
                self.assertEqual(http.call_count, 1)

    def test_truncated_response_never_cached(self):
        with tempfile.TemporaryDirectory() as tmp, patch('src.llm.DATA', Path(tmp)):
            with patch('urllib.request.urlopen', return_value=self.response({'claims':[]}, 'length')):
                with self.assertRaises(RuntimeError):
                    LMStudio().generate('Extract', {'pages':[]})
                self.assertFalse(list(Path(tmp).rglob('*.json')))

    def test_bad_citation_repair_remains_validated(self):
        client = unittest.mock.Mock()
        bad = dict(label='supported', rationale='test', flags=[],
                   evidence_refs=[dict(chunk_id='r:1',pdf_page=1,quote='invented')])
        client.generate.return_value = (bad, {'model':'test'})
        with self.assertRaises(ValueError):
            verify(client, {'report_id':'r'}, [dict(report_id='r',chunk_id='r:1',pdf_page=1,text='original')])
        self.assertEqual(client.generate.call_count, 2)


if __name__ == '__main__':
    unittest.main()
