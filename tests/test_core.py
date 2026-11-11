import copy
import unittest
from src.pipeline import BM25, norm, baseline_candidates
from src.numeric import check_rate
from src.llm import validate_claims, validate_assessment, verify
from src.evaluate import classification_metrics,retrieval_metrics

class NumericTests(unittest.TestCase):
    def setUp(self):
        self.scope=dict(company='A',year=2024,material='PET',geography='Global',boundary='Bottles',measurement_basis='Mass')
    def item(self,value,unit='t'):
        return dict(self.scope,value=value,unit=unit)
    def test_different_denominators(self):
        self.assertEqual(check_rate(self.item(2500),self.item(10000),25)['status'],'consistent')
        self.assertEqual(check_rate(self.item(2500),self.item(4000),62.5)['status'],'consistent')
        self.assertEqual(check_rate(self.item(2500),self.item(10000),62.5)['status'],'potential_inconsistency')
    def test_unit_normalization(self):
        self.assertEqual(check_rate(self.item(3000,'kg'),self.item(10),30)['calculated_percent'],30)
    def test_scope_mismatch_and_missing(self):
        for field in self.scope:
            item=self.item(3)
            item[field]=None
            self.assertEqual(check_rate(item,self.item(10),30)['status'],'not_comparable')
            item[field]='Different'
            self.assertEqual(check_rate(item,self.item(10),30)['status'],'not_comparable')
    def test_invalid_numbers(self):
        for n,d,p in [(1,0,10),(-1,10,10),(float('nan'),10,10),(1,10,float('inf'))]:
            self.assertEqual(check_rate(self.item(n),self.item(d),p)['status'],'invalid_input')

class GroundingTests(unittest.TestCase):
    def setUp(self):
        self.report=dict(report_id='r',company='A',report_year=2024)
        self.pages=[dict(pdf_page=1,text='Our plastic bottles contain 30% recycled PET.')]
    def test_valid_exact_quote(self):
        data={'claims':[dict(claim_text=self.pages[0]['text'],source_page=1,claim_type='recycled_content')]}
        ok,bad=validate_claims(data,self.pages,self.report)
        self.assertEqual((len(ok),len(bad)),(1,0))
    def test_fabricated_quote_and_wrong_page(self):
        for text,page in [('Our bottles contain 80% recycled PET.',1),(self.pages[0]['text'],2)]:
            ok,bad=validate_claims({'claims':[dict(claim_text=text,source_page=page,claim_type='recycled_content')]},self.pages,self.report)
            self.assertEqual((len(ok),len(bad)),(0,1))
    def test_citation_validation(self):
        ev=[dict(chunk_id='r:p1:c1',pdf_page=1,text=self.pages[0]['text'])]
        result=dict(label='supported',rationale='Test',evidence_refs=[dict(chunk_id='r:p1:c1',pdf_page=1,quote='30% recycled PET')])
        self.assertEqual(validate_assessment(result,ev)['label'],'supported')
        for field,value in [('quote','80% recycled PET'),('pdf_page',2),('chunk_id','other')]:
            bad=copy.deepcopy(result)
            bad['evidence_refs'][0][field]=value
            with self.assertRaises(ValueError): validate_assessment(bad,ev)
    def test_support_requires_evidence(self):
        with self.assertRaises(ValueError):
            validate_assessment(dict(label='supported',rationale='x',evidence_refs=[]),[])
    def test_cross_report_rejected(self):
        with self.assertRaises(ValueError):
            verify(None,dict(report_id='a'),[dict(report_id='b')])
    def test_future_claim_stays_unassessed_in_baseline(self):
        page=dict(self.report,pdf_page=1,packaging_relevant=True,text='By 2030, all our plastic packaging will be recyclable.')
        result=baseline_candidates(dict(pages=[page]))[0]
        self.assertEqual(result['claim_type'],'target')
        self.assertEqual(result['assessment'],'not_assessed')
    def test_decimal_claim_not_split(self):
        text='Our plastic packaging contains 62.5% recycled content.'
        page=dict(self.report,pdf_page=1,packaging_relevant=True,text=text)
        self.assertEqual(baseline_candidates(dict(pages=[page]))[0]['claim_text'],text)

class RetrievalTests(unittest.TestCase):
    def test_relevant_chunk_ranks_first(self):
        chunks=[dict(chunk_id='a',pdf_page=1,text='We support local schools.'),dict(chunk_id='b',pdf_page=2,text='Our plastic packaging uses recycled PET.')]
        result=BM25(chunks).search('recycled plastic packaging',3,exclude_text='Our plastic packaging uses recycled PET.')
        self.assertEqual(result[0]['chunk_id'],'b')
        self.assertTrue(result[0]['repeats_claim'])
    def test_empty_query(self):
        self.assertEqual(BM25([]).search('plastic'),[])
    def test_recall_uses_unique_pages(self):
        self.assertEqual(retrieval_metrics([1,2],[1,1,3])['page_recall_at_k'],0.5)

class EvaluationTests(unittest.TestCase):
    def test_no_gold_no_metrics(self):
        self.assertIsNone(classification_metrics([])['macro_f1'])
    def test_known_confusion(self):
        result=classification_metrics([('supported','supported'),('supported','insufficient_evidence'),('insufficient_evidence','insufficient_evidence')])
        self.assertAlmostEqual(result['accuracy'],2/3)
        self.assertAlmostEqual(result['macro_f1'],2/3)

if __name__=='__main__':unittest.main()
