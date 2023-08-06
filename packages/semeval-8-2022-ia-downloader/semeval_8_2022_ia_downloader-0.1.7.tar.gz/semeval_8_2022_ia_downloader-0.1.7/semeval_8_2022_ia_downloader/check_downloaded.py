import json
import os

from semeval_8_2022_ia_downloader.cli import parse_input, get_local_path_for_article

if __name__ == '__main__':
    location = 'semeval-2022_task8_train-data_batch-2.1.csv'
    dump_dir = 'newarticles'
    missing = list()
    notext = list()
    for article_id, article_link, article_lang in parse_input(location):
        filepath = get_local_path_for_article(article_id, dump_dir)
        if not os.path.exists(filepath):
            missing.append((article_id, article_link, article_lang))
        else:
            json_path = filepath[:-4]+'json'
            with open(json_path, encoding='utf8') as f:
                article_json = json.loads(f.read())
                if not 'text' in article_json or len(article_json['text'].strip())<50:
                    notext.append((article_id, article_link, article_lang))
