#  AUTHOR: Roman Bergman <roman.bergman@protonmail.com>
# LICENSE: AGPL3.0
# VERSION 0.3.1

import sys
import logging
import argparse
import itertools


class PasswordDictGenerator():
    def __init__(self):
        self.args = self.get_argv()
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d: %(levelname)s: %(message)s',
            level=getattr(logging, self.args.log.upper(), None),
            datefmt="%H:%M:%S"
        )
        logging.getLogger('ProxyChecker')

    def get_argv(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, add_help=False)
        parser.add_argument('-h', '--help', action='help', help='\tShow this help message and exit')
        parser.add_argument('--log', default='info', help='\tLevel logging: WARNING, ERROR, INFO, DEBUG. Default: INFO.')

        pg_threads = parser.add_argument_group(title='PASSWORD')
        pg_threads.add_argument('-p', action='store', type=str, required=True, help='\tPassword with mask.')

        pg_out = parser.add_argument_group(title='OUTPUT')
        pg_out.add_argument('-o', '--out', action='store', type=str, default='pwdGen.txt', help='\tOutput file name.')

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
        else:
            return parser.parse_args()

    def get_pwd_pattern(self, pwd_raw):
        mask_handler = False
        counter_handler = False
        mask_data = ''
        counter_data = ''
        pwd = []
        for item_tuple in range(0, len(pwd_raw)):
            if pwd_raw[item_tuple] not in ['[', '{'] and not mask_handler and not counter_handler:
                pwd.append(pwd_raw[item_tuple])
            elif pwd_raw[item_tuple] == '[':
                mask_handler = True
            elif pwd_raw[item_tuple] == ']' and pwd_raw[item_tuple + 1] != '{':
                mask_handler = False
                pwd.append({'repeat': 0, 'pattern': mask_data.split(',')})
                mask_data = ''
            elif pwd_raw[item_tuple] == ']' and pwd_raw[item_tuple + 1] == '{':
                counter_handler = True
            elif pwd_raw[item_tuple] == '}':
                mask_handler = False
                counter_handler = False
                pwd.append({'repeat': int(counter_data), 'pattern': mask_data.split(',')})
                mask_data = ''
                counter_data = ''
            elif mask_handler and not counter_handler and pwd_raw[item_tuple] != ']':
                mask_data += pwd_raw[item_tuple]
            elif mask_handler and counter_handler and pwd_raw[item_tuple] != '{':
                counter_data += pwd_raw[item_tuple]
        return pwd

    def save_passwords(self, pwd_list, out_file):
        if pwd_list:
            with open(out_file, 'w') as fw:
                for item_pwd in pwd_list:
                    fw.write(item_pwd + '\n')
            logging.info('{} passwords saved to: {}'.format(len(pwd_list), out_file))
        else:
            logging.error('Ex034')


    def pwd_handler(self, pwd_mask):
        _pwd_tuples = ''
        _pwd_list = []

        for item_tuple in self.get_pwd_pattern(pwd_mask):
            if isinstance(item_tuple, str):
                if not len(_pwd_list):
                    _pwd_tuples += item_tuple
                else:
                    _tmp_pwd_list = []
                    for item_pwd_list in _pwd_list:
                        _tmp_pwd_list.append(item_pwd_list + item_tuple)
                    _pwd_list = _tmp_pwd_list
            elif isinstance(item_tuple, dict):
                if not len(_pwd_list):
                    _pwd_list.append(_pwd_tuples)
                    _pwd_list_mask = []
                    for item_pwd in _pwd_list:
                        _pwd_tuples_mask = []
                        if item_tuple['repeat'] == 0:
                            for item_mask in item_tuple['pattern']:
                                if len(item_mask) == 1:
                                    if item_mask == '!':
                                        _pwd_tuples_mask.append('')
                                    else:
                                        _pwd_tuples_mask.append(item_mask)
                                if len(item_mask) == 2:
                                    if item_mask[0] == '\\':
                                        _pwd_tuples_mask.append(item_mask[1])
                            for item_mask in _pwd_tuples_mask:
                                _pwd_list_mask.append(item_pwd + item_mask)
                            _pwd_list = _pwd_list_mask
                        else:
                            pass
                            # REPEAT > 0
                else:
                    _pwd_list_mask = []
                    for item_pwd in _pwd_list:
                        _pwd_tuples_mask = []
                        if item_tuple['repeat'] == 0:
                            for item_mask in item_tuple['pattern']:
                                if len(item_mask) == 1:
                                    if item_mask == '!':
                                        _pwd_tuples_mask.append('')
                                    else:
                                        _pwd_tuples_mask.append(item_mask)
                                if len(item_mask) == 2:
                                    if item_mask[0] == '\\':
                                        _pwd_tuples_mask.append(item_mask[1])
                            for item_mask in _pwd_tuples_mask:
                                _pwd_list_mask.append(item_pwd + item_mask)
                            _pwd_list = _pwd_list_mask
                        else:
                            pass
                            # REPEAT > 0
        return _pwd_list

    def run(self):
        try:
            self.save_passwords(self.pwd_handler(self.args.p), self.args.out)
        except Exception as error:
            logging.error(error)

if __name__ == '__main__':
    PasswordDictGenerator().run()
