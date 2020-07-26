from secedgar.filings import Filing, FilingType
from secedgar.utils import get_cik_map
import pandas as pd
import os


path = 'E:\stockdata3\Filings'
filing = Filing(cik_lookup='msft', filing_type=FilingType.FILING_10K, count=10)
filing.save(path)
pass