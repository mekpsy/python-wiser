# -*- coding: utf-8 -*-

# テンポラリ転置インデックス
class tmp_ii :
    def __init__(self) :
        self.ii_buffer_count = 0 # 登録された文書数
        self.ii_buffer_count_threshold = 100 # ストレージの転置インデックスとマージする閾値
        self.ii_buffer = None # テンポラリ転置インデックス

# 転置インデックス
class InvertedIndexEntry :
    def __init__(self, token_id=None, docs_count=None, positions_count=None, postings_list=None) :
        self.token_id = token_id
        self.docs_count = docs_count
        self.positions_count = positions_count
        if postings_list is None :
            self.postings_list = []
        else :
            self.postings_list = postings_list

# ポスティングリスト
class PostingsListEntry :
    def __init__(self, document_id=None, positions_count=None, position=None) :
        self.document_id = document_id
        self.positions_count = positions_count
        if position is None :
            self.positions = []
        else :
            self.positions = [position]
