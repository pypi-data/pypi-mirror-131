# (c) 2021 frabit-web Project maintained and limited by FrabiTech < blylei.info@gmail.com >
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This file is part of frabit-web

from flask import Blueprint
from . import views
backup = Blueprint('backup', __name__)

