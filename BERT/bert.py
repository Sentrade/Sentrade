__author__ = "Davide Locatelli"
__status__ = "Development"

import pandas as pd
from pytorch_pretrained_bert.tokenization import BertTokenizer
from nltk.tokenize import sent_tokenize
from pytorch_pretrained_bert.modeling import *
import numpy as np
import torch

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class TextInput(object):
    
    def __init__(self, uid, text, label=None, agree=None):

        self.uid = uid
        self.text = text
        self.label = label
        self.agree = agree

class BertInput(object):

    def __init__(self, input_ids, input_mask, segment_ids, label_id, agree=None):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.agree = agree

def convert_textinput_to_bertinput(text, label_list, max_seq_length, tokenizer, mode='classification'):

    label_map = {label: i for i, label in enumerate(label_list)}
    label_map[None] = 9090

    features = []
    for (txt_i, txt) in enumerate(text):
        tokens = tokenizer.tokenize(txt.text)

        if len(tokens) > max_seq_length - 2:
            tokens = tokens[:(max_seq_length // 4) - 1] + tokens[
                                                              len(tokens) - (3 * max_seq_length // 4) + 1:]

        tokens = ["[CLS]"] + tokens + ["[SEP]"]

        segment_ids = [0] * len(tokens)
        
        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        input_mask = [1] * len(input_ids)

        padding = [0] * (max_seq_length - len(input_ids))
        input_ids += padding
        input_mask += padding
        segment_ids += padding

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length

        label_id = label_map[txt.label]

        agree = txt.agree
        mapagree = {'0.5': 1, '0.66': 2, '0.75': 3, '1.0': 4}
        try:
            agree = mapagree[agree]
        except:
            agree = 0

        if txt_i < 1:
            logger.info("*** Example ***")
            logger.info("guid: %s" % (txt.uid))
            logger.info("tokens: %s" % " ".join(
                [str(x) for x in tokens]))
            logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            logger.info(
                "segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
            logger.info("label: %s (id = %d)" % (txt.label, label_id))

        features.append(
            BertInput(input_ids=input_ids,
                          input_mask=input_mask,
                          segment_ids=segment_ids,
                          label_id=label_id,
                          agree=agree))
    return features

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1)[:, None])
    return e_x / np.sum(e_x, axis=1)[:, None]

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def get_score(text, model):

    model.eval()
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    sentences = sent_tokenize(text)

    label_list = ['positive', 'negative', 'neutral']
    label_dict = {0: 'positive', 1: 'negative', 2: 'neutral'}
    result = pd.DataFrame(columns=['sentence','logit','prediction','sentiment_score'])
    for batch in chunks(sentences, 5):

        text_input = [TextInput(str(i), sentence) for i, sentence in enumerate(batch)]

        bert_input = convert_textinput_to_bertinput(text_input, label_list, 64, tokenizer)

        all_input_ids = torch.tensor([f.input_ids for f in bert_input], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in bert_input], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in bert_input], dtype=torch.long)

        with torch.no_grad():
            logits = model(all_input_ids, all_segment_ids, all_input_mask)
            logits = softmax(np.array(logits))
            sentiment_score = pd.Series(logits[:,0] - logits[:,1])
            predictions = np.squeeze(np.argmax(logits, axis=1))

            batch_result = {'sentence': batch,
                            'logit': list(logits),
                            'prediction': predictions,
                            'sentiment_score':sentiment_score}
            
            batch_result = pd.DataFrame(batch_result)
            result = pd.concat([result,batch_result], ignore_index=True)

    result['prediction'] = result.prediction.apply(lambda x: label_dict[x])

    return result