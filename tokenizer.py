# -*- coding: utf-8 -*-

import wiserdb
import postings
import InvertedIndex
from pprint import pprint

def text_to_postings_list(document_id, text, n, ii_buffer) :

    tokens = ngram_next(text, n)  # 入力文字列を N-gram に分解する
    for position, token in enumerate(tokens) :
        try :
            # 検索の場合は、最後のN-gramに満たない端文字のトークンを使わない
            if len(token) > n or document_id != 0 :
                # UTF-32 → UTF-8
                uni_text = unicode(token, 'utf_32')
                utf8_text = uni_text.encode('utf_8')

                # tokenからポスティングリストを構築
                buffer_ii = token.token_to_postings_list(document_id, utf8_text, position, ii_buffer)
        except UnicodeDecodeError :
            pprint(vars(UnicodeDecodeError.reason.__dict__))

    # テンポラリ転置インデックスに登録
    if ii_buffer is not None :
        postings.merge_inverted_index(ii_buffer, buffer_ii)
    else :
        ii_buffer = buffer_ii

def is_ignored_char(char) :
    return False

def ngram_next(str, n) :
    token = ''
    tokens = []
    i = 0
    while i < len(str) :
        for c in str[i:i + n] :
            if not is_ignored_char(c) :
                token += c
        tokens.append(token)
        token = ''
        i += 1

    return tokens

def token_to_postings_list(document_id, token, position, ii_buffer) :
    # DBよりトークンIDの取得
    (token_id, docs_count) = wiserdb.db_get_token_id(token)

    # 既存のテンポラリ転置インデックスがある
    if ii_buffer is not None :
        ii_entry = find_token_from_index(token_id, ii_buffer)
    else :
        ii_entry = None

    if ii_entry is not None :
        # トークンに紐づく既存のポスティングリストがある
        pl = ii_entry.postings_list
        exist = False
        for pl_entry in pl :
            # 既にそのトークンを含む文書がある
            if pl_entry.document_id == document_id :
                # copied = copy.copy(pl_entry)
                pl_entry.positions_count += 1
                pl_entry.positions.append(position)
                exist = True
                break
        # そのトークンが初登場の文書
        if not exist :
            pl_entry = InvertedIndex.PostingsListEntry(document_id, 1, position)
            pl.append(pl_entry)
            ii_entry.docs_count += 1
        ii_entry.positions_count += 1
        ii_entry.postings_list = pl
    else :
        # 紐づく既存のポスティングリストがない
        pl_entry = InvertedIndex.PostingsListEntry(document_id, 1)
        pl_entry.positions.append(position)
        ii_entry = InvertedIndex.InvertedIndexEntry(token_id, docs_count, 1)
        ii_entry.postings_list.append(pl_entry)
        ii_buffer.append(ii_entry)

    return ii_buffer


def find_token_from_index(token_id, ii) :
    for ii_entry in ii :
        if ii_entry.token_id == token_id :
            return ii_entry
    return None
