# coding: utf-8

# Copyright 2020-2021 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import re

args = sys.argv
total = 0
passed = 0
failed = 0

try:
    for arg in args[1:]:
        # ress = re.search("^.*\*([0-9]+)\*.*\*([0-9]+).*\*([0-9]+)", str(arg))
        # ress = re.search(".*([0-9]+).*([0-9]+).*([0-9]+).*", str(arg))
        # total += int(ress.group(1))
        # passed += int(ress.group(2))
        # failed += int(ress.group(3))
        restab = re.findall(r'\d+', str(arg))
        total += int(restab[0])
        passed += int(restab[1])
        failed += int(restab[2])

except Exception:
    pass


print("Summary | total: *{}* | passed: *{}* | failed: *{}* | passrate: *{}%*".format(total,
                                                                                     passed, failed, int(passed/total*100)))
