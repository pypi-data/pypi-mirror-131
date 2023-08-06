#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from grutils import utils
from grutils import error
from grutils.utils import date_of

err = error.Error()
print(utils.int_value_of("101.12", err, 0))

print(date_of(datetime.date(datetime.now())))