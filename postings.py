# -*- coding: utf-8 -*-
import pickle
import base64
import wiserdb
import InvertedIndex
import tokenizer
from pprint import pprint

def merge_postings(pl1, pl2) :
    result_pl = []

    for pl_entry in next_pl_entry(pl1, pl2) :
        result_pl.append(pl_entry)

    return result_pl

def next_pl_entry(pl1, pl2) :
    pl1_idx = pl2_idx = 0
    pl1_len = len(pl1)
    pl2_len = len(pl2)

    while pl1_idx < pl1_len  or pl2_idx < pl2_len :
        if pl1_idx >= pl1_len :
            yield pl2[pl2_idx]
            pl2_idx += 1
        elif pl2_idx >= pl2_len :
            yield pl1[pl1_idx]
            pl1_idx += 1
        elif pl1[pl1_idx].document_id <= pl2[pl2_idx].document_id :
            yield pl1[pl1_idx]
            pl1_idx += 1
        elif pl1[pl1_idx].document_id >= pl2[pl2_idx].document_id :
            yield pl2[pl2_idx]
            pl2_idx += 1

def encode_postings(pl, alg) :
    if alg == 0 :
        return encode_postings_none(pl)
    elif alg == 1 :
        return encode_postings_golomb(pl)
    else :
        return None

def encode_postings_none(pl) :
    return base64.b64encode(pickle.dumps(pl, protocol=2))

def encode_postings_golomb(pl) :
    return pl

def decode_postings(encoded_pl, alg) :
    if alg == 0 :
        return decode_postings_none(encoded_pl)
    elif alg == 1 :
        return decode_postings_golomb()
    else :
        return None

def decode_postings_none(encoded_pl) :
     return pickle.loads(base64.b64decode(encoded_pl))

def decode_postings_golomb(encoded_pl) :
    return encoded_pl

def merge_inverted_index(base_ii, to_be_added_ii) :
    for added_ii_entry in to_be_added_ii :
        base_ii_entry = tokenizer.find_token_from_index(added_ii_entry.token_id, base_ii)
        if base_ii_entry is not None :
            base_ii_entry.docs_count += added_ii_entry.docs_count
            base_ii_entry.positions_count += added_ii_entry.positions_count
            base_ii_entry.postings_list = merge_postings(added_ii_entry.postings_list, base_ii_entry.postings_list)
        else :
            base_ii.append(added_ii_entry)

    to_be_added_ii = None

    return base_ii

def update_postings(ii_entry) :
    old_pl = fetch_postings(ii_entry.token_id)
    if old_pl is not None and len(old_pl) > 0 :
        ii_entry.postings_list =  merge_postings(old_pl, ii_entry.postings_list)
        ii_entry.docs_count = ii_entry.docs_count + len(old_pl)

        ii_entry.postings_list = encode_postings(ii_entry.postings_list, 0)
        wiserdb.db_update_postings(ii_entry.token_id, ii_entry.docs_count, ii_entry.postings_list)

        return True
    elif old_pl is None :
        print "cannot fetch old postings list of token({0}) for update.".format(ii_entry.token_id)
        return False;
    else :
        print "cannot fetch old postings list of token({0}) for update.".format(ii_entry.token_id)
        return False


def fetch_postings(token_id) :
    (docs_count, postings) = wiserdb.db_get_postings(token_id)
    if postings is not None :
        decoded_pl = decode_postings(postings, 0)
        # デコードエラー
        if len(decoded_pl) != docs_count :
            return None
    else :
        decoded_pl = None

    return decoded_pl

def append_positions(ple):
    for pos in range(ple.positions[0] + 1, ple.positions[0] + 5):
        ple.positions.append(pos)
    ple.positions_count = ple.positions_count + 4;

    return ple
