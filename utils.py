import os

import pandas as pd

from db import get_conn


def get_reports() -> list[str]:
    """ Returns a list of file names in the specified folder. """
    folder_path = "reports"
    entries = os.listdir(folder_path)
    files = [entry for entry in entries if os.path.isfile(os.path.join(folder_path, entry))]
    return files


def get_df(limit=10, fund_id=None):
    conn = get_conn()
    query = "select fund_mf_id, document_mf_id, fund_name, document_type, document_text from fund_document_v2 " \
            "where document_type in ('quarterly_report', 'investor_letter', 'monthly_report') "
    if fund_id:
        query += f"and fund_mf_id = {fund_id} "
    query += f"order by fund_mf_id limit {limit}"
    documents = conn.execute(query).fetchall()

    docs = pd.DataFrame([list(d) for d in documents],
                        columns=['fund_mf_id', 'document_mf_id', 'fund_name', 'document_type', 'document_text'])
    return docs
