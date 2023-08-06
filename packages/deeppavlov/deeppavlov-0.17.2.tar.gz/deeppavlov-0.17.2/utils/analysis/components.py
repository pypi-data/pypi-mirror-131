# Copyright 2021 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict
from pathlib import Path

from deeppavlov.core.commands.utils import parse_config
from deeppavlov.core.common.registry import list_models
from deeppavlov.core.data.utils import download, download_decompress, get_all_elems_from_json

root = Path(__file__).resolve().parents[2]
configs_path = root / 'deeppavlov' / 'configs'
configs = list(configs_path.glob('**/*.json'))


def get_referred_configs(path: Path, recursively=True):
    ans = []
    current = get_all_elems_from_json(parse_config(path), 'config_path')
    current = [Path(a) for a in current]
    ans.extend(current)
    if recursively:
        for conf in current:
            ans.extend(get_referred_configs(conf, recursively))
    return ans


def get_config_mentions(recursively=True):
    mentions = {c: 1 for c in configs}
    for config in configs:
        for ref in get_referred_configs(config, recursively):
            mentions[ref] = mentions.get(ref, 0) + 1
    return mentions


def get_component_mentions(conf_mentions: dict):
    mentions = {component: 0 for component in list_models()}
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! костыль ниже
    for config, config_multiplier in conf_mentions.items():
        for component in get_all_elems_from_json(parse_config(config), 'class_name'):
            mentions[component] = mentions.get(component, 0) + config_multiplier
    return mentions


def print_mentions(mentions: dict):
    for key in sorted(mentions, key=lambda x: mentions[x], reverse=True):
        print(key, mentions[key])


def mentions():
    config_mentions = get_config_mentions()

    component_mentions = get_component_mentions(config_mentions)
    print_mentions(component_mentions)


def get_users(component):
    ans = []
    for config in configs:
        elements = get_all_elems_from_json(parse_config(config), 'class_name')
        if component in elements:
            ans.append(config.stem)
    return component + ', '.join(ans) or '---'


components = ['api_requester', 'api_router', 'bert_sequence_network', 'bilstm_gru_nn', 'bow', 'char_splitting_lowercase_preprocessor', 'data_fitting_iterator', 'dialog_indexing_iterator', 'dictionary_vectorizer', 'file_paths_iterator', 'file_paths_reader', 'imdb_reader', 'kbqa_reader', 'kvret_dialog_iterator', 'kvret_reader', 'morpho_tagger', 'ner_bio_converter', 'ner_svm', 'params_search', 'pymorphy_russian_lemmatizer', 'pymorphy_vectorizer', 'rel_ranking_reader', 'ru_sent_tokenizer', 'russian_words_vocab', 'siamese_predictor', 'slotfill_raw_rasa', 'static_dictionary', 'str_token_reverser', 'str_utf8_encoder', 'tag_output_prettifier', 'top1_elector', 'torch_text_classification_model', 'torchtext_classification_data_reader', 'typos_custom_reader', 'typos_kartaslov_reader']


if __name__ == '__main__':
    #mentions()
    for comp in components:
        print(get_users(comp))
'''
bert_sequence_network
'''