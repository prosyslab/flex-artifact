#!/usr/bin/env python3

from parse import *
import os
from pathlib import Path
import subprocess
from asyncio.subprocess import DEVNULL
import logging
import multiprocessing
import parmap
import yaml
import random
import numpy as np
from benchmark import benchmark
from difflib import SequenceMatcher
import tqdm
import filecmp


PROJECT_HOME = Path(__file__).resolve().parent.parent
COVERAGE_DIR = PROJECT_HOME / 'flip_output'
YML_DIR = PROJECT_HOME / 'benchmark'

RUN_DOCKER_SCRIPT = PROJECT_HOME / 'script/run-docker.py'

logging.basicConfig(
    level=logging.INFO,
    format=
    "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S")


def get_test_num(project, case):
    with open(os.path.join(YML_DIR, project, f'{project}.bugzoo.yml')) as f:
        bug_data = yaml.load(f, Loader=yaml.FullLoader)
        neg_num = 0
        pos_num = 0
        for data in bug_data['bugs']:
            # print(data)
            if data['name'].split(':')[-1] == case:
                neg_num = int(data['test-harness']['failing'])
                pos_num = int(data['test-harness']['passing'])
                # print('FIND!!')
                break
        else:
            raise Exception("TEST NUM NOT FOUND")
    return neg_num, pos_num


def get_test_num(project, case):
    with open(os.path.join(YML_DIR, project, f'{project}.bugzoo.yml')) as f:
        bug_data = yaml.load(f, Loader=yaml.FullLoader)
        neg_num = 0
        pos_num = 0
        for data in bug_data['bugs']:
            # print(data)
            if data['name'].split(':')[-1] == case:
                neg_num = int(data['test-harness']['failing'])
                pos_num = int(data['test-harness']['passing'])
                # print('FIND!!')
                break
        else:
            raise Exception("TEST NUM NOT FOUND")
    return neg_num, pos_num


def read_signal_list(signal_list_file):
    result = []
    for line in signal_list_file:
        parse_line = parse("{}:{}", line.strip())
        if parse_line != None:
            result.append((os.path.basename(parse_line[0]), parse_line[1]))
    return result


def read_call_sequence(cov_file):
    result = []
    with open(cov_file) as f:
        for line in f:
            parse_line = parse("{}:{}", line.strip())
            if parse_line != None:
                result.append((parse_line[0], parse_line[1]))
    return result


def main():
    for project in benchmark:
        for case in benchmark[project]:
            if not os.path.exists(COVERAGE_DIR / project / case / 'branch'):
                continue 
            neg_num, pos_num = get_test_num(project, case)

            combi_result = dict()
            num = 0
            ground_set = set()
            
            origin_call_sequence_list = dict()
            for i in range(neg_num):
                test_num = i+1
                origin_call_sequence_list[test_num] = read_call_sequence(COVERAGE_DIR / project / case / 'value' / 'call' / f"n{test_num}.txt")
            
            with open(COVERAGE_DIR / project / case / 'result_ochiai.txt') as original_file:
                for line in original_file:
                    parse_line = parse("{}:{}\t{} {} {} {}", line.strip())
                    if parse_line==None:
                        continue
                    file, line, neg, pos, _, _ = parse_line
                    if float(neg) == 0:
                        combi_result[(file, line)] = (float(neg), float(pos))
                        
            signal_list_file = open(COVERAGE_DIR / project / case / 'result_branch.txt')
            signal_list = read_signal_list(signal_list_file)
            signal_list_file.close()
            signal_list_neg_file = open(COVERAGE_DIR / project / case / 'result_branch_neg.txt')
            signal_list_neg = read_signal_list(signal_list_neg_file)
            signal_list_neg_file.close()
            
            signal_list += signal_list_neg
            
            for (inject_file, inject_line) in signal_list:
                if not (os.path.exists(COVERAGE_DIR / project / case / 'branch' / inject_file / inject_line / "result_ochiai_error.txt") and os.path.getsize(COVERAGE_DIR / project / case / 'branch' / inject_file / inject_line / "result_ochiai_error.txt") > 2):
                    continue
                
                tmp_ground_set = set()
                
                if not os.path.exists(COVERAGE_DIR / project / case / 'branch' / inject_file / inject_line / 'call'):
                    continue
                
                check_call = True
                for i in range(neg_num):
                    test_num = i+1
                    origin_call_sequence_path = str(COVERAGE_DIR / project / case / 'value' / 'call' / f"n{test_num}.txt")
                    call_sequence_path = str(COVERAGE_DIR / project / case / 'branch' / inject_file / inject_line / 'call' / f"n{test_num}.txt")
                    if not os.path.exists(origin_call_sequence_path) or not os.path.exists(call_sequence_path):
                        check_call = False
                        break
                    diff_result = subprocess.Popen(["diff", f"{origin_call_sequence_path}", f"{call_sequence_path}"], stdout=subprocess.PIPE)
                    result = diff_result.stdout.read().decode('UTF-8', 'ignore').strip().split('\n')
                    result = list(filter(lambda x: not x.startswith('<') and not x.startswith('>') and not x.startswith('-'), result))
                    length_result = subprocess.Popen(["wc", "-l", f"{origin_call_sequence_path}"], stdout=subprocess.PIPE)
                    length = int(length_result.stdout.read().decode('utf-8').split()[0])
                    sum = 0
                    # print(result)
                    if len(result) == 0 or (len(result) == 1 and result[0]==''):
                        continue
                    for line in result:
                        diff_type = (set(line) & set(['a', 'd', 'c'])).pop()
                        diffs = line.split(diff_type)
                        old_lines = diffs[0].split(',')
                        new_lines = diffs[1].split(',')
                        old_from = int(old_lines[0])
                        old_to = int(old_lines[1]) if len(old_lines) > 1 else int(old_lines[0])
                        new_from = int(new_lines[0])
                        new_to = int(new_lines[1]) if len(new_lines) > 1 else int(new_lines[0])
                        old_length = old_to - old_from + 1
                        new_length = new_to - new_from + 1
                        if diff_type == 'c':
                            sum += max(old_length, new_length)
                        elif diff_type == 'a':
                            sum += new_length
                        elif diff_type == 'd':
                            sum += old_length
                    if sum / length > 0.1:
                        check_call = False
                        break
                        
                if check_call==False:
                    continue
                
                num += 1
                
                with open(COVERAGE_DIR / project / case / 'branch' / inject_file / inject_line / 'result_ochiai_error.txt') as error_result_file:
                    for line in error_result_file:
                        parse_line = parse("{}:{}\t{} {} {} {}", line.strip())
                        if parse_line==None:
                            continue
                        file, line, neg, pos, _, _ = parse_line
                        tmp_ground_set.add((os.path.basename(file), line))
                        if (file, line) not in combi_result:
                            combi_result[(file, line)] = (float(neg), float(pos))
                            ground_set.add((os.path.basename(file), line))
                        else:
                            combi_result[(file, line)] = (min(combi_result[(file, line)][0], float(neg)), min(combi_result[(file, line)][1], float(pos)))
                for ground in ground_set:
                    if ground not in tmp_ground_set:
                        combi_result[ground] = (0.0, 0.0)
            print(f"{project}-{case}: Number of used branch: ", num)
            with open(COVERAGE_DIR / project / case / 'branch' / 'result_ochiai_error_multi.txt', 'w') as result_file:
                for ground in combi_result:
                    result_file.write(f"{ground[0]}:{ground[1]}\t{combi_result[ground][0]} {combi_result[ground][1]} 0.0 0\n")


if __name__ == '__main__':
    main()
